#ifndef utilities_header
#define utilities_header

// constants
#define TIMEZONE 2      // define the timezone (3 for UTC+3)
#define DATA_SIZE 70    // define the number of characters in the data buffer
#define LOG_SIZE 335    // define the size of the log

#define NUM_LINES 350    // number of lines of data to store in a day
#define SAMPLE_TIME 600  // sampling time between taking samples from the sensor values in seconds
#define START_OF_DAY 5  // define the start of day in hours from 0000 from which sampling will start
#define END_OF_DAY 19   // define the END of day in hours from 0000 from which sampling will stop

#include "mbed.h"
#include "HTTPClient.h"
#include "NTPClient.h"
#include "link/LinkMonitor.h"

extern Serial pc;
extern char data[DATA_SIZE];

class Watchdog{ // watchdog timer class
    public:
    void kick(float s);
    void kick();
};

extern DigitalOut green2;
extern DigitalOut green1;
extern DigitalOut red;
extern Watchdog wdt;

void createPaths( char filePath[], char  logPath[], char date[]);   // create the filenames and directories in the sd card
char * log(char * path, struct connectivityState state, int lines);    // create the log buffer for each upload stage
void ntpInternetTime(); // get UTC timestamp from ntp - network time protocol
int file_lines(char * path);  //get the number of lines in a text file

struct connectivityState {
   bool connected;
   bool sent;
   int connectionTime;
   int uploadTime;
   int  Rssi;
   LinkMonitor::REGISTRATION_STATE RegistrationState;
   LinkMonitor::BEARER Bearer;

};

#endif