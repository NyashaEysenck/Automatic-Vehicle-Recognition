Automatic Vehicle Recognition System
This project was developed as a school group project that implements an Automatic Vehicle Recognition System using Python and Flask, designed for managing clients, detecting license plates from video streams, extracting text using OCR, and managing entry approvals based on recognized plates.

Table of Contents

Introduction

Features

Installation

Usage

Technologies Used

Contributing

License

### Introduction
The Automatic Vehicle Recognition System is designed to streamline vehicle entry management by automatically detecting license plates from video streams and managing entry approvals based on recognized plates. It integrates with an external camera for real-time video streaming and uses OCR for extracting text from detected license plates.

### Features

License plate detection using Haar Cascade classifier.
OCR for extracting text from detected license plates.
Real-time video streaming and annotation.
Approval and logging system based on recognized plates.
Email notifications for updates made to clients' or guards' accounts.
User management: Superuser can add new guards, clients, and vehicles.

### Installation

clone the repositor
cd automatic-vehicle-recognition
pip install -r requirements.txt

### Usage

# Starting the Flask Server
run python main.py in the root directory
# Accessing the Video Feed
Open your web browser and go to http://localhost:5000
(NOTE - The address will not displayed to the terminal as it is logged to the trail.log file)

### Setup

# Environmental Variables
Set up the following environmental variables required for the project:
MAIL_USERNAME: Email address used for sending notifications.
MAIL_PASSWORD: Password for the email account.
SECRET_KEY: A secret key for session management.
DATABASE_URL: The URL for the MySQL database connection.
# MySQL Connection
Install MySQL server and create a new database named _database.
Ensure the DATABASE_URL environmental variable is correctly configured to connect to your MySQL database.
# Superuser Setup
The default Superuser is set up with the email from the environmental variables.
The initial password for the Superuser is RandomPassword123.
After logging in, the Superuser can change their password, add new users (guards), add new clients, and their vehicles.
# External Camera Connection
Connect to an external camera for real-time video streaming.
Start the camera through the application interface and initiate the system to begin license plate recognition.
## Email Updates
Email updates are sent for every update made to clients' or guards' accounts.

### Technologies Used
Python
Flask
OpenCV
EasyOCR
SQLAlchemy
MySQL
