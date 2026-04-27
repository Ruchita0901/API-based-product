# API-based-product

## Project Overview

API-based-product demonstrates a polished, evaluator-ready backend submission with two services:

- `record_label_api`: a secure Record Label API with OpenAPI 3.1.1 and Swagger UI.
- `book_service`: a book information service exposed with REST, RPC, and GraphQL.

This repository includes Docker Compose support, Kong gateway documentation, and automated tests.

## Features

- REST CRUD endpoints for books
- RPC-style book operations
- GraphQL query and mutation support
- Secured artist management API with Basic Auth
- OpenAPI YAML specification served at `/openapi.yaml`
- Swagger UI available at `/docs`
- Docker Compose orchestration with Kong gateway
- Tested with PyTest

## Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- Graphene / GraphQL
- Kong API Gateway
- Docker Compose
- PyTest

## Folder Structure

```text
API-based-product/
├── book_service/
│   ├── app.py
│   ├── data.py
│   ├── graphql_api.py
│   ├── rest_api.py
│   └── rpc_api.py
├── record_label_api/
│   ├── main.py
│   └── openapi.yaml
├── tests/
│   └── test_api.py
├── docker-compose.yml
├── main.py
├── README.md
├── assignment_report.md
└── requirements.txt
```

## Prerequisites

- Python 3.12+
- pip
- Docker
- docker-compose

## Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running Locally

### Start the Record Label API

```bash
python main.py --service record_label_api --port 8002
```

- Swagger UI: `http://localhost:8002/docs`
- OpenAPI YAML: `http://localhost:8002/openapi.yaml`
- Health check: `http://localhost:8002/`

### Start the Book Service

```bash
python main.py --service book_service --port 8003
```

- REST docs: `http://localhost:8003/docs`
- GraphQL playground: `http://localhost:8003/graphql`

## Run with Docker Compose

Start both services and Kong:

```bash
docker-compose up -d
```

Endpoints:

- Record Label API: `http://localhost:8002`
- Book Service: `http://localhost:8003`
- Kong Proxy: `http://localhost:8000`
- Kong Admin: `http://localhost:8001`

## Record Label API

### Authentication

All Record Label endpoints require HTTP Basic Authentication:

- Username: `admin`
- Password: `admin123`

### Endpoints

- `GET /artists` — list artists with pagination using `offset` and `limit`
- `POST /artists` — create a new artist
- `GET /artists/{artistname}` — retrieve an artist by name

### Example Requests

List artists:

```bash
curl -u admin:admin123 "http://localhost:8002/artists?offset=0&limit=2"
```

Create an artist:

```bash
curl -u admin:admin123 -H "Content-Type: application/json" \
  -d '{"name":"Adele","genre":"Pop","albums":4,"username":"adele"}' \
  http://localhost:8002/artists
```

Get artist by name:

```bash
curl -u admin:admin123 http://localhost:8002/artists/Adele
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

## Book Service

The Book Service uses a shared in-memory dataset for the same data across REST, RPC, and GraphQL.

### REST Endpoints

- `GET /books`
- `GET /books/{id}`
- `POST /books`
- `PUT /books/{id}`
- `DELETE /books/{id}`

### RPC Endpoints

- `POST /getBook`
- `POST /createBook`
- `POST /updateBook`

### GraphQL Endpoint

- `POST /graphql`

### Example Requests

REST list books:

```bash
curl http://localhost:8003/books
```

REST create book:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"Dune","author":"Frank Herbert"}' \
  http://localhost:8003/books
```

RPC get book:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"id": 1}' \
  http://localhost:8003/getBook
```

GraphQL query:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"query { book(id: 1) { title author } }"}' \
  http://localhost:8003/graphql
```

GraphQL mutation:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"mutation { createBook(title: \"Foundation\", author: \"Isaac Asimov\") { book { id title author } } }"}' \
  http://localhost:8003/graphql
```

## Kong API Gateway Setup

Register the Record Label service:

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=record-label-service" \
  --data "url=http://record_label_api:8002"
```

Create the Kong route:

```bash
curl -i -X POST http://localhost:8001/services/record-label-service/routes \
  --data "paths[]=/record-label" \
  --data "strip_path=false"
```

Add rate limiting:

```bash
curl -i -X POST http://localhost:8001/services/record-label-service/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=5" \
  --data "config.policy=local"
```

Add request size limiting:

```bash
curl -i -X POST http://localhost:8001/services/record-label-service/plugins \
  --data "name=request-size-limiting" \
  --data "config.allowed_payload_size=1048576"
```

Test via Kong:

```bash
curl -u admin:admin123 http://localhost:8000/record-label/artists
```

## Example Responses

REST list books response:

```json
[
  {"id": 1, "title": "1984", "author": "George Orwell"}
]
```

RPC getBook response:

```json
{
  "id": 1,
  "title": "1984",
  "author": "George Orwell"
}
```

GraphQL response:

```json
{
  "data": {
    "book": {
      "title": "1984",
      "author": "George Orwell"
    }
  }
}
```

## Testing

Run tests with:

```bash
pytest tests/test_api.py -q
```

## Known Limitations

- Data is stored in-memory and not persisted across restarts.
- Kong DB-less mode requires plugins to be reapplied after container recreation.
- This implementation is meant for local evaluation and demonstration.
