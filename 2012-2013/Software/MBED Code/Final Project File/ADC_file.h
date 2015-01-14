#ifndef adc_header
#define adc_header

#include "mbed.h"
#include <I2C.h>


#define UPDATE_TIME 20.0 // 18Ksecs = 5 hours
#define DELAY 1.0

// ADC addresses
const int ADC1 = 0x42; // DC current board 
const int ADC2 = 0x44; //DC voltage board
const int ADC3 = 0x40; //AC board 


//read from an ADC
int ADCread(int pinNo, int ADC);
int ACread(int pinNO, int ADCAddress);




#endif