# Use the official Golang image as a base image
FROM golang:latest

# Set the working directory inside the container
WORKDIR /go/src/app

# Copy the Go modules files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the entire source code into the container
COPY . .

# Run the producer.go file
CMD ["go", "run", "producer.go"]
