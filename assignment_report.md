# Assignment Report

## Introduction

This project provides a professional API submission with two separate services:

- `record_label_api` for artist management.
- `book_service` for book information across REST, RPC, and GraphQL.

It emphasizes evaluator clarity, simple setup, and consistent API behavior.

## Architecture Overview

The codebase is composed of two FastAPI services plus a shared root entry point:

- `record_label_api/` contains the Record Label service and the OpenAPI 3.1.1 YAML document.
- `book_service/` contains the shared dataset with REST, RPC, and GraphQL adapters.
- `main.py` is a single startup entry point that launches either service.

Docker Compose supports launching both services together with Kong as an API gateway.

## Design Decisions

### Why REST, RPC, and GraphQL?

- REST is used for predictable, resource-oriented book management.
- RPC is used for action-based book operations that are easy to reason about.
- GraphQL is used for flexible client-driven queries and a single unified endpoint.

These styles demonstrate the trade-offs between explicit resources, procedural commands, and flexible schema-driven queries.

### Why in-memory storage?

In-memory storage keeps setup simple and makes the service easy to evaluate. The trade-off is that state does not persist across restarts, which is acceptable for a demo project.

## Record Label API

### API contract

Endpoints:

- `GET /artists` — paginated list of artists using `offset` and `limit`
- `POST /artists` — create a new artist
- `GET /artists/{artistname}` — retrieve an artist by name

Security:

- HTTP Basic Authentication with `admin` / `admin123`

Response handling:

- `200 OK` for successful retrievals
- `201 Created` for successful creation
- `400 Bad Request` for invalid parameters
- `401 Unauthorized` for incorrect credentials
- `404 Not Found` for missing artists

### OpenAPI and Swagger

The existing `record_label_api/openapi.yaml` is served at `/openapi.yaml` and is consumed by Swagger UI at `/docs`.
This provides a direct, evaluator-friendly API documentation experience.

## Book Service API Paradigms

### REST

The REST API supports full CRUD operations on books and is ideal for standard resource-based workflows.

### RPC

The RPC endpoints expose operation-focused actions and are useful when the client expects method-like behavior.

### GraphQL

GraphQL provides a flexible query interface, allowing clients to request exactly the fields they need and use a single endpoint.

## Trade-offs and Observations

| Style | Strengths | Best use case |
|---|---|---|
| REST | Clear resource semantics and predictable URLs | Standard CRUD APIs |
| RPC | Simple, action-oriented payloads | Command-style service interactions |
| GraphQL | Flexible field selection and single endpoint | UI-driven data fetching and variable query shapes |

## Docker and Deployment

Docker Compose runs the Record Label API, Book Service, and Kong gateway together. The gateway is configured for proxying and plugin management with commands provided in the README.

## Limitations

- Data is stored only in memory and resets on each service restart.
- Kong DB-less mode requires plugin reconfiguration after containers are recreated.
- This project is structured for demonstration and local evaluation, not long-term production persistence.

## Conclusion

The repository now offers a complete evaluator-ready submission with:

- secure and documented APIs
- a single entry point and Docker Compose support
- multiple API paradigms with consistent shared data
- clear documentation, example commands, and tests
