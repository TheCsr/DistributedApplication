# DistributedApplication

Luleå University of Technology

Course: D7001D

Instructor: Dr. Evgeny Osipov

Group Members: Mirjalol Aminov, Nadir Arfi, Diana Mustakhova, Chandan Singh, Brianna Swan

## Overview
This project is a distributed networking system implementing a special kind of publish-subscribe functionality. It enables communication between clients connected anonymously to a server. A client publishes encrypted data to the server, which maintains a database. A subscriber client knows the publisher's ID, and requests its data from the server. The subscriber client receives the enrypted data, and decrypts it. 

Client interfaces are web applications using Flask.

## How to Use

### Create a new virtual environment and install the required libraries.
pip install -r requirements.txt

### Launch the server:
python server.py

### Launch the publisher
python Publisher.py [ip]:[port]

### Launch the subscriber
python Susbscriber.py [ip]:[port]

