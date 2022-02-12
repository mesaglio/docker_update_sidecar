FROM alpine:3
RUN apk update && apk upgrade && apk add curl jq
WORKDIR /app
COPY script.sh .
ENTRYPOINT [ "sh", "script.sh" ]