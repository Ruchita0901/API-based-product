# Part 3 — Book Info Service (REST · RPC · GraphQL)

Single Node.js + Express server, shared in-memory book list, three paradigms.

## Run

```bash
npm install
npm start
# -> http://localhost:4000
```

## Try it

### REST
```bash
curl http://localhost:4000/books
curl http://localhost:4000/books/1
curl -X POST http://localhost:4000/books \
     -H "Content-Type: application/json" \
     -d '{"title":"Refactoring","author":"Martin Fowler","year":1999}'
```

### RPC
```bash
curl -X POST http://localhost:4000/rpc/getBook \
     -H "Content-Type: application/json" -d '{"id":1}'

curl -X POST http://localhost:4000/rpc/createBook \
     -H "Content-Type: application/json" \
     -d '{"title":"DDD","author":"Eric Evans","year":2003}'
```

### GraphQL
Open http://localhost:4000/graphql in a browser for GraphiQL, or:
```bash
curl -X POST http://localhost:4000/graphql \
     -H "Content-Type: application/json" \
     -d '{"query":"{ book(id:1) { title author year } }"}'
```

## Comparison of the three paradigms

| Aspect            | REST                                | RPC                                  | GraphQL                                  |
|-------------------|-------------------------------------|--------------------------------------|------------------------------------------|
| Style             | Resource-oriented (nouns + verbs)   | Action-oriented (procedures)         | Query language over a single endpoint    |
| URL shape         | Many URLs (`/books`, `/books/:id`)  | One URL per procedure                | Single `/graphql` endpoint               |
| HTTP semantics    | GET/POST/PUT/DELETE + status codes  | Usually all POST                     | Usually all POST                         |
| Over/under-fetch  | Fixed payload — common              | Fixed payload — common               | Client picks fields — neither            |
| Discoverability   | OpenAPI / HATEOAS                   | Custom docs (or proto IDL for gRPC)  | Self-describing schema + introspection   |
| Versioning        | URL/header (`/v2/books`)            | New procedure name                   | Schema evolves with deprecations         |
| Best for          | Public CRUD APIs                    | Internal service-to-service calls    | Aggregating data for varied UI clients   |

**Takeaway.** REST shines for resource CRUD and caching; RPC is the most natural
fit when you think in terms of actions/commands between trusted services;
GraphQL trades server complexity for client flexibility, eliminating
over-/under-fetching when many clients need different shapes of the same data.
