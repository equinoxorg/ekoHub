#include "mbed.h"
#include "VodafoneUSBModem.h"
#include "HTTPClient.h"
#include <stdlib.h>
#include <string.h>



// status LEDs
DigitalOut upload_status(LED1);
DigitalOut not_sent_status(LED2);
DigitalOut timeout_status(LED3);

// objects
Serial pc(USBTX, USBRX);
Timeout interrupt;


// functions
void upload_data(void const * );
void upload_data();
void stop_sending();

// constants
const int MAXCHARS = 60; // length of string to send
const int UPLOAD_TIME = 6000; // in ms
const int CONN_TIMEOUT  = 4; // mbed connection timeout
const int UPLOAD_TIMEOUT = 4; // upload timeout
 
 /*nb: MAXCHARS must be less than CHUNK size. go to HTTPclient.cpp to
  modify chunk size */
  
// variables
bool finishedUploading;
bool stop;
bool readyToSend;
char * data;// data to send




int main() {

   //VT100 erase screen
  pc.printf("\x1B[2J");    
  pc.printf("\rStart! ");
 
  VodafoneUSBModem modem; 
 
  srand(time(NULL)); // set random generator;
  
  pc.printf("\n\rTrying to connect");
  int ret = modem.connect("pp.vodafone.co.uk");
        
  if(ret)
  {
     pc.printf("\n\rCould not connect\n");
     return;
  }
  // main loop
  while(1) 
  {
 
    finishedUploading = false;
    stop = false;
    readyToSend = false;
    char temp[4]; 
    int i = 0;
    
    // prepare the buffer to send
    data = (char *)malloc(sizeof(temp) * MAXCHARS);
    strcpy(data, "");
     
    pc.printf("\n\rCreating buffer...");
    while( i < MAXCHARS) 
    {
      if( i > 0)
        strcat(data, " ");
        
      // generate a random float number
      float a  = (float)rand()/((float)RAND_MAX/100.0);
      sprintf(temp, "%.1f", a); // convert number to string 
      strcat(data, temp); // a number to buffer
      i++;
    }
    pc.printf("\n\rdata is: %s ", data);
    readyToSend = true;
    pc.printf("\n\rReady to send %d bytes", strlen(data));
    upload_data();
    
    
    
    wait(3.0);
    free(data); // deallocate memory 
    pc.printf("\n\rRepeat");
   }
   modem.disconnect();
}

void upload_data()
 {
        //wait before sending
       // Thread::wait(UPLOAD_TIME);
        HTTPClient http;
        char str[512];
        HTTPMap message; // data to send
        HTTPText reply(str, 512);
     
        
        while(!readyToSend) {// do nothing 
        }
        pc.printf("\n\rGoing to send now!");
        
        
  
       // POST DATA
        message.put("measurements" , data ); // map name to file
        
        pc.printf("\n\rTrying to post data...\n");
        pc.printf("\n\rdata: %s", data);
        pc.printf("\n\rData that will be sent: %d bytes", strlen(data) );
    
       
       int ret = http.post("http://davidfirstapp.appspot.com/", message, &reply);
   
    
    
        if (!ret)
        {
            // light up fits LED
            upload_status = 1;
            pc.printf("\n\rExecuted POST successfully - read %d characters\n", strlen(str));
            pc.printf("\n\rResult: %s\n", str);
        }
        else {
            not_sent_status = 1;
            pc.printf("\n\rError : ret = %d \n\r HTTP return code = %d\n", ret, http.getHTTPResponseCode());
        }
       
 }
 
 void stop_sending() 
 {
    stop = true;
    timeout_status = 1;
 }
 
 
 