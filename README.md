# API Design Assignment 1

This repository contains solutions to the three parts of Assignment 1.

```
.
├── q1-openapi/              # Part 1 — OpenAPI 3.1.1 spec for a record label
│   └── record-label.yaml
├── q2-kong/                 # Part 2 — Kong rate limiting & request size limiting
│   ├── docker-compose.yml
│   └── README.md
├── q3-book-service/         # Part 3 — Book Info Service (REST + RPC + GraphQL)
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── README.md
```

## Part 1 — OpenAPI 3.1.1 (Record Label)

File: [q1-openapi/record-label.yaml](q1-openapi/record-label.yaml)

Defines:
- Basic authentication applied globally.
- `GET /artists` with `limit` and `offset` query params.
- `POST /artists` to create an artist.
- `GET /artists/{artistname}` to fetch a specific artist.
- Reusable `components.schemas` (`Artist`, `NewArtist`, `Error`).
- Status codes: `200`, `201`, `400`, `401`, `404`.

**Validate locally:**
```bash
npx @redocly/cli lint q1-openapi/record-label.yaml
# or paste into https://editor-next.swagger.io/
```

## Part 2 — Kong API Gateway (Rate + Request-Size Limiting)

Folder: [q2-kong/](q2-kong/)

DB-less Kong (declarative config) proxying to `httpbin.org`. Plugins:
- `rate-limiting` — 5 requests/minute.
- `request-size-limiting` — 1 KB max payload.

**Run:**
```bash
cd q2-kong
docker compose up -d
# Test rate limiting (6th call -> HTTP 429)
for i in 1 2 3 4 5 6; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/get; done
# Test size limit (HTTP 413)
curl -X POST http://localhost:8000/post -H "Content-Type: application/json" --data "$(head -c 2000 /dev/urandom | base64)"
```

## Part 3 — Book Info Service (REST / RPC / GraphQL)

Folder: [q3-book-service/](q3-book-service/)

A single Python Flask/FastAPI server exposing the same in-memory book data through three paradigms.

**Run:**
```bash
cd q3-book-service
pip install -r requirements.txt
python main.py
# Server: http://localhost:4000
```

**Endpoints:**

| Paradigm  | Example                                                                |
|-----------|------------------------------------------------------------------------|
| REST      | `GET http://localhost:4000/books` · `GET /books/1`                     |
| RPC       | `POST http://localhost:4000/rpc/getBook` body `{"id":1}`               |
| GraphQL   | `POST http://localhost:4000/graphql` body `{ "query": "{ book(id:1){title author} }" }` |

### Comparison of Paradigms

| Aspect            | REST                                | RPC                                  | GraphQL                                  |
|-------------------|-------------------------------------|--------------------------------------|------------------------------------------|
| Style             | Resource-oriented (nouns + verbs)   | Action-oriented (verbs/procedures)   | Query language over a single endpoint    |
| URL shape         | Many URLs (`/books`, `/books/1`)    | One URL per procedure                | Single `/graphql` endpoint               |
| HTTP semantics    | Uses GET/POST/PUT/DELETE + statuses | Usually all POST                     | Usually all POST                         |
| Over/under-fetch  | Fixed payload — common              | Fixed payload — common               | Client picks fields — neither            |
| Discoverability   | OpenAPI / HATEOAS                   | Custom docs or proto/IDL             | Self-describing schema + introspection   |
| Versioning        | URL or header (`/v2/books`)         | New procedure name                   | Schema evolves with deprecation          |
| Tooling           | Massive ecosystem                   | gRPC tooling strong; plain RPC weak  | Strong typed clients (Apollo, urql)      |
| Best for          | Public CRUD APIs                    | Internal service-to-service calls    | Aggregating data for varied UI clients   |
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
