FROM alpine:3.14

# Install Python
RUN apk add --no-cache python3 py3-psutil

WORKDIR /app

# Copy the script files
COPY main.py /app/

# Run the script
CMD ["./main.py"]
