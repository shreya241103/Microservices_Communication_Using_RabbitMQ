# Inventory Management System with Microservices and RabbitMQ

## Problem Statement

Build an inventory management system utilizing a microservices architecture with RabbitMQ for inter-service communication and Docker for containerization. 


### Producer Service:

- Develop the producer service responsible for constructing queues/exchanges and transferring data to consumers.
- Implement the HTTP server to listen to health_check and CRUD requests.
- Test the producer service to ensure it interacts correctly with RabbitMQ and handles HTTP requests.

### Consumer Services:

- Implement consumer services (consumer_one to consumer_four) to handle specific tasks like health checks, item creation, stock management, and order processing.
- Ensure each consumer service can communicate with RabbitMQ and perform its designated actions.
- Test each consumer service individually to verify its functionality.

## Design

### Architecture
<img width="875" alt="Screenshot 2024-04-26 at 7 11 57 PM" src="https://github.com/shreya241103/Microservices_Communication_Using_RabbitMQ/assets/115857097/5384e44b-5311-4a85-a405-8de6e2b20ba0">

### Database Design
<img width="684" alt="Screenshot 2024-04-26 at 7 09 14 PM" src="https://github.com/shreya241103/Microservices_Communication_Using_RabbitMQ/assets/115857097/c1cdd87d-c76d-44e6-bb34-bf300e0aea8d">




