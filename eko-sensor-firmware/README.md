# EKO Network Board (RS485) Sensor Firmware

This firmware is compatible with:
* EKObb Revision 2 and Revision 3 (PIC24F16KA102)
* PIC24FJ256GB106 Starter Kit (SureElectronics)

Build using the Microchip C30 compiler (XC16).

# Using Network Boards

The network boards connect via a differential RS-485 bus and utilise a subset of the Modbus Protocol. Each device has a unique address on the bus and provides read and write access to a number of regions of memory (SRAM). By writing certain values to registers functionality on the device (ADC/Light Readings) can be triggered.

Each network board has Configuration RAM and Data RAM. Configuration RAM begins at 0x8000 and the first 8 words of this RAM is loaded at boot from the onboard EEPROM. 

## Configuring the Network Board

Config Memory Lock Register: 0x8008 
Config Memory Unlock Code: 0xE010
Config Memory Lock Code: 0xA0EE

The network board can be configured through the modbus interface. To prevent accidental writes to the EEPROM backed configuration memory, that memory region must be unlocked by writing 0xE010 to the Config Memory Lock Register (0x8008).

Once the configuration memory is unlocked, the config region starting at address 0x8000 is available for writing. Each of the 8 registers (0x8000 - 0x8007) is composed of two 8-bit fields encoded in big-endian [MSW:LSW].

### Register 0x8000

0x8000 contains the MODBUS Device Address and MODBUS Device Class.

Register 0x8000 : [MODBUS-DEVICE-ADDRESS:MODBUS-DEVICE-CLASS]

The MODBUS device address must be between 0 and 255. Address 0x00 is reserved for broadcast and Address 0x01 is reserved for failsafe.

The MODBUS device class corresponds to the type of sensor connected. It would be one of the following defined:

* AC_SENSOR : 0x10
* DC_SENSOR_SOLAR : 0x11
* DC_SENSOR_BATTERY : 0x12
* ATMOSPHERIC : 0x13

### Register 0x8001 - 0x8002

0x8001 contains the ADC Input Selection and ADC Sample/Repeat Count. Register 0x8002 contains the ADC Sample Interval and ADC Wait Times.

#### Principal of Operation

The ADC handler implemented on network boards functions as a loop that is triggered by writing to a ADC Control Register (see below). The loop operates in the following sequence:

1. ADC Triggered (Write 0x80 to 0x8009)
2. Select one of the enabled ADC Channels (0,1,2,3,5)
    1. Sample channel and place result in buffer
    2. Wait for [Sample Interval] time
    3. If [Repeat Count] is set, go to 1 until count met
3. Wait for period [Wait Time]
4. Goto 2 and repeat with remaining enabled channels until all are done

Note that on trigger, the process will only occur once for each channel. On completion, the ADC Control Register will be set to 0x00.

See Line 438 of main.c and the file p24_adc.c, specifically the ProcessADCEvents function to see how this works underneath.

#### Configuration

Register 0x8001 : [ADC_INPUT_SELECTION:ADC_SAMPLE_COUNT]

The ADC Input Selection is is a bitmask selection which channels (AN0, AN1, AN2, AN3 or AN5) to sample. Bit 5 corresponds to AN5 and Bit 0 corresponds to AN0 (where AN0 is the LSB).

For example, a value of 0x05 or 0b00000101 would enable AN0 and AN2 for polling. Bit 4 (corresponding to AN4) has no effect since AN4 is not implemented.

The ADC Sample Count determines how many times an ADC input is sampled. For single shot measurements, choosing 1 would suffice.

Register 0x8002 : [ADC_SAMPLE_INTERVAL:ADC_WAIT]

The ADC_SAMPLE_INTERVAL sets, in milliseconds, the time between two successive samples being taken of the same channel. This sampling process is repeated ADC_SAMPLE_COUNT times.

The ADC_WAIT time is the time, in milliseconds, between the sampling of one channel and the next.

#### Register 0x8003

Register 0x8003 contains the I2C chip select followed by a 1 byte zero-padding. The I2C chip select defines which chips are installed on a sensor module and enables them for polling. The register is a bitmask like ADC_INPUT_SELECTION

Register 0x8003 : [I2C_CONTROL:ZEROS]

The following settings are valid for I2C_CONTROL:
* 0x20 selects the Temperature Sensor (MCP9800)
* 0x40 selects the Light Sensor in Single Sample Mode (TSL2561)
* 0x10 selects the Light Sensor in Continuous Sample Mode (TSL2561)

Settings can be logically OR'ed although setting both 0x40 and 0x10 will likely have no effect as 0x10 (continuous) would take precedence.


