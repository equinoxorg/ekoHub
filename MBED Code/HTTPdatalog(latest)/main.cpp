#include "VodafoneUSBModem.h"
#include "HTTPClient.h"
#include "mbed.h"
#include "SDFileSystem.h"
#include "string.h"



SDFileSystem sd(p5, p6, p7, p8, "sd");

Serial pc (USBTX, USBRX);
Timeout write_interrupt;
Timeout upload_interrupt;



// constants
#define SAMPLE_TIME 3.0
#define UPLOAD_TIME 10.0
#define MAXLINES 1000



// flags
bool day_is_over;
bool upload_data;
bool write_data;
 
// functions
void write();
void upload();
void send_data(void const* data);
char * convert_to_byte_stream(char * buffer);



int main() 
{
     // use the mbed RTOS to manage memory and processing/source requirements
     // of the USB modem driver 
    Thread testTask(send_data, NULL, osPriorityNormal, 1024 * 4);
     sd = new SDFileSystem(p5, p6, p7, p8, "sd");
    
   
     char data[MAXLINES] ;
     int day = 0;
     float ac_current, ac_voltage, dc_current, dc_voltage;
     ac_current = 4.5;
     ac_voltage = 6.1;
     dc_current =  2.3;
     dc_voltage = 4.5;
     
     char path[100] ;
     day_is_over = false;
     upload_data = false;
     write_data = false;
     int time = 0;

    pc.printf("\x1B[2J");    //VT100 erase screen
    pc.printf("\rStart! ");
    
  
    // main loop
  //  while(1)
    //  {
    
        day++;
        char temp[8] = "";
        
        // create new directory and new file for each day
        sprintf(temp, "%d", day);
        pc.printf("\n\rtemp is %s", temp);
        
        strcpy(path, "/sd/day");
        pc.printf("\n\rpath is %s ", path);
        strcat(path ,temp);
        pc.printf("\n\rpath is %s ", path);
        
        
        sd.mkdir(path, 0777); 
        strcat(path , "/day");
        strcat(path, temp);
        strcat(path , ".txt");
        
        
        pc.printf("\n\rpath is %s ", path); 
        pc.printf("\n\rDEFAULT STACK SIZE: %d ", (DEFAULT_STACK_SIZE/4));
       
        
        FILE * fp = fopen(path , "w"); 
        
        fprintf(fp, "ac_current\t\t");
        fprintf(fp, "ac_voltage\t\t");
        fprintf(fp, "dc_current\t\t");
        fprintf(fp, "dc_voltage\n");

       
         
        // set interrupts 
        write_interrupt.attach(&write, SAMPLE_TIME);
       
        while( !day_is_over )
        {
            // when ready to write to file,
            // read from sensors and write
            
            if ( time > 2)  // after some time e.g around 6pm day is over
                day_is_over = true; 
                
            if( write_data)
            {
                write_interrupt.detach();
                time++;
              
                
                 pc.printf("\n\rtime %d ", time);
                
                ac_current++;
                ac_voltage++;
                dc_current++;
                dc_voltage++;

                fprintf(fp, "%.2f\t\t\t " , ac_current);
                fprintf(fp, "%.2f\t\t\t ",  ac_voltage);
                fprintf(fp, "%.2f\t\t\t ",  dc_current);
                fprintf(fp, "%.2f \n ",  dc_voltage);
        
                
                write_data = false;
                write_interrupt.attach(&write, SAMPLE_TIME);
              
            }

        }
        write_interrupt.detach();   
        fclose(fp);   
        Thread::wait(1000);
        

        // now read file into a buffer
        fp = fopen(path, "r");
        char tmp[MAXLINES] = "";
        char buffer[MAXLINES] = "";
        char symbol;
        int i = 0;
        int j = 0;
   
        int line = 1;
        bool space = false;
        
       
        // read file into buffer
        if (fp != NULL)
        {
            while(fgets(tmp, MAXLINES, fp  )  != NULL )
                strcat(buffer, tmp);        
        
        }
        
       
       
       // convert the data from the buffer into a byte stream
       // for appropriate transmission
        strcpy(data, convert_to_byte_stream(buffer)) ;
        pc.printf("\n\rTest:        5.50 7.10 3.30");
        pc.printf("\n\rOutput data: %s\n\r", data); 
        fclose(fp);
        delete sd; 
       
        
       
       
        
        
      
        
        
        
        

    
   

}

void write()
{
    write_data = true;
}

void upload()
{
    upload_data = true;
}

// reads from file of current day and
// returns data in an appropriate format
// for transmission

char * convert_to_byte_stream(char * buffer)
{
    bool space = false;
    int i = 0;
    int j = 0;
    
    i = strcspn( buffer, "\n"); // first occurence of eol in string
    pc.printf("\n\ri is %d", i);
    
    char data[MAXLINES];
    
      // start reading from the second line
  
           while ( i < (strlen(buffer) - 1) )
           {
                if (buffer[i] != '\t' && buffer[i] !='\n' && buffer[i] != ' ') // if there's no space
                {
                     if(space) // ...but there was a space previously 
                     {
                          space = false;
                          data[j] = ' ';
                          j++;
                     }
                            
                          data[j] = buffer[i];
                          j++;
                }
                    
                    else // don't add anything to data
                        space = true;
                        
                        i++;
            } 
            pc.printf("\n\rdata is %s", data);
            return data;   
} 

void send_data(void const* data)
{
        
        Thread::wait(17000.0);
        VodafoneUSBModem modem;
        pc.printf("\n\rIn function");
        char temp[] = "4.5 3.2 5.3 4.5";
        char output[512];  
        // HTTP request
        pc.printf("\n\rTrying to connect...\n");
        
        int ret;
        ret = modem.connect("pp.vodafone.co.uk");
     
        if(ret)
        {
            pc.printf("\r\tCould not connect\n");
            return;
        }
     
             
        HTTPClient client;
        HTTPMap  message; // data to send
        HTTPText reply(output, 512); // server reply
 
      
       // pc.printf("\n\rdata sent: %d bytes \n" , strlen(output_data));
        
        // POST DATA
        message.put("measurements" , temp); // map name to file
        pc.printf("\n\rTrying to post data...\n\r");
        ret = client.post("http://davidfirstapp.appspot.com/", message, &reply);
  
    if(!ret){
        pc.printf("\rExecuted POST successfully - read %d characters\n\r", strlen(output));
        pc.printf("Result: %s\n\r", output); 
   }
    
  
  
    else { // unsuccessful post - write data to file
        pc.printf("\rError  ret = %d and HTTP return code = %d\n\r", ret, client.getHTTPResponseCode());
    
    }
   
  
     pc.printf("\n\rDone ! ");
     modem.disconnect();
   
}