# UART to Cosm (e.quinox Hydro)

The cosm-client.py script should be run with the serial port as it's input parameter.

`python2 cosm-client.py /dev/ttyUSB0`

Optionally specify the `-u` parameter with the minimum time between server updates in seconds (default 5mins). The code will automatically sync every 9 samples.

The code accepts data in the form `nodename,value\n`, eg: `weir,4\n`.

Only `weir` and `forebay` are accepted.

## Simulator

The simulator allows the code to be tested without the devices being present. To test offline, use `socat` to create a virtual serial port pipe.

On Linux:
`socat -d -d pty,raw,echo=0 pty,raw,echo=0`

This will usually create two ends of a serial port at `\dev\pts\`

The simulator accepts only the serial port as a paramter