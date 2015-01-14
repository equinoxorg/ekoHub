#include "utilities.h"


// Load timeout value in watchdog timer and enable
void Watchdog::kick(float s) {
   LPC_WDT->WDCLKSEL = 0x1;                // Set CLK src to PCLK
   uint32_t clk = SystemCoreClock / 16;    // WD has a fixed /4 prescaler, PCLK default is /4
   LPC_WDT->WDTC = s * (float)clk;
   LPC_WDT->WDMOD = 0x3;                   // Enabled and Reset
   kick();
}
    
// "kick" or "feed" the dog - reset the watchdog timer by writing this required bit pattern
void Watchdog::kick() {
   LPC_WDT->WDFEED = 0xAA;
   LPC_WDT->WDFEED = 0x55;
}


/** This method creates two files with the given paths,
 *  on the SD card,  encapsulated in the same folder.
 *  These files will respectively contain the sensor
 *  readings saved during an entire day and their corresponding
 *  log. This method will be called everytime the mbed resets.
 *  These files won't be created again if they already exist
 *  @param sensorsfilePath: The path to the file which 
 *  contains all the sensor readings
 *  @param logPath: The path to the file which contains 
 *  a log for every reading
 */
 
void createPaths( char sensorsfilePath[], char  logPath[], char date[]){
    char dirPath[100]; // path to directory
    
    //create file dir path
    strcpy(dirPath, "/sd/");
    strcat(dirPath,  date);
    // make directory       
    mkdir(dirPath, 0777); 
    
    // create dataFile
    strcpy(sensorsfilePath, dirPath);
    strcat(sensorsfilePath, "/data.txt");
 
    
    strcpy(logPath,  dirPath);
    strcat(logPath, "/");
    strcat(logPath , "log.txt");

}


/** Save extra information to log. The log
 *  will be written both to a disk and sent
 *  remotely
 *  @param path: The path for the log file
 *  @param connectivityState: This data structure
 *  holds extensive information regarding connection
 *  time and data transfers
 *  @param lines The total number of lines/ instances
 *  that have been written to the data file so far. 
 *  We used this to determine the number of the instance
 *  whom this log corresponds to
 *  @return A buffer which contains a similar log to be sent
 *  remotely
 */
char * log(char * path, struct connectivityState state, int lines)
{
  char buffer[512];     // buffer to write to the file
  char sendBuffer[LOG_SIZE]; // buffer used to store the log which we will send
  char tmp[200];
  strcpy(buffer, "");
  strcpy(sendBuffer, "");
  
  time_t date;
  date = time(NULL)+ (3600*TIMEZONE);
  
  char * country;
  if(TIMEZONE == 3)
    country = "Kenya";
  if(TIMEZONE == 2)  
    country = "Rwanda";
  if(TIMEZONE ==1)
    country = "UK";  
  
  //write the date in the log
  sprintf(tmp, "------------------------------------------\n%s Time: %s \n", country,  ctime(&date));
  strcat(buffer, tmp);
  
  sprintf(tmp, "%s (%s).\r", ctime(&date), country);
  strcat(sendBuffer, tmp);
  pc.printf("\r%s Time: %s\r", country, ctime(&date));
  
  sprintf(tmp, "instance no. : %d\n", (lines + 1));
  strcat(buffer, tmp  );
  
  if(state.connected) {
    strcat(buffer,"connection : successful\n");
    strcat(sendBuffer, "successful");
    sprintf(tmp, "connection time : %d seconds\n", state.connectionTime);
    strcat(buffer, tmp);
    sprintf(tmp, " (%ds) - ", state.connectionTime);
    strcat(sendBuffer, tmp);
    
    pc.printf("connection : successful\n\r");
    pc.printf("connection time : %d seconds\n\r", state.connectionTime);

    switch(state.Bearer) {
    
        case 0 : strcat( buffer, "connection type: Unknown\n");
        strcat(sendBuffer, "Unknown");
        pc.printf("connection type: Unknown\n\r");
        break;
        
        case 1: strcat( buffer, "connection type: GSM (2G)\n");
        strcat(sendBuffer, "GSM (2G)");
        pc.printf("connection type: GSM (2G)\n\r");
        break;
        
        case 2: strcat(buffer, "connection type: EDGE (2.5G)\n");
        strcat(sendBuffer, "EDGE (2.5G)");
        pc.printf("connection type: EDGE (2.5G)\n\r");
        break;
        
        case 3 : strcat(buffer,"connection type: UMTS (3G) \n");
        strcat(sendBuffer, "UMTS (3G)");
        pc.printf("connection type: UMTS (3G) \n\r");
        break;
        
        case 4 : strcat(buffer,"connection type: HSPA (3G+) \n");
        strcat(sendBuffer, "HSPA (3G+)");
        pc.printf("connection type: HSPA (3G+) \n\r");
        break;
    
    
    }
    
    switch(state.RegistrationState) {
        case 0: strcat(buffer, "registration state : Unknown\n");
        strcat(sendBuffer, ". Unknown Registration");
        pc.printf("registration state : Unknown\n\r");
        break;
        
        case 1: strcat(buffer, "registration state : Registering\n");
        strcat(sendBuffer, ". Registering");
        pc.printf("registration state : Registering\n\r");
        break;
        
        case 2: strcat(buffer, "registration state : Denied\n");
        strcat(sendBuffer, ". Denied Registration");
        pc.printf("registration state : Denied\n\r");
        break;
        
        case 3: strcat(buffer,"registration state : No signal\n");
        strcat(sendBuffer, ". No signal");
        pc.printf("registration state : No signal\n\r");
        break;
        
        case 4: strcat(buffer, "registration state : Registered on Home Network\n");
        strcat(sendBuffer, ". Registered on Home Network");
        pc.printf("registration state : Registered on Home Network\n\r");
        break;
        
        case 5: strcat(buffer,"registration state : Registered on Roaming Network unknown\n");
        strcat(sendBuffer, ". Registered on Roaming Network unknown");
        pc.printf("registration state : Registered on Roaming Network unknown\n\r");
        break;
    
    
    }
    switch( state.Rssi) {
      case 0 : strcat(buffer, "rssi : unknown\n");
      strcat(sendBuffer, " unknown\n");
      pc.printf("rssi : unknown\n\r");
      break;
      
      default : sprintf(tmp,"rssi : %ddbm\n", state.Rssi); 
      pc.printf("rssi : %ddbm\n\r", state.Rssi);
      strcat(buffer, tmp);
      sprintf(tmp," (%ddbm).", state.Rssi); 
      strcat(sendBuffer, tmp);
      
      break;
    
    
    }
    
    if(state.sent){
        strcat(buffer,"upload : successful\n");
        strcat(sendBuffer, " Successful");
        sprintf(tmp,"data sent : %d bytes\n", strlen(data));
        strcat(buffer, tmp);
        sprintf(tmp," (%d bytes - ", strlen(data));
        strcat(sendBuffer, tmp);
        sprintf(tmp,"server response time: %d seconds\n", state.uploadTime);
        strcat(buffer, tmp);
        sprintf(tmp,"%ds).", state.uploadTime);
        strcat(sendBuffer, tmp);
        
        
        pc.printf("upload : successful\n\r");
        pc.printf("data sent : %d bytes\n\r", strlen(data));
        pc.printf("server response time: %d seconds\n\r", state.uploadTime);
         
    }
      
    else{
        strcat(buffer,"upload : unsuccessful\n");
        strcat(sendBuffer," Unsuccessful.");
        pc.printf("upload : unsuccessful\n\r");
    }
  }
    
  else{
   strcat(buffer, "unsuccessful\n");
   strcat(sendBuffer," Unsuccessful.");
   pc.printf("connection : unsuccessful\n\r");
   }
   
   FILE * fp2 = fopen(path, "a");
   fprintf(fp2, "%s", buffer); 
   fclose(fp2);
   
   return sendBuffer;
}

/** Set the RTC from the Internet time
*/

void ntpInternetTime() 
{
    NTPClient ntp;
    time_t InternetTime;
    int time_int = 0;
    
    do{
        if (ntp.setTime("0.pool.ntp.org") == 0)
        {
            pc.printf("\n\rManaged to set time successfully");  
            InternetTime = time(NULL);
            InternetTime += ((3600)*TIMEZONE);  // add TIMEZONE Hours for correct time in country
            time_int = InternetTime;
            pc.printf("\n\rInternet timestamp %d ", InternetTime);
            pc.printf("\n\rInternet time as basic string %s \n ", ctime(&InternetTime));  
            if(time_int<0)
                pc.printf("\n\rInternet time is invalid...Trying Again");
        }
      }
      while(time_int < 0 && time_int < 1376326229); // check if time is correct i.e. is in the future
} 

int file_lines(char * path){
    
    char buff[100];
    int lines = 0;
    FILE *f;
    if (f = fopen(path, "r")){

        while(fgets(buff,100,f) != NULL) {
            lines++;
        } 
        fclose(f);
    }
    else lines = 0;
    
    return lines;
}