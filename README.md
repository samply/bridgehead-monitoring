# Bridgehead-monitoring

A small monitoring service written in Rust. The tool checks local bridgehead components and reports the status to a central monitoring service.

## Usage

This can simply be run with docker-compose:

    docker-compose up

## Environment Varibales

| Variable Name | Meaning |
|-----|-------|
| PROXY_ID | Your beam proxy.id with full broker url |
| KEY API | key for communication with the beam proxy |
