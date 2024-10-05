# NextCloud Calendar Manage API

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-yellow?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-green?logo=flask&logoColor=white)
![](https://img.shields.io/badge/CalDAV-green)
![](https://img.shields.io/badge/iCalendar-green)

![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white)
![NextCloud](https://img.shields.io/badge/NextCloud-blue?logo=nextcloud&logoColor=white)

## Overview

This project provides a REST API for manipulating NextCloud calendars using Flask, allowing you to retrieve, add, and delete NextCloud calendar events and check for the existence of events via the API. It is intended to be called from a script to be used to automatically add events to the calendar on a regular basis.

## Quick Start

### Option1: Running with Python

Install the required packages:
```bash
pip install -r requirements.txt
```

Set environment variables:

- `NEXTCLOUD_URL`: Your NextCloud URL.
- `NEXTCLOUD_USERNAME`: Your NextCloud username.
- `NEXTCLOUD_PASSWORD`: Your NextCloud password.
- `VERIFY_SSL`: Set to True to validate SSL certificates (if using a trusted certificate).

**Example:**
```bash
export NEXTCLOUD_URL='https://your_nextcloud_domain/remote.php/dav'
export NEXTCLOUD_USERNAME='your_username'
export NEXTCLOUD_PASSWORD='your_password'
export VERIFY_SSL='False'
```

Run the Flask application:
```bash
python app.py
```

### Option2: Running with Docker

Build the Docker image:
```bash
docker build -t nextcloud-calendar-api .
```

Run the Docker container:
```bash
docker run -d -p 5000:5000 \
  -e NEXTCLOUD_URL='https://<your_nextcloud_domain>/remote.php/dav' \
  -e NEXTCLOUD_USERNAME='<your_nextcloud_username>' \
  -e NEXTCLOUD_PASSWORD='<your_nextcloud_password>' \
  -e VERIFY_SSL='False' \
  nextcloud-flask-api
```

The API will be accessible at http://localhost:5000.


## API Reference
### 1. Get Calendars
- **Endpoint**: `/calendars`
- **Method**: `GET`
- **Description**: Retrieves a list of all calendars associated with the user.
- **Response**:
  - Success (200):
    ```json
    {
      "calendars": ["Calendar1", "Calendar2"]
    }
    ```
  - Error (500):
    ```json
    {
      "error": "Failed to retrieve calendars"
    }
    ```

### 2. Add Event
- **Endpoint**: `/add_event`
- **Method**: `POST`
- **Description**: Adds a new event to a specific calendar.
- **Request Body**:
  ```json
  {
    "calendar_name": "Calendar1",
    "start_time": "2024-10-05T09:00:00",
    "end_time": "2024-10-05T10:00:00",
    "summary": "Meeting",
    "description": "study session",
    "timezone": "Asia/Tokyo"
  }
- **Response**:
  - Success (200):
    ```json
    {
      "message": "Event added to Calendar1"
    }
    ```
  - Error (400):
    ```json
    {
      "error": "Invalid event data"
    }
    ```
  - Error (500):
    ```json
    {
      "error": "Failed to add event"
    }
    ```
### 3.Delete Event
- Endpoint: `/delete_event`
- Method: `DELETE`
- Description: Deletes an event from a specific calendar.
- **Request Body**:
  ```json
  {
    "calendar_name": "Calendar1",
    "summary": "Meeting"
  }
- **Response**:
  - Success (200):
    ```json
    {
      "message": "Event 'Meeting' deleted from Calendar1"
    }
    ```
  - Error (400):
    ```json
    {
      "error": "Failed to delete event"
    }
    ```
### 4. Get Events
- **Endpoint**: `/events`
- **Method**: `GET`
- **Description**: Retrieves all events from a specific calendar.
- **Query Parameters**:
  - `calendar_name`: The name of the calendar.
- **Response**:
  - Success (200):
    ```json
    {
      "events": ["Event1", "Event2"]
    }
    ```
  - Error (400):
    ```json
    {
      "error": "Failed to retrieve events"
    }
    ```
### 5. Event Exists
- **Endpoint**: `/event_exists`
- **Method**: `GET`
- **Description**: Checks if a specific event exists in a calendar.
- **Query Parameters**:
  - `calendar_name`: The name of the calendar.
  - `summary`: The summary of the event.
- **Response**:
  - Success (200):
    ```json
    {
      "exists": true
    }
    ```
  - Error (400):
    ```json
    {
      "error": "calendar_name and summary are required"
    }
    ```
  - Error (500):
    ```json
    {
      "error": "Failed to check if event exists"
    }
    ```
