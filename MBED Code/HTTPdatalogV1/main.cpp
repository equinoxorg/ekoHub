
#include "VodafoneUSBModem.h"
#include "HTTPClient.h"
#include "ADC_file.h"
#include <cstdio>
#include <string.h>
#include <string>
#include <iomanip>
#include <sstream>

 
LocalFileSystem  local("local");
Serial pc(USBTX, USBRX);
DigitalOut led(LED1);
DigitalOut led2(LED2);

Timeout interrupt; // interrupt object
stringstream buffer;



void callback();
bool send_data(VodafoneUSBModem& modem, char * data);

bool update;
bool done;

int main()
{
    VodafoneUSBModem modem;
    
    pc.printf("\x1B[2J");    //VT100 erase screen
    
    pc.printf("\rTrying to connect...\n");
    int ret = modem.connect("pp.vodafone.co.uk");
  
   if(ret)
    {
         pc.printf("\r\tCould not connect\n");
         return;
    }
    int time = 0;
    update = false;
    bool stop = false;
    bool file_write = false;
    
        
    float AC_current, AC_voltage, DC_current, DC_voltage;
    char * temp;
    
    AC_current = 0.0;
    AC_voltage = 0.0;
    DC_current = 0.0;
    DC_voltage = 0.0;
    
   
 
    
    // call a function after a delay
   
    interrupt.attach(&callback, UPDATE_TIME);
    
        // main loop
        while( !stop)
        {
          // read output of each sensor  and write to buffer
          pc.printf( "\rReadings = %d ", time);
         // AC_current = (ADCread(1) * 3.3 )/ 1023;
         // pc.printf("\n\rAC current : %.2f ", AC_current );
             
          buffer << AC_current << " ";
          
       //   AC_voltage = ADCread(2);
          buffer << AC_voltage <<  " ";
       
    
       //   DC_current = ADCread(3);
          buffer << DC_current << " ";
      
        //  DC_voltage = ADCread(4);
          buffer << DC_voltage << " ";
      
        
          AC_current++;
          AC_voltage++;
          DC_current++;
          DC_voltage++;
        
        
          
          if(update)
          {
            update = false;
         
            
            // loop carries on if HTTP post is successful
            // otherwise stops and we write to file
            stop = send_data(modem, temp);
            
            if( stop)
                break;
            
           
            buffer.str(""); // empty buffer
            buffer.clear();
            time = 0;
            
           
          } 
           
            wait(DELAY);
            time++;
     
       }
          pc.printf("\n\rDONE!\n\r ");
          modem.disconnect();
    
     
        FILE * fp = fopen("/local/file.txt", "a");
        fprintf(fp, temp);
         
  
        if(fp != NULL)
            pc.printf("\rSuccessfully wrote to file\n\r");
     
        else
        pc.printf("\rUnsuccessful in file write\n\r");
        
        fclose(fp);
               
        pc.printf("\n\r Testing... ");
}


void callback(void)
{
    update = true;
      
} 


bool send_data(VodafoneUSBModem& modem, char * data)
{
    interrupt.detach();
    HTTPClient client;
   
    
    
     
    pc.printf("\n\rInterrupt!\n");
  
    /* Note: double is 8 bytes and char is 1 byte
    so the size if our char buffer must be at least 8n 
    if we want to insert 8 numbers */ 
 
   // char data[] = "4.5 3.2 5.3 4.5";
    char output[512]; // server reply
    long pos = buffer.tellp();
  
    // convert buffer into a string
    // then copy string to buffer
    /*
    strcpy(data, (buffer.str()).c_str());
    pc.printf("\n\rdata to send : %d bytes \r", pos);
    pc.printf("\n\rdata sent : %d bytes \n" , strlen(data));
   
    
    int counter = 0;
    
    temp = data; */
    HTTPMap  message; // data to send
    HTTPText reply(output, 512); // server reply
 
 
   
    // POST DATA
    message.put("measurements" , temp); // map name to file
    pc.printf("\rTrying to post data...\n\r");
    int ret = client.post("http://davidfirstapp.appspot.com/", message, &reply);
  
    if(!ret){
        pc.printf("\rExecuted POST successfully - read %d characters\n\r", strlen(output));
        pc.printf("Result: %s\n\r", output); 
   }
    
  
  
    else { // unsuccessful post - write data to file
        pc.printf("\rError  ret = %d and HTTP return code = %d\n\r", ret, client.getHTTPResponseCode());
    
    }
    
    wait(3.0);
  
    interrupt.attach(&callback, UPDATE_TIME - DELAY);
    return ret;
 
}
