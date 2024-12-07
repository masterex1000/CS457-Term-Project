#!/bin/bash

server_port="57054"
server_address="localhost"
web_host_interface="0.0.0.0"
web_host_port="8080"

show_help() {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -h               Show this help menu"
  echo "  -i <address>     Server address (default: $server_address)"
  echo "  -p <port>        Server port (default: $server_port)"
  echo "  -w <interface>   Web host interface (default: $web_host_interface)"
  echo "  -n <port>        Web host port (default: $web_host_port)"
  exit 0
}

while getopts ":p:i:hw:n:" opt; do
  case $opt in
    p)
      server_port="$OPTARG"
      ;;
    i)
      server_address="$OPTARG"
      ;;
    h)
      show_help
      exit 1
      ;;
    w)
      web_host_interface="$OPTARG"
      ;;
    n)
      web_host_port="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Construct and execute the command
command="python3 -m websockify $web_host_interface:$web_host_port $server_address:$server_port --web=./src/web_client"
echo "Executing: $command"
eval $command