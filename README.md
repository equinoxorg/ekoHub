# Energy Kiosk Observer - Client Scripts


Whats included in this package:
* A Modbus sensor poll module (eko.Sensors)
* A eko_upload synchronisation module (eko.WebService)
* A interface layer for BeagleBoard XM hardware (eko.SystemInterface)
* PPPd connect script generation (scripts/modem)
* Typical sensor config files (config/sensors)
* Typical sensor board EEPROM config templates (config/setup)
* A stand-alone configuration execution utility (configtool.py)
* Misc shell scripts for installation (scripts/install, inittab.sample, etc...)
* A heartbeat service
* Several testbenches and pre-created RSA keys for testing with AppEngine
* A RSA keygen app that generates 1024 bit RSA public/private keys on a beagleboard

As of 31st August 2012, some of this is still a Work in Progress
* The heartbeat script needs to be tested
* Seperation between platform specific and generic code to be fully implemented by use of hooks

## Pre-requisite Packages
* GCC 4.x toolchain (a binary toolchain available from most distros is sufficient)
* Python 2.7.x (2.7.3 or later reccomended)
* PySerial
* PyCrypto 2.3 (2.6 may also be acceptable)
* Poster (http://pypi.python.org/pypi/poster/0.4)
* Modbus-Tk (http://code.google.com/p/modbus-tk/)

It is also reccomended that the following standard linux packages are installed
* OpenSSH / Dropbear SSH
* NTP

### Installation Notes

For the python modules, most are available via Python Setuptools (i.e. easy_install PACKAGENAME). This is the reccomended path for installation. This is also why GCC is required on the target as some libraries must be built from source (automatically).

mobdus-tk is not available via easy_install, thus download the zip package and install it manually.

## The main.py script

main.py is a newly added launcher for the DataLogger script. It serves to perform two primary functions:
1. Command line options allowed for all paths in the system and the various levels of power efficency (latter parts still WiP)
2. Self-Checks to ensure operating environment meets the minimum requirements for execution of the script set

Type `main.py --help` for a usage printout

Typical usage:
`main.py --config /etc/eko --output /data`

Note that the directories passed to main.py must exist. Sanity checks at startup will otherwise exit.

Read main.py for more documentation. Note some parameters are not fully programmable yet. Fix this in code until someone fixes it and updates this doc / main.py.

### Notes on the new Context dictionary

The context or ctx dictionary is instantiated from the command-line arguments passed to main.py. Data is only added to it inside main.py, and the finished construct is passed to the initialiser of the DataLogger class in eko_logger.py. Nearly all sub-modules, classes and functions in the datalogger script set are passed the context variable as it contains all the system paths, serial numbers and Web API URLs. Thus any future additions to the script should pass their configuration parameters at startup through the ctx dictionary to maintain consistancy.

## eko_logger.py

eko_logger.py is still the main entry point for the datalogging script. However, a major change is in effect on the way the script handled post-startup, pre-connect, post-connect and other events. To optimise power, at various stages of the script execution, system level functions needed to be called (Beagleboard specific for example). Having these being directly called from eko_logger.py was an obstacle toward developing on x86 Linux and MacOSX computing environments. As of Aug 2012, these functions are being stripped from eko_logger.py and are being migrated to a external "BoardConfig" class.

All events of note will be assigned standard (by default empty) hook functions. A BoardConfig module will override each function with device specific code. This way, it is ensured that the core script can function independant of platform, and the number of log warnings are also kept at a  minimum.

## configtool.py

Configtool allows the manual execution of a sensor configuration script. This allows independant testing of sensors outside of the main datalogger script.

Usage of the setup script collection alongside this application will also allow for the easy programming of sensor boards. Config files are commented and can be cross referenced with ModbusInterface.py for a better understanding of the available functions and their result.

See typical config sets in ./config for more

## tools/keygen/eko_keygen.py

Call eko_keygen.py with the path to your target config directory as the first and only parameter, i.e.
`eko_keygen.py /etc/eko/`

The keygen will create a fresh RSA public/private key pair if one does not already exist. If a private key does exist, it will extract the public key and print it to the console. This printed public key must be pasted in at v2.ekohub.org.

## tools/pppd_scriptgen

pppd_scriptgen generates and packaged a number of pppd scripts when provided with the operator APN, username and password. These scripts vary from level 0 to level 4 with different levels of added complexity. The script can be executed as follows:

`Usage: pppd_scriptgen.py MODEM OPERATOR APN USERNAME [COMPLEXITY] [PASSWORD]`

The two modems currently supported are the Huawei E220 (he220) and ZTE MF112 (mf112). All other Huawei or ZTE modems should remain compatible with these two units.

### Important

The ppp_script_gen.py script requires a third-party library called ovotemplate. To obtain this, change to the pppd_scriptgen directory and type: wget `get_ovotemplate.README`. Otherwise downloading ovotemplate from the URL specified in this readme and copying via SCP will also work.

## Unittests

Several unittests are included to verify the sanity of the Web Sync code. Ensure that the bundled RSA key is registered as a kiosk online, ensuring that the device serial number is '123456'

