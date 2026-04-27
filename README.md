# API-based-product

## Project Overview

This repository contains two independently runnable API services:

- `record_label_api`: a FastAPI-based Record Label API with Basic Authentication and OpenAPI 3.1.1 documentation.
- `book_service`: a shared book dataset exposed through REST, RPC, and GraphQL endpoints.

The project also includes Docker Compose support and Kong gateway setup instructions.

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

### Run the Record Label API

```bash
python main.py --service record_label_api --port 8002
```

- Swagger UI: `http://localhost:8002/docs`
- OpenAPI YAML: `http://localhost:8002/openapi.yaml`

### Run the Book Service

```bash
python main.py --service book_service --port 8003
```

- REST docs: `http://localhost:8003/docs`
- GraphQL playground: `http://localhost:8003/graphql`

## Docker Compose

Bring up all services with:

```bash
docker-compose up -d
```

Service endpoints:

- Record Label API: `http://localhost:8002`
- Book Service: `http://localhost:8003`
- Kong Proxy: `http://localhost:8000`
- Kong Admin: `http://localhost:8001`

## Record Label API

### Authentication

All endpoints require HTTP Basic Authentication:

- Username: `admin`
- Password: `admin123`

### Endpoints

- `GET /artists` — list artists with `offset` and `limit`
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

This service exposes a shared in-memory book dataset through multiple API paradigms.

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

Mutation example:

```graphql
mutation {
  createBook(title: "Foundation", author: "Isaac Asimov") {
    book {
      id
      title
      author
    }
  }
}
```

### Example Requests

REST list books:

```bash
curl http://localhost:8003/books
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

## Kong API Gateway Setup

Register the record label backend:

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=record-label-service" \
  --data "url=http://record_label_api:8002"
```

Create the proxy route:

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

Test through Kong:

```bash
curl -u admin:admin123 http://localhost:8000/record-label/artists
```

## API Style Comparison

| Paradigm | Endpoints | Strength | Best for |
| --- | --- | --- | --- |
| REST | `/books`, `/books/{id}` | Resource-driven, explicit HTTP semantics | Standard CRUD and API compatibility |
| RPC | `/getBook`, `/createBook`, `/updateBook` | Procedural, action-oriented | Simple command-style workflows |
| GraphQL | `/graphql` | Flexible client-driven field selection | UI-driven data fetching and minimizing roundtrips |

## Testing

Run tests with:

```bash
pytest
```

## Known Limitations

- In-memory storage means book and artist data do not persist across restarts.
- Kong DB-less mode configuration must be reapplied after container recreation.
- This sample is designed for local evaluation and demonstration rather than production persistence.
