#!/bin/bash

set -e
set -u

# error for getopt
E_OPTERROR=85
# the default interface of the wireless card
INTERFACE="wlan0"
INTERFACE_SET=false
# the default channel to set for the wireless interface
CHANNEL="14"
CHANNEL_SET=false
# the default essid to set for the wireless interface
ESSID="des-mesh0"
ESSID_SET=false
# the default mode to set 
MODE="ad-hoc"
MODE_SET=false
# the default transmit power to set for the wireless interface
TXPOWER="27dbm"
TXPOWER_SET=false
# the ip address of the wireless interface
IP=""
# the netmask of the wireless interface
NETMASK="255.255.0.0"

# check if $1 is set at all
if [[ -n "$1" ]] 
then
  # check if the script was called with the --help option
  if [ $1 = "--help" ] 
  then
    echo "usage: `basename $0` options (-ictmev)"
    echo "        -i <interface> wireless interface to set"
    echo "        -c <channel>   channel of the wireless interface"
    echo "        -t <txpower>   transmit power of the wireless interface"
    echo "        -m <mode>      mode of the wireless interface"
    echo "        -e <essid>     essid of the wireless interface"
    echo "        -v             enable verbose flag"
    exit $E_OPTERROR
  fi
fi

# parse the command line options
while getopts ":i:c:t:m:e:" option 
do
  case $option in
   i ) INTERFACE_SET=true
       INTERFACE=$OPTARG
       ;;
   c ) CHANNEL_SET=true 
       CHANNEL=$OPTARG
       ;;
   t ) TXPOWER_SET=true 
       TXPOWER=$OPTARG
       ;;
   m ) MODE_SET=true
       MODE=$OPTARG
       ;;
   e ) ESSID_SET=true
       ESSID=$OPTARG
       ;;
   : ) echo "option -$OPTARG requires an argument.";;
   * ) echo "unknown option chosen.";;
  esac
done

# interface is 'wlan0'
if [ $INTERFACE = "wlan0" ]
then
  IP=$(calc_ip 0)
# interface is 'wlan1'
elif [ $INTERFACE = "wlan1" ]
then
  IP=$(calc_ip 1)
  # check if the channel is set, otherwise set the default value to 40
  if ! $CHANNEL_SET 
  then
    CHANNEL=40  
  fi
# interface is 'wlan2'
else 
  IP=$(calc_ip 2)
  # check if the channel is set, otherwise set the default value to 44
  if ! $CHANNEL_SET 
  then
    CHANNEL=44
  fi
fi

# set the ip/netmask settings for the wireless interface
ifconfig $INTERFACE $IP netmask $NETMASK
# set the wireless interface parameters 
iwconfig $INTERFACE mode $MODE
iwconfig $INTERFACE essid $ESSID 
iwconfig $INTERFACE channel $CHANNEL
iwconfig $INTERFACE txpower $TXPOWER

