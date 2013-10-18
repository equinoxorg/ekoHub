#include "ADC_file.h"


int ADCread(int pinNO , int ADC)
{ //function to perform conversion and read value from Analog Devices AD7993 ADC using the command mode (option 2 on datasheet)

    I2C i2c(p28, p27);
    char data[2]; //variable to store values read from ADC
    int conv; // indicates pin that will be read
    int ADCaddr; // ADC we're reading from
    
    
    // select ADC
    switch(ADC) {
        case 1 : ADCaddr = ADC1;
        break;
        
        case 2 : ADCaddr = ADC2;
        break;
        
        case 3 : ADCaddr = ADC3;
        break;
    }
    
    // select pin
    switch(pinNO) {
    
        case 1 : conv = 0x10;
        break;
        
        case 2: conv = 0x20;
        break; 
        
        case 3: conv = 0x40; 
        break;
        
        case 4: conv = 0x80; 
        break;
        
  
     }

    i2c.start(); //start I2C process
    i2c.write(ADCaddr); // Send address of ADC on SDA 
    i2c.write(conv); // Send the command to convert on correct pin and set the address pointer to the conversion result register
    wait(0.001); //wait for conversion to take place

    i2c.read(ADCaddr, data, 2); //read from the ADC - it will automatically read from the result register
    i2c.stop(); //stop process
        
    int x = data[0] & 0xF; //top byte of data - and with 0xF as only bottom 4 bits are useful
    int y = data[1]; //bottom byte of data 
        
    int z = (x<<8)|y; //shift top byte of data to the top part of the int and or it with bottom part so they are concatenated
    z = z>>2;    
    
    return z; //return integer value from ADC - 12bit resolution
        
    //for more information see AD7993/AD7994 datasheet 
}


int ACread(int pinNo, int ADCAddress){

        I2C i2c(p28, p27);
   
        int val=0;
        int min=512;
        int max=512;
        int counter=0;
        int numSamples = 600; // increase this by increments of 50
        int pk2pk=0;
        int avg=0;
        int avgcount=0;
                               
        while (counter <= numSamples)
        {
            val = ADCread(pinNo, ADCAddress);           //  get sample of AC wave
           
            if (val<min)            
                min = val;
               
            if (val>max)
                max = val;
           
            if (counter%60 == 0){  // calculate peak to peak and average every 60 samples
                                               
               pk2pk = max - min;
               avg = ((pk2pk + (avg*avgcount))/(1+avgcount)); // calculates a cumulative average
               avgcount++;
                                                               
               // reset min and max values after calculating average
               min=512;
               max=512;
                                                               
            }
                                               
            counter++; 
            wait(0.001); // wait for 1ms
                                               
        }
       
        return avg;
 
}
