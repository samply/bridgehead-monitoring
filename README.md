# Bridgehead-monitoring

A small monitoring service written in Rust. The tool checks local bridgehead components and reports the status to a central monitoring service.

## Usage

bridgehead-monitoring [OPTIONS] --beam-id <BEAM_ID> --beam-api-key <BEAM_API_KEY>

```
Options:
      --beam-id <BEAM_ID>            Beam id for the application [env: BEAM_ID=]
      --beam-api-key <BEAM_API_KEY>  Beam secret for the application [env: BEAM_API_KEY=]
      --beam-proxy <BEAM_PROXY>      Beam proxy url [env: BEAM_PROXY=] [default: http://beam-proxy]
      --blaze-url <BLAZE_URL>        Blaze base url [env: BLAZE_URL=] [default: http://blaze]
  -h, --help                         Print help
```

## Docker usage

The configuration options can all be set via enviroment variables as seen in [usage](#usage).

Example:
```yml
  bridgehead-monitorer:
    image: samply/bridgehead-monitoring:rust-rewrite
    environment:
      - BEAM_ID=monitoring.${PROXY_ID}
      - BEAM_API_KEY=${BEAM_APP_SECRET}
      - BEAM_PROXY=http://beam-proxy
    depends_on:
      - beam-proxy
```

