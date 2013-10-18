#ifndef data_header
#define data_header

#include "mbed.h"
#include "rtos.h"
#include "ADC_file.h"
#include "utilities.h" 

extern char data[DATA_SIZE];

extern bool finished_storing;
extern bool finished_uploading;
extern bool sent;

extern Mutex mutex;
extern Serial pc;
extern Timeout file_interrupt;
extern Timer timer;
extern DigitalOut led2;

extern DigitalOut green1;
extern DigitalOut green2;

void sendData(void const* arg);
void storeData(char * path);
void sendLog(char * buffer, char * path);


#endif