package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/streadway/amqp"
)

const (
	producer1Threshold = 5 // Threshold in seconds for Producer 1
	producer2Threshold = 5 // Threshold in seconds for Producer 2
)

var (
	lastMessageTimeProducer1 time.Time
	lastMessageTimeProducer2 time.Time
	mutex                    sync.Mutex
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func handleMessages(d amqp.Delivery) {
	mutex.Lock()
	defer mutex.Unlock()
	if string(d.Body) == "Alive producer1" {
		lastMessageTimeProducer1 = time.Now()
	} else if string(d.Body) == "Alive producer2" {
		lastMessageTimeProducer2 = time.Now()
	}
}

func checkProducers() {
	for {
		time.Sleep(1* time.Second) // Check every 30 seconds

		mutex.Lock()
		currentTime := time.Now()
		// Check if Producer 1 has sent a message within the threshold
		if currentTime.Sub(lastMessageTimeProducer1) > producer1Threshold*time.Second {
			fmt.Println("Producer 1 is not working")
		}
		// Check if Producer 2 has sent a message within the threshold
		if currentTime.Sub(lastMessageTimeProducer2) > producer2Threshold*time.Second {
			fmt.Println("Producer 2 is not working")
		}
		mutex.Unlock()
	}
}

func main() {
	fmt.Println("Go RabbitMQ Consumer")

	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"HealthCheck", // Queue name
		false,         // Durable
		false,         // Delete when unused
		false,         // Exclusive
		false,         // No-wait
		nil,           // Arguments
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	go checkProducers()

	for d := range msgs {
		handleMessages(d)
	}

	fmt.Println("Consumer started. To exit press CTRL+C")
	signalCh := make(chan os.Signal, 1)
	signal.Notify(signalCh, syscall.SIGINT, syscall.SIGTERM)
	<-signalCh
	fmt.Println("Shutting down...")
}
