#include "ADC_file.h"



int ADCread(int pinNO)
{ //function to perform conversion and read value from Analog Devices AD7993 ADC using the command mode (option 2 on datasheet)

    I2C i2c(p28, p27);
    char data[2]; //variable to store values read from ADC
    int conv;

    if(pinNO == 1) //choose conversion value to send to ADC to tell it which pin to convert on
         conv = 0x10;
    
    else if(pinNO == 2)
          conv = 0x20;
    
    else if(pinNO == 3)
          conv = 0x40;
    
    else if(pinNO ==4)
          conv = 0x80;
    

    i2c.start(); //start I"C process
    i2c.write(ADCAddr); // Send address of ADC on SDA 
    i2c.write(conv); // Send the command to convert on correct pin and set the address pointer to the conversion result register
    wait(0.7); //wait for conversion to take place

    i2c.read(ADCAddr, data, 2); //read from the ADC - it will automatically read from the result register
    i2c.stop(); //stop process
        
    int x = data[0] & 0xF; //top byte of data - and with 0xF as only bottom 4 bits are useful
    int y = data[1]; //bottom byte of data 
        
    int z = (x<<8)|y; //shift top byte of data to the top part of the int and or it with bottom part so they are concatenated
        
    return z; //return integer value from ADC - 12bit resolution
        
    //for more information see AD7993/AD7994 datasheet 
}


