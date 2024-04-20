package main

import (
	"encoding/json"
	"fmt"

	"github.com/streadway/amqp"
)

type Message struct {
	Type       string `json:"type"`
	CustomerID string `json:"customer_id"`
}

var ProductsMessageChannel = make(chan map[string]interface{})
var OrdersMessageChannel = make(chan map[string]interface{})
var Ch *amqp.Channel

func ProduceReadMessage(msg Message) {
	body, err := json.Marshal(msg)
	failOnError(err, "Failed to marshal JSON")
	err = Ch.Publish(
		"",     // exchange
		"Read", // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		})
	failOnError(err, "Failed to publish a message")
	fmt.Println(" [x] Sent", msg)
}

func ConsumeDataMessages() {
	msgs, err := Ch.Consume(
		"Data", // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	for d := range msgs {
		var data map[string]interface{}
		err := json.Unmarshal(d.Body, &data)
		failOnError(err, "Failed to unmarshal JSON")
		fmt.Printf(" [x] Received data\n")
		// fmt.Printf(" [x] Received data from %s\n", data["table"])
		// fmt.Println("Data:", data["data"])

		if data["table"] == "products" {
			ProductsMessageChannel <- data
		} else {
			OrdersMessageChannel <- data
		}
	}
}
