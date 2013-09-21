#include "mbed.h"
#include <I2C.h>
#include <DigitalOut.h>

DigitalOut myled(LED1);
DigitalOut pin1(p21); // green
DigitalOut pin2(p22); // middle green 
DigitalOut pin3(p23); // red

I2C i2c(p28, p27);
Serial pc(USBTX, USBRX);

int ADCread(int pinNO, const int ADCAddr);
int ACread(int pinNO, int ADCAddress);

int main() {
    
    const int ADCAddr1 = 0x44; // DC Voltage
    const int ADCAddr2 = 0x42; // DC Current
    const int ADCAddr3 = 0x40; // AC Board
    
	float VREF = 5;
    float resolution = 1023;
	float factor = 5/1023;
    

    while(1) {
      
        int VDC1 = ADCread(1,ADCAddr1);
        int VDC2 = ADCread(2,ADCAddr1);
        int VDC3 = ADCread(3,ADCAddr1);
        int VDC4 = ADCread(4,ADCAddr1);
        
        int IDC1 = ADCread(1,ADCAddr2);
        int IDC2 = ADCread(2,ADCAddr2);
        int IDC3 = ADCread(3,ADCAddr2);
        int IDC4 = ADCread(4,ADCAddr2);
        
        int AC1 = ACread(1,ADCAddr3);
        int AC2 = ACread(2,ADCAddr3);
        int AC3 = ACread(3,ADCAddr3);
        int AC4 = ACread(4,ADCAddr3);

        pc.printf("\n\rVDC1: %f \t", VDC1*factor);
        pc.printf("VDC2: %f \t", VDC2*factor);
        pc.printf("VDC3: %f \t", VDC3*factor);
        pc.printf("VDC4: %f \t", VDC4*factor);
        
        pc.printf("\n\rIDC1: %f \t", IDC1*factor);
        pc.printf("IDC2: %f \t", IDC2*factor);
        pc.printf("IDC3: %f \t", IDC3*factor);
        pc.printf("IDC4: %f \t", IDC4*factor);
        
        pc.printf("\n\rAC1: %f \t", AC1*factor);
        pc.printf("AC2: %df\t", AC2*factor);
        pc.printf("AC3: %f \t", AC3*factor);
        pc.printf("AC4: %f \t \n\r", AC4*factor);
        
        wait(1.5);

    }
}


int ACread(int pinNO, int ADCAddress){
    
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
            val = ADCread(pinNo, ADCAddress);	//  get sample of AC wave
            
            if (val<min)	
                min = val;
                
            if (val>max)
                max = val;
            
			if (counter%60 == 0){  // calculate peak to peak and average every 60 samples
			
				pk2pk = max - min;
				avg = (pk2pk + (avg*avgcount)/(1+avgcount)) // calculates a cumulative average
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

int ADCread(int pinNO, const int ADCAddr){ //function to perform conversion and read value from Analog Devices AD7993 ADC using the command mode (option 2 on datasheet)

    int conv;
    char data[2]; //variable to store values read from ADC

if(pinNO == 1){ //choose conversion value to send to ADC to tell it which pin to convert on
    conv = 0x10;
    }
else if(pinNO == 2){
    conv = 0x20;
    }
else if(pinNO == 3){
    conv = 0x40;
    }
else if(pinNO ==4){
    conv = 0x80;
    }
    
        i2c.start(); //start I2C process
        i2c.write(ADCAddr); // Send address of ADC on SDA 
        i2c.write(conv); // Send the command to convert on correct pin and set the address pointer to the conversion result register
        wait(0.001); //wait for conversion to take place

        i2c.read(ADCAddr, data, 2); //read from the ADC - it will automatically read from the result register
        i2c.stop(); //stop process
        
        int top = data[0] & 0xF; //top byte of data - and with 0xF as only bottom 4 bits are useful
        int bot = data[1]; //bottom byte of data 
        
        int full = (top<<8)|bot; //shift top byte of data to the top part of the int and or it with bottom part so they are concatenated
        full = full>>2;
        return full; //return integer value from ADC - 10bit resolution
        
        //for more information see AD7993/AD7994 datasheet 
}