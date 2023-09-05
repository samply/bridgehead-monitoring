# Bridgehead-monitoring

A small monitoring service written in Rust. The tool checks local bridgehead components and reports the status to a central monitoring service.

## Usage

```
bridgehead-monitoring [OPTIONS] --beam-id <BEAM_ID> --beam-api-key <BEAM_API_KEY>

Options:
      --beam-id <BEAM_ID>                Beam id for the application [env: BEAM_ID=]
      --beam-api-key <BEAM_API_KEY>      Beam secret for the application [env: BEAM_API_KEY=]
      --beam-proxy-url <BEAM_PROXY_URL>  Beam proxy url [env: BEAM_PROXY_URL=] [default: http://beam-proxy:8081]
      --blaze-url <BLAZE_URL>            Blaze base url [env: BLAZE_URL=] [default: http://blaze:8080]
  -h, --help                             Print help
```

## Docker usage

The configuration options can all be set via enviroment variables as seen in [usage](#usage).

Example:
```yml
  bridgehead-monitoring:
    image: samply/bridgehead-monitoring:latest
    environment:
      - BEAM_ID=monitoring.${PROXY_ID}
      - BEAM_API_KEY=${BEAM_APP_SECRET}
      - BEAM_PROXY_URL=http://beam-proxy
    depends_on:
      - beam-proxy
```

