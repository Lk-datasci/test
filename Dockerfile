FROM alpine:latest

LABEL maintainer="test-hem-4812"

RUN echo "Hello from HuggingFace source!" && \
    echo "Pipeline build OK"

CMD ["echo", "Container started successfully"]
