package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetProducts(c *gin.Context) {
	fmt.Println("Here Now")
	var message Message
	message.CustomerID = ""
	message.Type = "read_products"
	go ProduceReadMessage(message)
	result := <-ProductsMessageChannel
	fmt.Println("Result Data:", result["data"])
	c.JSON(http.StatusOK, result["data"])
}

func GetOrdersByID(c *gin.Context) {
	customer_id := c.Param("id")
	var message Message
	message.CustomerID = customer_id
	message.Type = "read_orders"
	go ProduceReadMessage(message)

	result := <-OrdersMessageChannel
	fmt.Println("Result Data:", result["data"])
	c.JSON(http.StatusOK, result)
}

func PostOrder(c *gin.Context) {
	var newOrder Order

	if err := c.BindJSON(&newOrder); err != nil {
		return
	}

	fmt.Println("Order: ", newOrder)
}
