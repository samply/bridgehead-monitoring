# Bridgehead-monitoring

A small monitoring service written in rust. The tool checks local bridgehead components and reports the status to a central monitoring service.

## Usage

To run with docker-compose

docker-compose up

Environment Varibales

Var Value
PROXY_ID Your beam proxy.id with full broker url
KEY API key for communication with the beam proxy
