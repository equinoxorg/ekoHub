#!/bin/sh

if [ -e ppp-connect-eko.tar.gz ]
then
	echo "File exists, installing"
	echo "You better be root!"
	mv ./ppp-connect-eko.tar.gz /
	cd /
	tar xvzf ppp-connect-eko.tar.gz
else
	echo "File does not exist. Run build.sh."
fi
