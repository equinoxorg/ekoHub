/* VodafoneUSBModem.h */
/* Copyright (C) 2012 mbed.org, MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 * and associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute,
 * sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 * BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#ifndef VODAFONEUSBMODEM_H_
#define VODAFONEUSBMODEM_H_

#include "core/fwk.h"

#include "USB3GModule/WANDongle.h"
#include "at/ATCommandsInterface.h"
#include "serial/usb/USBSerialStream.h"
#include "ip/PPPIPInterface.h"
#include "sms/SMSInterface.h"
#include "ussd/USSDInterface.h"
#include "link/LinkMonitor.h"
#include "utilities.h"

/** Vodafone USB Modem (K3770/K3772-Z) dongle
 */
class VodafoneUSBModem
{
public:
  /** Create Vodafone USB Modem (K3770/K3772-Z) dongle API instance
      @param powerGatingPin Optional pin commanding a power gating transistor on the modem's power line 
      @param powerGatingOnWhenPinHigh true if the pin needs to be high to power the dongle, defaults to true
   */
  VodafoneUSBModem(PinName powerGatingPin = NC, bool powerGatingOnWhenPinHigh = true);

  //Internet-related functions

  /** Open a 3G internet connection
      @return 0 on success, error code on failure
  */
  int connect(const char* apn = NULL, const char* user = NULL, const char* password = NULL);

  /** Close the internet connection
     @return 0 on success, error code on failure
  */
  int disconnect();


  /** Send a SM
     @param number The receiver's phone number
     @param message The message to send
     @return 0 on success, error code on failure
   */
  int sendSM(const char* number, const char* message);


  /** Receive a SM
     @param number Pointer to a buffer to store the sender's phone number (must be at least 17 characters-long, including the sapce for the null-terminating char)
     @param message Pointer to a buffer to store the the incoming message
     @param maxLength Maximum message length that can be stored in buffer (including null-terminating character)
     @return 0 on success, error code on failure
   */
  int getSM(char* number, char* message, size_t maxLength);

  /** Get the number of SMs in the incoming box
     @param pCount pointer to store the number of unprocessed SMs on
     @return 0 on success, error code on failure
   */
  int getSMCount(size_t* pCount);

  /** Send a USSD command & wait for its result
    @param command The command to send
    @param result Buffer in which to store the result
    @param maxLength Maximum result length that can be stored in buffer (including null-terminating character)
    @return 0 on success, error code on failure
  */
  int sendUSSD(const char* command, char* result, size_t maxLength);
  
  /** Get link state
    @param pRssi pointer to store the current RSSI in dBm, between -51 dBm and -113 dBm if known; -51 dBm means -51 dBm or more; -113 dBm means -113 dBm or less; 0 if unknown
    @param pRegistrationState pointer to store the current registration state
    @param pBearer pointer to store the current bearer
    @return 0 on success, error code on failure
  */
  int getLinkState(int& pRssi, LinkMonitor::REGISTRATION_STATE& pRegistrationState, LinkMonitor::BEARER& pBearer);  

  /** Get the ATCommandsInterface instance
    @return Pointer to the ATCommandsInterface instance
   */
  ATCommandsInterface* getATCommandsInterface();
  
  /** Switch power on or off
    In order to use this function, a pin name must have been entered in the constructor
    @param enable true to switch the dongle on, false to switch it off
    @return 0 on success, error code on failure
  */
  int power(bool enable);

protected:
  bool power(); //< Turn power to USB dongle ON.

  /** Initialise dongle.
   * The following actions are performed:
   * 1) Power up
   * 2) Establish USB connection to dongle
   * 3) Start AT interface thread
   * 4) Wait for network registration
   */
  int init();
  
  /** De-initialise dongle.
   * The following actions are performed:
   * 1) Tear down PPP session
   * 2) Set SMS,USSD, and LinkMonitor subsystems to un-initialised
   * 3) Close the AT commands interface
   * 4) Tear down the USB connection to dongle
   */
  int cleanup();

private:
  WANDongle m_dongle;          //< Interface to USB connected WAN dongle
  
  USBSerialStream m_atStream;  //< Serial interface to AT channel on modem
  USBSerialStream m_pppStream; //< Serial interface to PPP channel on modem
  
  ATCommandsInterface m_at;    //< Interface to AT commands processing
  
  SMSInterface m_sms;          //< Interface to SMS manager (send/receive etc)
  USSDInterface m_ussd;        //< Interface to USSD manager (send etc)
  LinkMonitor m_linkMonitor;   //< Interface to link monitor (RSSI)
  
  PPPIPInterface m_ppp;        //< Interface to PPP conection manager (IP assignment etc)

  bool m_dongleConnected; //< Is the dongle physically connected (does the USB stack respond)? true/false
  bool m_ipInit;          //< Has PPIPInterface object (m_ppp) been initialised? true/false
  bool m_smsInit;         //< Has SMSInterface object (m_sms) been initialised? true/false
  bool m_ussdInit;        //< Has USSDInterface object (m_ussd) been initialised? true/false
  bool m_linkMonitorInit; //< Has LinkMonitor object (m_linkMonitor) been initialised? true/false
  bool m_atOpen;          //< Is the interface to the ATCommandsInterface open? true/false
  
  PinName m_powerGatingPin;        //< Pin which toggles power gating
  bool m_powerGatingOnWhenPinHigh; //< Semantics of power gating (whether high or low toggles power gating)
};


#endif /* VODAFONEUSBMODEM_H_ */
