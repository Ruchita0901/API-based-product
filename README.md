# API-based-product

## Overview

This repository contains two working backend projects:

- `record-label-api`: FastAPI Record Label API secured with Basic Authentication and documented with OpenAPI 3.1.1.
- `book_service`: single shared book dataset exposed through REST, RPC, and GraphQL paradigms.

It also includes a `docker-compose.yml` setup for Kong API Gateway.

## Requirements

- Python 3.12+
- `pip`
- `docker` and `docker-compose` (for Kong setup)

## Install

```bash
python -m pip install -r requirements.txt
```

## Run Locally

### Record Label API

```bash
uvicorn record-label-api.main:app --reload --host 0.0.0.0 --port 8000
```

Docs: `http://localhost:8000/docs`
OpenAPI schema: `http://localhost:8000/openapi.yaml`

### Book Info Service

```bash
uvicorn book_service.app:app --reload --host 0.0.0.0 --port 8002
```

Docs: `http://localhost:8002/docs`

## Record Label API

### Authentication

Use HTTP Basic Auth with credentials:

- username: `admin`
- password: `admin123`

### Endpoints

- `GET /artists` - paginated list of artists
- `POST /artists` - create a new artist
- `GET /artists/{artistname}` - get artist by name

### Sample Requests

List artists:

```bash
curl -u admin:admin123 "http://localhost:8000/artists?offset=0&limit=2"
```

Create artist:

```bash
curl -u admin:admin123 -H "Content-Type: application/json" \
  -d '{"name":"Adele","genre":"Pop","albums":4,"username":"adele"}' \
  http://localhost:8000/artists
```

Get artist by name:

```bash
curl -u admin:admin123 http://localhost:8000/artists/Adele
```

### Example Response

```json
{
  "name": "Adele",
  "genre": "Pop",
  "albums": 4,
  "username": "adele"
}
```

## Book Info Service

### REST

- `GET /books`
- `GET /books/{id}`

### RPC

- `POST /getBook` with JSON `{ "id": 1 }`
- `POST /createBook` with JSON `{ "title": "Dune", "author": "Frank Herbert" }`

### GraphQL

Query example:

```graphql
query {
  book(id: 1) {
    title
    author
  }
}
```

### Sample Requests

REST list books:

```bash
curl http://localhost:8002/books
```

RPC create book:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"Brave New World","author":"Aldous Huxley"}' \
  http://localhost:8002/createBook
```

GraphQL query:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"query { book(id: 1) { title author } }"}' \
  http://localhost:8002/graphql
```

## Kong API Gateway Setup

### Start services

```bash
docker-compose up -d
```

### Kong admin and proxy ports

- Proxy: `http://localhost:8000`
- Admin API: `http://localhost:8001`
- Direct backend: `http://localhost:8002`

### Register service

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=record-label-service" \
  --data "url=http://recordlabelapi:8000"
```

### Create route

```bash
curl -i -X POST http://localhost:8001/services/record-label-service/routes \
  --data "paths[]=/record-label" \
  --data "strip_path=false"
```

### Add rate limiting plugin

```bash
curl -i -X POST http://localhost:8001/services/record-label-service/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=5" \
  --data "config.policy=local"
```

### Add request size limiting plugin

```bash
curl -i -X POST http://localhost:8001/services/record-label-service/plugins \
  --data "name=request-size-limiting" \
  --data "config.allowed_payload_size=1048576"
```

### Test through Kong

```bash
curl -u admin:admin123 http://localhost:8000/record-label/artists
```

## REST vs RPC vs GraphQL

| Paradigm | Endpoint(s) | Payload Style | Use Case |
| --- | --- | --- | --- |
| REST | `GET /books`, `GET /books/{id}` | Resource-oriented, URL-based | Standard data retrieval and collection access |
| RPC | `POST /getBook`, `POST /createBook` | Action-oriented, method style | Remote procedure calls and command-style workflows |
| GraphQL | `POST /graphql` | Query language with fields selection | Flexible queries with client-controlled result shape |

## Notes

- `record-label-api/openapi.yaml` is valid OpenAPI 3.1.1 and matches the FastAPI schema.
- `record-label-api` requires Basic Authentication for all endpoints.
- `book_service` exposes all three paradigms from one shared dataset.
