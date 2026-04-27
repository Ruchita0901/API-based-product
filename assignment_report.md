# Assignment Report

## Introduction

This submission delivers a complete local API project with two independent services:

- `record_label_api`: a record label service with secure FastAPI endpoints and OpenAPI 3.1.1 documentation.
- `book_service`: a shared book dataset exposed by REST, RPC, and GraphQL.

The project is designed for evaluation clarity, developer usability, and a consistent experience across API styles.

## Architecture and Design

### Service separation

The project maintains clear separation of concerns:

- `record_label_api/` contains the record label FastAPI service and its OpenAPI specification.
- `book_service/` contains the shared book dataset plus REST, RPC, and GraphQL adapters.
- `main.py` is the root entry point for local service startup.

### Single entry point

A top-level `main.py` lets evaluators run either service with a single command,
while Docker Compose can start both services simultaneously.

## Record Label API

### API design

The record label API exposes three endpoints:

- `GET /artists` with pagination support via `offset` and `limit`
- `POST /artists` to create a new artist
- `GET /artists/{artistname}` to retrieve artists by their name, not by username

The API is secured with HTTP Basic Authentication and returns appropriate status codes:

- `200 OK` for successful reads
- `201 Created` for successful creation
- `400 Bad Request` for invalid input
- `401 Unauthorized` for failed authentication
- `404 Not Found` for missing artists

### OpenAPI integration

The `record_label_api/openapi.yaml` file is used directly by the API. FastAPI serves
OpenAPI through its docs and also exposes the raw YAML file at `/openapi.yaml`.
This ensures the spec is both valid and accessible.

## Book Service API Paradigms

### REST API

Implemented with full CRUD semantics:

- `GET /books`
- `GET /books/{id}`
- `POST /books`
- `PUT /books/{id}`
- `DELETE /books/{id}`

This service is ideal for standard HTTP-based resource operations.

### RPC API

The RPC layer supports method-style operations:

- `POST /getBook`
- `POST /createBook`
- `POST /updateBook`

RPC is useful for clients that prefer action-oriented interaction patterns.

### GraphQL API

GraphQL supports both queries and mutations with a single endpoint:

- Query book data with field selection
- Create new books with `createBook`

GraphQL is valuable when clients need flexible payload shapes and selective fields.

## Trade-offs: REST vs RPC vs GraphQL

- REST
  - Pros: standard HTTP semantics, easy caching, clear resources
  - Cons: fixed endpoints for each action
- RPC
  - Pros: direct action-based calls, simple payloads
  - Cons: less discoverable and less aligned with HTTP resource modeling
- GraphQL
  - Pros: flexible client-driven queries, fewer round trips
  - Cons: greater server complexity and more difficult caching

## Kong API Gateway

Kong runs in DB-less mode and proxies requests to the Record Label API.
The gateway demonstrates:

- service registration
- route creation
- rate limiting plugin
- request size limiting plugin

These features are documented with exact `curl` commands in the repository README.

## Testing

The project includes PyTest coverage for both services, verifying:

- record label authentication and artist endpoints
- book service REST CRUD behavior
- book service RPC operations
- book service GraphQL query and mutation

## Limitations

- Data is stored in-memory, so state is not persisted across restarts.
- Kong plugin configuration in DB-less mode must be reapplied if containers are recreated.
- This implementation is intended for evaluation and local demonstration.

## Conclusion

This repository is now structured for evaluation and developer use, with:

- a clear entry point,
- robust API implementations,
- full documentation,
- Docker Compose support,
- and unit tests.
