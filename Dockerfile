# This assumes binaries are present, see COPY directive.

ARG IMGNAME=gcr.io/distroless/cc

FROM alpine AS chmodder
ARG FEATURE
ARG TARGETARCH
COPY /artifacts/binaries-$TARGETARCH/bridgehead-monitoring /app/
RUN chmod +x /app/*

FROM ${IMGNAME}
ARG TARGETARCH
COPY --from=chmodder /app/* /usr/local/bin/
ENTRYPOINT [ "/usr/local/bin/bridgehead-monitoring" ]

