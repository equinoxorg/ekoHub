/* ********************************************************************* *
 * 				Energy Kiosk Observer : Sensor Firmware					 *
 * 						Version 2 / Aug 2011							 *
 *  																	 *
 * ********************************************************************* *
 * 		AUTHORS:		Charith Amarasinghe <ca508@ic.ac.uk>			 *
 *						Gonzalo de Gisbert	<gdg90@ic.ac.uk>	         *
 *																		 *
 * ********************************************************************* *
 */
#define USE_AND_OR

#define TARGET_EKOBB_R3
#include "board/chip.h"
#include "board/p24_fuses.h"
#include "board/p24_board.h"
#include "include/modbus2.h"

//p24 libs
#include <uart.h>
#include <timer.h>

//mb crc tables
#include "include/crc_tables.h"

unsigned char rxbuf[10];
unsigned char txbuf[64];

unsigned char rx_msg;
unsigned char error_code;

unsigned char j = 0;

void init_uart1(int BRG)
{
	U1MODE = 0x8000; /* Enable UART, set RTS to simplex */
	U1STA = 0x0400; /* Enable transmit */
	IFS0bits.U1RXIF = 0;	
	IPC2bits.U1RXIP = 6;
	IEC0bits.U1RXIE = 1;
	U1BRG = BRG;
}

void __attribute__ ((interrupt,no_auto_psv)) _U1RXInterrupt(void)
{
    // for function codes 0x01 to 0x06, the expected length is 8.
    // we only support functions 0x01 to 0x06. 
	
	U1RX_Clear_Intr_Status_Bit;
 	
	while(!U1STAbits.URXDA);
    rxbuf[j++] = (U1RXREG & 0xFF);
    
	if(j >= 8) /* limitation */
	{
		rx_msg=1; // flag that a pdu is recvd
		IEC0bits.U1RXIE = 0; //disable interrupt
		j = 0;
	}
}

void error_led_on( void )
{
	mLED2_On()
}

int main (void)
{

	unsigned char temp = 0;
	AD1PCFG = 0xFFFF;
	TRISBbits.TRISB2 = 1; // In
	TRISBbits.TRISB7 = 0; // Out
	TRISBbits.TRISB8 = 0;
	LATBbits.LATB8 = 0;
	

	mInitLED();
	
	while(1)
	{	
		// init uart and interrupts
		rx_msg = 0;
		init_uart1(25);
		mLED1 = 0;
		mLED2 = 0;
  		while (!rx_msg);
		// message recvd. in rxbuf.
		temp = validate_pdu(rxbuf);

		if (temp == 1)
		{
			mLED2 = 0; // reset error led
			// message is known good!
			mLED1 = 1; // frame led on
			temp = process_pdu(rxbuf, txbuf);
			LATBbits.LATB8 = 1; // enable transmit
			Nop();
			Nop();
			Nop();
			Nop();
			Nop();
			while(temp > 0)
			{
				while(U1STAbits.UTXBF);
				U1TXREG = txbuf[--temp];
			}
			// transmit response
			// frame led off.
		}
		U1MODE = 0x0000;
		LATBbits.LATB8 = 0;
		Nop();
		Nop();
	}
}

