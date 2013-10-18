#include "dataTransfer.h"
#include "HTTPClient.h"
#include "utilities.h"

void storeData(char * path)
{

    time_t current_time = time(NULL) + (3600*TIMEZONE);
    pc.printf("\n\rTime : %s ", ctime(&current_time));  
    pc.printf("\n\rWriting file to %s ", path);
    int time_int = current_time;
    
     // read values from ADCs 
     
     green2 = 1;
     int ac_voltage1 = ACread(1, 3);
     green2 = 0;
     wait(0.4);
     green2 = 1;
     int ac_voltage2 = ACread(2, 3);
     green2 = 0;
     wait(0.4);
     green2 = 1;
     int ac_current1 = ACread(3, 3);
     green2 = 0;
     wait(0.4);
     green2 = 1;
     int ac_current2 = ACread(4, 3);
     green2 = 0;
     
     wait(0.5);
     
     green2 = 1;
     int dc_current1 = ADCread(1, 1);
     int dc_current2 = ADCread(2, 1);
     int dc_current3 = ADCread(3, 1);
     int dc_current4 = ADCread(4, 1); 
     green2 = 0;
     
     wait(0.5);
     
     green2 = 1;
     int dc_voltage1 = ADCread(1, 2);
     int dc_voltage2 = ADCread(2, 2);
     int dc_voltage3 = ADCread(3, 2);
     int dc_voltage4 = ADCread(4, 2); 
     green2 = 0;
     
     //Test values
     /*
     green2 = 1;
     int ac_current1 = 4345;
     int ac_current2 = 5533;
     int ac_voltage1 = 6024;
     int ac_voltage2 = 7356;
     green2 = 0;
     
     wait(0.5);
     
     green2 = 1;
     int dc_current1 = 3434;
     int dc_current2 = 9434;
     int dc_current3 = 2323;
     int dc_current4 = 124;
     green2 = 0;
     
     wait(0.5);
     
     green2 = 1;
     int dc_voltage1 = 5423;
     int dc_voltage2 = 1040;
     int dc_voltage3 = 9920;
     int dc_voltage4 = 9545; 
     green2 = 0;
     */
     
     pc.printf("\n\rACC 1 : %4d ", ac_current1);
     pc.printf("\n\rACC 2 : %4d ", ac_current2);
     pc.printf("\n\rACV 1 : %4d ", ac_voltage1);
     pc.printf("\n\rACV 2 : %4d ", ac_voltage2);
        
     pc.printf("\n\rDCC 1 : %4d ", dc_current1);
     pc.printf("\n\rDCC 2 : %4d ", dc_current2);
     pc.printf("\n\rDCC 3 : %4d ", dc_current3);
     pc.printf("\n\rDCC 4 : %4d ", dc_current4);
    
     pc.printf("\n\rDCV 1 : %4d ", dc_voltage1);
     pc.printf("\n\rDCV 2 : %4d ", dc_voltage2);
     pc.printf("\n\rDCV 3 : %4d ", dc_voltage3);
     pc.printf("\n\rDCV 4 : %4d ", dc_voltage4);
     
     pc.printf("\n\rTIME : %d ", time_int);
   
   // convert the integers into a suitable string format for upload
    char data_buffer[110] = "";
    char tmp[12];
    
    strcat(data_buffer, "");
    
    sprintf(tmp, "%d", ac_current1);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", ac_current2);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", ac_voltage1);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", ac_voltage2);
    strcat(data_buffer, tmp);
    
    sprintf(tmp, " %d", dc_current1);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", dc_current2);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", dc_current3);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", dc_current4);
    strcat(data_buffer, tmp);
    
    sprintf(tmp, " %d", dc_voltage1);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", dc_voltage2);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", dc_voltage3);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", dc_voltage4);
    strcat(data_buffer, tmp);
    sprintf(tmp, " %d", time_int);
    strcat(data_buffer, tmp);
    
    pc.printf("\n\n\rData Buffer: %s\n\r", data_buffer);
    // open file to write
    FILE * fp = fopen(path, "a");

    fprintf(fp, "%4d, ",  ac_current1);
    fprintf(fp, "%4d, ",  ac_current2);
    fprintf(fp, "%4d, ",  ac_voltage1);
    fprintf(fp, "%4d, ",  ac_voltage2);
            
    fprintf(fp, "%4d, ",  dc_current1);
    fprintf(fp, "%4d, ",  dc_current2);
    fprintf(fp, "%4d, ",  dc_current3);
    fprintf(fp, "%4d, ",  dc_current4);
            
            
    fprintf(fp, "%4d, ",  dc_voltage1);
    fprintf(fp, "%4d, ",  dc_voltage2);
    fprintf(fp, "%4d, ",  dc_voltage3);
    fprintf(fp, "%4d, ",  dc_voltage4); 
            
    fprintf(fp, "%d\n",      time_int); 
    
    fclose(fp);
    strcpy(data, data_buffer);
     
}


void sendData(void const* ) 
{
      
      while(1) {
      
        // upload data regularly
        while(1) 
        { 
            mutex.lock();
            if(finished_storing) {
                mutex.unlock();
                break;
            }
            mutex.unlock();
        } 
 
         //POST data
        HTTPClient http;
        HTTPMap message; // data to send
           
        char str[512];
        HTTPText reply(str, 512);
        message.put("e.quinoxsensors" , data); // map name to file
        pc.printf("\n\rTrying to post data...\n");
        pc.printf("\n\rData: %s", data);
        pc.printf("\n\rData that will be sent: %d bytes", strlen(data) );
    
        timer.start();
        int ret = http.post("http://davidfirstapp.appspot.com/sensors", message, &reply);
        timer.stop();
    
        if (!ret)
        {
            //light up second LED
            led2 = 1;
            sent = true;
            pc.printf("\n\rExecuted POST successfully - read %d characters\n", strlen(str));
            pc.printf("\n\rResult: %s\n\r\n\r", str);
        }
        else
        {
            pc.printf("\n\rError : ret = %d \n\r HTTP return code = %d\n\n\r", ret, http.getHTTPResponseCode());
            
            green1 = 1;
            green2 = 1;
            wait(3);
            green1 = 0;
            green2 = 0;
        }
        // lock the "finished_uploading" variable to prevent the main thread
        // from accessing it at the same time
        mutex.lock();
        finished_uploading = true; 
        mutex.unlock();
        Thread::wait(20000);
        pc.printf("\n\rFinished waiting");
     }
  
     
}

void sendLog(char * buffer, char * path)
{
           
      HTTPClient client;
      HTTPMap  message; // data to send
      char output[512];  
      HTTPText reply(output, 512); // server reply
      message.put("e.quinoxlog", buffer);
      
      pc.printf("\n\rTrying to post log...\n\r");
      int ret = client.post("http://davidfirstapp.appspot.com/log", message, &reply);
      
      if (!ret)
      {
      
           pc.printf("\n\rExecuted POST successfully - read %d characters\n", strlen(output));
           pc.printf("\n\rResult: %s\n", output);
           
      }
      else
      {
           pc.printf("\n\rError : ret = %d \n\r HTTP return code = %d\n", ret, client.getHTTPResponseCode());
           
           green1 = 1;
           green2 = 1;
           wait(3);
           green1 = 0;
           green2 = 0;
           
           FILE * fp1 = fopen( path, "a");
           fprintf(fp1, "\nUNSUCCESSFUL LOG UPLOAD\n");
           fclose(fp1);
      }
}