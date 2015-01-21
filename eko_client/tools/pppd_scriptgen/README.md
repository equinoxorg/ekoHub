# PPPd Script Generator

Run the pppd script generator by calling:
`python pppd_scriptgen.py MODEM OPERATOR APN USERNAME [COMPLEXITY] [PASSWORD] [USB]`

*MODEM* is either _he220_ (for Huawei Modems) or _mf112_ (for ZTE modems)

*OPERATOR* is a human friendly name for the cellular operator (no spaces). eg: tigorw

*APN* is the APN for the operator (eg: giffgaff.com, 3internet, web.tigo.rw)

*USERNAME* as supplied by the operator, type "" if username is to be blank

*COMPLEXITY* (Optional), A number between 0 and 4, start with 0, try 1...4 if you have problems

*PASSWORD* (Optional), if supplied provide here, if empty but you want to type USB (next up), use ""

*USB* (Optional), By default it is assumed the modem is at /dev/gsmmodem, but you can manually override through this variable. Do not specify the /dev/ parameter, i.e. valid options are *ttyUSB0* or *gsmmodem*

Example uses:

`python pppd_scriptgen.py he220 tigorwanda web.tigo.rw "" 0`

`python pppd_scriptgen.py he220 tigorwanda web.tigo.rw "" 0 "" ttyUSB0`

`python pppd_scriptgen.py he220 giffgaffuk giffgaff.com giffgaff 1 "" ttyUSB0`

# Installation

The built scripts are put into the folder ./build

To package them into a tar.gz file, run build.sh while in the tools/pppd_scriptgen directory

eg:
`sh build.sh`

To install them (if you are root on the system, run install.sh

eg:
`sh install.sh`

Or you could install manually by copying the generated tar.gz file to root and extracting it there.

# Testing

To test the scripts, first ensure that they have been installed as above.

Find the script name you created/installed

`ls -l /etc/ppp/peers/`

Results are typically in the format

`he220.giffgaff.1.peer'
i.e. `modemname.operatorname.level.peer`

Now execute pppd with this connection as the target

`pppd call he220.giffgaff.1.peer nodetach`

If the nodetach option is not passed, the pppd instance will go to the background. By using nodetach you are able to see debug information from pppd and also to see if the connection was successful.

To kill a detached pppd, use `killall pppd`