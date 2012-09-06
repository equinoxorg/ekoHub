# Sensor Config Files for Setup

## Defaults

Note that default values like the serial port to use and baudrate should go in sensor.default.cfg in the config directory (usually /etc/eko/sensor.default.cfg)

## How it works

The config values in the DEFAULT section are inherited by all other config sections. Put common values such as the modbus address here.

Each remaining config section of the cfg file has a prefix number which controls it's order of execution.

Each config section is a MODBUS command, and the register address, operation type (read/write) and value (if present) are specified as configuration entries.

I.e. a typical config section to write 0xABCD to register 0x8020 is as follows

```
[01WRITEABCD]
mb_func=6
mb_start=0x8020
mb_count=1
mb_write=0xABCD
```

Section `[00WRITEBEFORE]`, if present, would have been executed prior.


## Using the setup scripts

The setup scripts are tailored for a standard kiosk. Firstly open up (or cat) a setup script for the type of sensor you wish to program. For situations with two identical sensors, use one script for one sensor; i.e. AC sensor 1 uses ac.setup.cfg and AC sensor 2 uses ac2.setup.cfg.

Ensure that the device is *the only device* physically connected to the proper port on the datalogger as specified by the `port_num` parameter of the setup config file.

If the device address in known, update it on the script. Otherwise, reset the EEPROM on the sensor board (see attached png) and set the address in the script to 0x01 (the default address).

Ensure that the default settings script is present and up-to-date (/etc/eko/sensor.default.cfg)

Section `01SETMBADDR` sets the new address of the sensor, ensure that this will not conflict with any other sensors previously configured. The setup script set has been written to ensure that this does not happen.

Once the setup script is updated, save it, and go to the root of the eko_client directory

Run `configtool.py`

`python configtool.py configs/setup/ac.setup.cfg /tmp /etc/eko`

where the first parameter was the path to the config file. A configuration memory dump will be downloaded and placed in the /tmp folder.

