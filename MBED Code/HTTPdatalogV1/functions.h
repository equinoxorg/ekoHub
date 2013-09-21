#ifndef adc_header
#define adc_header

#include "mbed.h"
#include <sstream>
#include <fstream>
#include <I2C.h>


#define UPDATE_TIME 20.0 // 18Ksecs = 5 hours
#define DELAY 1.0


const int ADCAddr = 0x42;


// read from an ADC
int ADCread(int pinNo);
//bool file_update(stringstream buffer);




#endif