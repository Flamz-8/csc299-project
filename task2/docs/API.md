# API Documentation for Task2 Study Planner App

## Overview

This document provides an overview of the API endpoints and their usage for the Task2 Study Planner App. The app includes features for managing tasks, tracking study sessions, and scheduling events.

## API Endpoints

### 1. Task Management

#### Create a Task

- **Endpoint:** `/api/tasks`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "title": "Task Title",
    "description": "Task Description",
    "due_date": "YYYY-MM-DD",
    "priority": "low|medium|high"
  }
  ```
- **Response:**
  - **201 Created**: Returns the created task object.
  - **400 Bad Request**: If the request body is invalid.

#### Get All Tasks

- **Endpoint:** `/api/tasks`
- **Method:** `GET`
- **Response:**
  - **200 OK**: Returns a list of all tasks.

#### Update a Task

- **Endpoint:** `/api/tasks/{id}`
- **Method:** `PUT`
- **Request Body:**
  ```json
  {
    "title": "Updated Task Title",
    "description": "Updated Task Description",
    "due_date": "YYYY-MM-DD",
    "priority": "low|medium|high",
    "completed": true|false
  }
  ```
- **Response:**
  - **200 OK**: Returns the updated task object.
  - **404 Not Found**: If the task with the specified ID does not exist.

#### Delete a Task

- **Endpoint:** `/api/tasks/{id}`
- **Method:** `DELETE`
- **Response:**
  - **204 No Content**: If the task was successfully deleted.
  - **404 Not Found**: If the task with the specified ID does not exist.

### 2. Study Session Tracking

#### Start a Study Session

- **Endpoint:** `/api/study-sessions/start`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "task_id": "Task ID",
    "duration": "Duration in minutes"
  }
  ```
- **Response:**
  - **200 OK**: Returns the study session details including a timer.
  - **400 Bad Request**: If the request body is invalid.

#### End a Study Session

- **Endpoint:** `/api/study-sessions/end`
- **Method:** `POST`
- **Response:**
  - **200 OK**: Returns the summary of the completed study session.

### 3. Calendar Management

#### Get Calendar Events

- **Endpoint:** `/api/calendar/events`
- **Method:** `GET`
- **Response:**
  - **200 OK**: Returns a list of calendar events.

#### Add Calendar Event

- **Endpoint:** `/api/calendar/events`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "title": "Event Title",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "description": "Event Description"
  }
  ```
- **Response:**
  - **201 Created**: Returns the created event object.
  - **400 Bad Request**: If the request body is invalid.

## Conclusion

This API documentation provides a comprehensive overview of the endpoints available in the Task2 Study Planner App. For further details on usage and examples, please refer to the README.md file in the project.