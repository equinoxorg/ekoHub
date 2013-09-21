#include "mbed.h"
#include "VodafoneUSBModem.h"
#include "HTTPClient.h"

DigitalOut myled(LED1);
Serial pc(USBTX, USBRX);
/*
void test(void const*) 
{
    VodafoneUSBModem modem;
    HTTPClient http;
    char str[512];
    
    int ret = modem.connect("SMART"); //pp.vodafone.co.uk");
    if(ret)
    {
      printf("Could not connect\n");
      return;
    }
    
    //GET data
    printf("Trying to fetch page...\n");
    ret = http.get("http://mbed.org/media/uploads/donatien/hello.txt", str, 128);
    if (!ret)
    {
      printf("Page fetched successfully - read %d characters\n", strlen(str));
      printf("Result: %s\n", str);
    }
    else
    {
      printf("Error - ret = %d - HTTP return code = %d\n", ret, http.getHTTPResponseCode());
    }
    
    //POST data
    HTTPMap map;
    HTTPText text(str, 512);
    map.put("Hello", "World");
    map.put("test", "1234");
    printf("Trying to post data...\n");
    ret = http.post("http://httpbin.org/post", map, &text);
    if (!ret)
    {
      printf("Executed POST successfully - read %d characters\n", strlen(str));
      printf("Result: %s\n", str);
    }
    else
    {
      printf("Error - ret = %d - HTTP return code = %d\n", ret, http.getHTTPResponseCode());
    }
    
    modem.disconnect();  

    while(1) {
    }
}


int main()
{
  Thread testTask(test, NULL, osPriorityNormal, 1024 * 4);
  DigitalOut led(LED1);
  while(1)
  {
    led=!led;
    Thread::wait(1000);  
  }

  return 0;
}
/*
*/
int main(){

VodafoneUSBModem modem;

//int ret = 1;
char str[512];

//while(ret != 0){

int ret = modem.connect("SMART");   //pp.vodafone.co.uk");
//}

HTTPClient http;
HTTPMap map;

map.put("v1", "7"); 
HTTPText text(str, 512);
ret = http.post("http://humanspace.org.uk/PE/saveDat.php?name=map",map, &text);

if(!ret){
    pc.printf("success %s\n", str);
    }
else
    pc.printf("no \n");
  
  
}