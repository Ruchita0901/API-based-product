# Part 1 — OpenAPI 3.1.1 (Record Label)

OpenAPI 3.1.1 specification for a secure Record Label API with artist management.

## Overview

The `record-label.yaml` file defines a RESTful API for managing artists with:
- **Authentication**: Basic Auth applied globally to all endpoints
- **Resources**: Artist management (list, create, retrieve by name)
- **Query Parameters**: Pagination support with `limit` and `offset`
- **Status Codes**: Comprehensive error and success responses (`200`, `201`, `400`, `401`, `404`)
- **Reusable Schemas**: Standardized request/response components

## File Structure

```
record-label.yaml    # Complete OpenAPI 3.1.1 specification
```

## API Endpoints

### GET /artists
Retrieve a list of artists with pagination.

**Query Parameters:**
- `limit` (integer, optional): Number of results to return (default: 10)
- `offset` (integer, optional): Number of results to skip (default: 0)

**Response:** `200 OK`
```json
{
  "artists": [
    {
      "name": "The Beatles",
      "genre": "Rock",
      "foundedYear": 1960
    }
  ]
}
```

---

### POST /artists
Create a new artist.

**Request Body:**
```json
{
  "name": "The Beatles",
  "genre": "Rock",
  "foundedYear": 1960
}
```

**Response:** `201 Created`
```json
{
  "id": "artist-123",
  "name": "The Beatles",
  "genre": "Rock",
  "foundedYear": 1960
}
```

---

### GET /artists/{artistname}
Retrieve a specific artist by name.

**Path Parameters:**
- `artistname` (string, required): The artist's name

**Response:** `200 OK`
```json
{
  "id": "artist-123",
  "name": "The Beatles",
  "genre": "Rock",
  "foundedYear": 1960
}
```

## Authentication

All endpoints require **Basic Authentication**. Include the `Authorization` header:

```bash
curl -H "Authorization: Basic base64(username:password)" http://localhost/artists
```

Example with credentials `admin:secret`:
```bash
Authorization: Basic YWRtaW46c2VjcmV0
```

## Error Responses

### 400 Bad Request
Invalid input or malformed request.

```json
{
  "error": "Bad Request",
  "message": "Invalid artist data"
}
```

### 401 Unauthorized
Missing or invalid authentication credentials.

```json
{
  "error": "Unauthorized",
  "message": "Invalid credentials"
}
```

### 404 Not Found
Artist not found.

```json
{
  "error": "Not Found",
  "message": "Artist not found"
}
```

## Validation

### Validate the spec locally

Using **Redocly CLI**:
```bash
npx @redocly/cli lint record-label.yaml
```

Using **Swagger Editor**:
Paste the YAML content into https://editor-next.swagger.io/

### Generate API Documentation

View the spec in **Swagger UI** or **ReDoc**:
```bash
# Using a local Swagger UI server
docker run -p 80:8080 -e SWAGGER_JSON=/spec/record-label.yaml -v $(pwd):/spec swaggerapi/swagger-ui
```

## Reusable Components

The spec defines reusable schemas under `components.schemas`:

- **Artist**: Full artist object with all fields
- **NewArtist**: Artist creation request (without `id`)
- **Error**: Standard error response format

## Testing

### Test with curl

**List artists:**
```bash
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" http://localhost:8000/artists
```

**Create an artist:**
```bash
curl -X POST http://localhost:8000/artists \
  -H "Authorization: Basic YWRtaW46c2VjcmV0" \
  -H "Content-Type: application/json" \
  -d '{"name":"Pink Floyd","genre":"Rock","foundedYear":1965}'
```

**Get a specific artist:**
```bash
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" http://localhost:8000/artists/Pink%20Floyd
```

## Pagination Example

Retrieve 5 artists, skipping the first 10:

```bash
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" \
  'http://localhost:8000/artists?limit=5&offset=10'
```

## More Information

- [OpenAPI 3.1.1 Specification](https://spec.openapis.org/oas/v3.1.1)
- [Swagger Editor](https://editor.swagger.io/)
- [Redocly CLI](https://redocly.com/docs/cli/)
