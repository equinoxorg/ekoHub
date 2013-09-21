#include "mbed.h"
#include "SDFileSystem.h"
 
SDFileSystem sd(p5, p6, p7, p8, "sd"); // the pinout on the mbed Cool Components workshop board
Serial pc(USBTX, USBRX);
 
int main() {
    printf("Hello World!\n");   
 
    mkdir("/sd/data", 0777);
    
    float result =34.893009;

    
    FILE *fp = fopen("/sd/data/data9.txt", "w");
    if(fp == NULL) {
        error("Could not open file for write\n");
    }

    float x[10];
    int i =0;
    for(i =0; i<9; i++)
    {
        x[i] = result + (5*i);
        fprintf(fp, "%f \n", x[i]);         
    }
    fclose(fp); 
 
    FILE *fp1 = fopen("/sd/data/data9.txt", "r");
    float y;
      while (!feof(fp1)){                        // while not end of file
           fscanf(fp1, "%f", &y);                         // get a character/byte from the file
           pc.printf("%f \t",y); 
      }
      fclose(fp1);      
      
    printf("Goodbye World!\n");
}
