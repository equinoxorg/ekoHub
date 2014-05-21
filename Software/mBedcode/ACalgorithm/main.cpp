#include "mbed.h"

#define SAMPLE_RATE 0.002  // in seconds
#define SAMPLE_TIME 0.5 // in seconds

LocalFileSystem local("local");
Serial pc(USBTX, USBRX);


// configure unused ADC pins as DigitalOut
// to reduce noisy spikes
DigitalOut led(LED1);
DigitalOut led2(LED2);
DigitalOut ai15(p15);
DigitalOut ai16(p16);
DigitalOut ai17(p17);
DigitalOut ai18(p18);
DigitalOut ai19(p19);



Ticker timer; // timer interrupt to read from sinewave
AnalogIn Vin(p20); // voltage input in percentage
 
volatile float * samples;
volatile int ADC_count = 0; // number of ADC samples
volatile float Vmin;
volatile float Vmax;
int intial_read = 1; // initial sinewave read to compute initial min an max values
void check_wave(); // initial wave check
void ADC_read();

int main()
{
     float Vrms; // RMS voltage
     mbed_interface_disconnect(); // turn off debug
     
     // allocated total number of samples
     const int total_samples = ceil(SAMPLE_TIME/SAMPLE_RATE);
     samples = (float*)malloc(sizeof(float)*total_samples);
     
     
     check_wave();
     pc.printf("initial values\n\r");
     pc.printf("Vmax = %.4f\n\r", Vmax);
     pc.printf("Vmin = %.4f\n\r", Vmin);
     
     led2 = 1;
     
     // set interrupt
     timer.attach(&ADC_read, SAMPLE_RATE);

     
     
     // wait until all samples have been read
     while(ADC_count != total_samples){         
     // do nothing
     }
     timer.detach(); 
     Vrms = 0.707*(Vmax - Vmin)/2;
     
    
     FILE *fp = fopen("/local/samples.txt", "w");  // Open "samples.txt" on the local file system for writing
     
     int i;
     fprintf(fp, "Vrms = %.4f\n\n", Vrms);
     fprintf(fp, "Vmax = %.4f\n\n", Vmax);
     fprintf(fp, "Vmin = %.4f\n\n", Vmin);
     fprintf (fp,"total number of samples : %d\n\n", total_samples);
     
     for(i=0; i < total_samples; i++){
        fprintf(fp,"%.4f\n" , samples[i]);   
     }
     fclose(fp);
     
     free((void *)samples);
     pc.printf("\n\rFinished\n\r");
     return 0;
     
}

void ADC_read(){
    
    
    float tmp = Vin*3.3;
    //pc.printf("sample %d: %.4f\n\r", ADC_count, samples[ADC_count]);
    ADC_count++;
    
    if (tmp > Vmax)
        Vmax = tmp;
        
    else if (tmp < Vmin)
        Vmin = tmp;

    samples[ADC_count] = tmp;
  
}

void check_wave(){
    
    // we assume a mains input frequency of 50Hz for the AC signal
    // => f = 50Hz <=> T = 20ms
    
    // choose the number of samples to read
    const int N = 100;
    
    // choose Ts such that only a single period of the sinewave is covered
    float Ts = (0.02)/N;
    
    int i;
    
    // initialize extremum values to first sample
    Vmax = 3.3*Vin;
    Vmin = Vmax;
     
    // read the remaining N-1 samples of the input with a time spacing
    // of Ts seconds between each
    for(i=0; i < N-1; i++){
        
        float tmp = 3.3*Vin;
        if (tmp < Vmin) {
           // pc.printf("less\n\r");
            Vmin = tmp;
        }
            
        else if (tmp > Vmax){
           // pc.printf("more\n\r");
            Vmax = tmp;
        }
            
        wait(Ts);   
    }
}