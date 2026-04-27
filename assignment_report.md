# Assignment Report

## Introduction
This submission contains a record label API, a Kong API gateway configuration, and a book information service implemented in REST, RPC, and GraphQL paradigms. The project is designed to be simple, academic, and fully runnable on a local machine.

## OpenAPI Explanation
The OpenAPI document describes the `Record Label API` with three endpoints: `GET /artists`, `POST /artists`, and `GET /artists/{artistname}`. It includes request parameters, response schemas, and HTTP Basic Authentication as the security requirement.

## Kong Setup Explanation
Kong is deployed in a Docker container in DB-less mode. The gateway is configured to proxy requests to the local FastAPI backend through the host gateway. Rate limiting and request size limiting are enabled using Kong plugins.

## API Implementations

### Record Label API
Implemented in `record-label-api/main.py` using FastAPI. It supports an in-memory dataset, pagination, HTTP Basic Authentication, and proper status codes.

### Book Info Service
Three separate Python modules are provided under `book-service`:
- `rest_api.py`: REST endpoints for `GET /books` and `GET /books/{id}`
- `rpc_api.py`: RPC endpoints for `POST /getBook` and `POST /createBook`
- `graphql_api.py`: GraphQL endpoint for `POST /graphql`
All three use the same dataset and return identical book information.

## Comparison Table: REST vs RPC vs GraphQL

| Feature | REST | RPC | GraphQL |
|---|---|---|---|
| Style | Resource-oriented | Method-oriented | Query-oriented |
| Flexibility | Moderate | Limited | High |
| Efficiency | Good for simple requests | Good for fixed operations | Excellent for selective fields |
| Complexity | Low | Low | Moderate |

## Screenshot Section

### Swagger UI
Open the record label API docs in a browser at `http://localhost:8000/docs`.

### GET/POST Requests
Use the provided curl examples to exercise `GET /artists`, `POST /artists`, and `GET /artists/{artistname}`.

### Kong Commands and Errors
Run Kong setup commands from the assignment instructions. Expected error responses include `429 Too Many Requests` after excessive calls and `413 Payload Too Large` for large POST bodies.

### REST, RPC, GraphQL Outputs
The Book Info Service returns identical data from each paradigm for the dataset entry `id=1`.

## Conclusion
This solution meets the assignment requirements with simple, maintainable code and clear documentation. The backend runs locally, Kong is configured with rate limiting and request size limiting, and the book service demonstrates three API paradigms with a shared dataset.
