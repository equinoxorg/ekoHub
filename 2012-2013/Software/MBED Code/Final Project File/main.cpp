#include "mbed.h"
#include "VodafoneUSBModem.h"
#include "HTTPClient.h"
#include "SDFileSystem.h"
#include "utilities.h"
#include "ADC_file.h"
#include "dataTransfer.h"
#include "link/LinkMonitor.h"
#include "PowerControl/PowerControl.h"
#include "PowerControl/EthernetPowerControl.h"

Serial pc(USBTX, USBRX);

Timer timer; // to calculate the time for modem to connect
Mutex mutex;  // mutual exclusion object created to ensure parts of the code don't use the same resource at the same time

DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);

// Status Indication LEDs
DigitalOut red(p23);
DigitalOut green1(p22);
DigitalOut green2(p21);

// global data buffer. Needs to be global due to the sendData thread
char data[DATA_SIZE];

char apn[] = "internet.mtn";
char user[] = "";
char password[] = "";

// flags
bool sent; // indicates if data was uploaded
bool finished_uploading; // lets the mutex know that the modem has finished using the shared resources
bool finished_storing;  // lets the mutex and thread know that sd card has finished using the resources
bool day_is_over;   // variable to indicate whether we have sampled enough data for the day

int result; // for use of the mbed interface power down

Watchdog wdt;

int main()
{  
    red = 1;        // setup status indication LEDs
    green1 = 0;
    green2 = 0;
    
    //pc.printf("\x1B[2J");   //VT100 erase screen  
    pc.printf("\n\r\n\r\n\r\n\r-------------------------------\n\rStart! ");
    
    //result = mbed_interface_powerdown();    // turns off power to unused peripherals
    
    wdt.kick(60);  // setup a timeout on watchdog timer hardware.
    pc.printf("\n\rSetup watchdog timer to 60 seconds");
                                 
    VodafoneUSBModem modem; 
    
    //initiate thread for uploading data later. This must be executed as
    //a separate program to control memory and process requirements
    Thread upload(sendData, NULL, osPriorityNormal, 1024 * 4);
    
    struct tm *tmp;
    time_t curtime;
    int time_hrs;
    int time_mins;
    char mins[2];
    char hour[2];
    curtime = time(NULL);           // get the time from the RTC. 
    tmp = localtime(&curtime);
    strftime(hour, 2, "%H", tmp);  // convert the time into 24Hour Hours format
    time_hrs = atoi(hour) + TIMEZONE;
        
    strftime(mins, 2, "%M", tmp);    // get the time in minutes past the hour
    time_mins = atoi(mins);
    
    int time_int = curtime;
    
    pc.printf("\n\rRTC Time: %d Hours %d Minutes\n\r", time_hrs, time_mins);
    
    // ONLY GET INTERNET TIME IF THE RTC TIME IS WRONG i.e. if it is way in the past or periodically i.e. around every 90 minutes
    if(time_int < 1377427463 || (time_hrs%2 == 0 && (time_mins > 25 && time_mins <35))){
    
        pc.printf("\n\rTrying to connect...");
        green1 = 1;
        modem.connect(apn, user, password);
        pc.printf("\n\rGetting ntp internet time");
        ntpInternetTime();
        modem.disconnect();
        green1 = 0;
        
    }
    wdt.kick(45); 
    pc.printf("\n\rWatchdog timer reset to 45 seconds");
    
    // setup the date for the directories
    char date[256];
    curtime = time(NULL);
    
    int curtime_int = 0;
    curtime_int += (3600*TIMEZONE);
    curtime = curtime_int;
    
    time(&curtime);
    tmp = localtime(&curtime);
    strftime(date, 256, "%d%b%Y", tmp);
    pc.printf("\r\n%s\n", date);
    
    time_hrs = 0;
    strftime(hour, 26, "%H", tmp);
    time_hrs = atoi(hour) + TIMEZONE;
    
    pc.printf("\n\rHours: %d\n\r", time_hrs);
    
    SDFileSystem sd(p5, p6, p7, p8, "sd"); // setup sd filesystem

    char filePath[100]; // path to file
    char logPath[100]; // path to log
 
    // create the strings which store the directories of the files in the sd card
    createPaths(filePath, logPath, date);        
    pc.printf("\n\rFile path: %s\n", filePath);
    pc.printf("\n\rLog path: %s\n", logPath);
    
    // find the number of lines in the data file
    
    int lines = 0;
    lines = file_lines(filePath);
    pc.printf("\n\rNo. of lines in %s: %d", filePath, lines);
    
    //inititalize leds and flags
    led1 = 0;
    led2 = 0;
    led3 = 0;
    finished_uploading = false;
    finished_storing = false;
    sent = false;
    day_is_over = false;
    
    // start storing and uploading 
    // only if if the file is not full and if the time is within an acceptable range
    
    if(lines < NUM_LINES && time_hrs >= START_OF_DAY && time_hrs < END_OF_DAY){ 
        
        day_is_over = false;
        
        // read data from ADC and store in a data buffer
        storeData(filePath);
        // Open a 3G connection
        pc.printf("\n\rTrying to connect");
        green1 = 1;
        wdt.kick(40); 
        pc.printf("\n\rWatchdog timer reset to 40 seconds");
       
        // time connection setup
        timer.start();
        int ret = modem.connect(apn, user, password); // safaricom
        timer.stop();
        
        // get connection state
        struct connectivityState connectivityState;
        int  Rssi;
        LinkMonitor::REGISTRATION_STATE RegistrationState;
        LinkMonitor::BEARER Bearer;
        int linkstate = modem.getLinkState(Rssi, RegistrationState, Bearer);
    
        // get link state info
        if ( !linkstate ) 
        {
          connectivityState.Rssi = Rssi;
          connectivityState.RegistrationState = RegistrationState;
          connectivityState.Bearer = Bearer;
        } 
       
        // read connection time
        connectivityState.connectionTime = timer.read();
        if(ret){
             pc.printf("\n\rCould not connect\n");
             return;
        }
        
        else
        connectivityState.connected = true;
        
        mutex.lock();
        finished_storing = true;
        mutex.unlock();
         
        // wait until upload is finished or timeout has reached
        while(1) 
        { 
          // lock the "upload_is_finished" variable to prevent the other thread
          // from accessing it at the same time. 
            mutex.lock();
            if(finished_uploading) {
                modem.disconnect();
                mutex.unlock();
                break;
             }
            mutex.unlock();
        } 
        
        connectivityState.sent = sent;
        connectivityState.uploadTime = timer.read();
        
        upload.terminate();     // terminate the upload thread 
        green1 = 0;
        
        char * logData; 
        logData = log(logPath, connectivityState, lines); // write all the log in the sd card
        
        pc.printf("\n\n\rBuffer to send:\n\r%s\n\r", logData);
        
        wdt.kick(SAMPLE_TIME); 
        pc.printf("\n\rWatchdog timer reset to %d seconds", SAMPLE_TIME);
        
        green1 = 1;
        pc.printf("\n\rTrying to connect to send log");
        modem.connect(apn, user, password);
        sendLog(logData, logPath);  // upload the log data
    
        pc.printf("\n\rDone!");
        modem.disconnect();
        green1 = 0;
        
        free(data);
        led1 = 1;

        wdt.kick(SAMPLE_TIME); 
        pc.printf("\n\rWatchdog timer reset to %d seconds", SAMPLE_TIME);
        
        result = mbed_interface_powerdown();    // turns off power to unused peripherals
        PHY_PowerDown();
        Sleep();
        Peripheral_PowerDown(0xFFFF7FFF);

        while(1){   // infinite while loop. the chip will reset after the sample time has elapsed and start again.
            led3 = 1;
            day_is_over = false;  
        }  

    } //END IF
    else {
        
        pc.printf("\n\r\n\rNow the system should do nothing except for maintain time\n\r");
        day_is_over = true;
    }
    
    time_mins=0;
    
    while(day_is_over == true)
    {   
        curtime = time(NULL);           // get the time from the RTC. 
        tmp = localtime(&curtime);
        strftime(hour, 2, "%H", tmp);  // convert the time into 24Hour Hours format
        time_hrs = atoi(hour) + TIMEZONE;
        
        strftime(mins, 2, "%M", tmp);
        time_mins = atoi(mins);
        
        // if time has reached the start of day condition
        if(time_hrs == START_OF_DAY){  
            
            day_is_over = false;
            wdt.kick(1); // reset the mbed after 1 second
        }
        
        //setup the watchdog timer to appropriate value. 
        int wd_value = 0;

        if(time_hrs >= START_OF_DAY){
        
            wd_value = ((23 - time_hrs + (START_OF_DAY))*60) + (60 - time_mins);
        }
        else wd_value = (((START_OF_DAY) - time_hrs - 1)*60) + (60 - time_mins);
       
       
        pc.printf("\n\rWatchdog set to %d hours %d mins", ((wd_value - (60 - time_mins))/60), (60-time_mins));
        
        wd_value = wd_value*60;
        pc.printf("\n\rWatchdog Value: %d", wd_value);
        
        wdt.kick(wd_value);
        pc.printf("\n\rTime: %02d:%02d\n\r", time_hrs, time_mins);

       if(time_mins > 25 && time_mins < 35){ // periodically set the time 
            
            wdt.kick(40); // reset watchdog to 40 seconds
            pc.printf("\n\rTrying to connect...");
            green1 = 1;
            modem.connect(apn, user, password);
            pc.printf("\n\rGetting ntp internet time");
            ntpInternetTime();
            modem.disconnect();
            green1 = 0;
            wdt.kick(wd_value);  // reset watchdog after time has been set

       }

       result = mbed_interface_powerdown();    // turns off power to unused peripherals
       day_is_over = true;
       pc.printf("\n\rNow wait 5 mins");
       wait(300);
    }

}  // end of main function
