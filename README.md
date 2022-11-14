# bridgehead-monitoring
A small monitoring service for your local bridgehead. It checks local components and transmit the status to  a central monitoring service.

## Usage

To run with docker-compose

```docker-compose up```

### Environment Varibales

| Var |  Value |
|---|---|
| HOST  |  Hostname of the system |
| SITE_NAME  |  The full name of our site  |
| PROJECT  | Specifies the project. Currently we only support ccp/bbmri  |
| PROXY_ID  |  Your beam proxy.id with full broker url |
| MONITORING_TARGET  |  Specifies the target monitoring services provided by the project |
| KEY  |  API key for communication with the beam proxy  |
| BEAM_URL  |  Specifies the beam proxy URL |