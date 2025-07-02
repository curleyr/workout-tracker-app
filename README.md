# Workout Tracker App (WIP)

A scalable, containerized workout tracker application where users can register, log in, search for exercises, and track their workouts and progress over time.

## Project Status

This project is a work-in-progress and actively being built. The backend is being architected first. The authentication and profile services are functional and form the foundation for secure user access and identity management. Future phases will include workout tracking, exercise search, and a React frontend.

## Architecture Overview

This app uses a **microservices architecture** to support modular growth and easy maintenance. Each service runs independently and communicates over internal Docker networking.

### Currently Implemented:

- **Auth Service**
- **Profile Service**

### Upcoming:

- Workout Logging Service
- Exercise Search Service
- React + TypeScript Frontend
- Analytics / Progress Dashboard

## Authentication Service & Flow

The authentication service loosely mimics the [Auth0](https://auth0.com) flow, issuing a JWT on login or token request. Tokens are used as Bearer tokens for authorization across services.

### Auth Endpoints

| Endpoint    | Method | Description                                       |
| ----------- | ------ | ------------------------------------------------- |
| `/register` | POST   | Registers a new user and creates a linked profile |
| `/login`    | POST   | Authenticates user credentials and returns a JWT  |
| `/token`    | POST   | Issues a token using `client_id`/`client_secret`  |

- Registration triggers a **POST** request to the `profile-service` to create the user profile.
- JWTs are signed and verified using utility functions.
- All services will validate tokens before processing protected requests.

## Profile Service

The profile service maintains user identity data (first name, last name, email).

### Profile Endpoints

| Endpoint  | Method | Description           |
| --------- | ------ | --------------------- |
| `/create` | POST   | Creates a new profile |

Profiles are created automatically during registration via an internal POST request from the auth service. Other routes to be built in a future phase.

## Tech Stack

- **Backend**: Python + Flask, using SQLAlchemy for ORM and PostgreSQL as the database
- **Microservices**: Auth + Profile services, each with its own PostgreSQL instance
- **Authentication**: Custom JWT-based bearer token flow
- **Containerization**: Docker + Docker Compose
- **Frontend (planned)**: TypeScript + React

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/curleyr/workout-tracker-app
   cd workout-tracker-app
   ```
2. Copy environment configs for each service within the individual microservices directories.

   ```bash
   cp .env.example .env
   ```

3. Build and start services:
   ```bash
   docker-compose up --build
   ```

## Postman Collection for Local Testing

A Postman collection is included at the root of the project to simplify local API testing for the Auth and Profile services.

- File: workout-tracker-app.local.postman_collection.json

Ensure your local services are running via Docker Compose before using the requests.
