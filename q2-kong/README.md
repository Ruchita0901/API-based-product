# Part 2 — Kong: Rate Limiting & Request Size Limiting

DB-less Kong with a declarative config. Proxies all requests to `httpbin.org`
and applies two plugins:

- **rate-limiting** — `5 requests per minute` (per consumer/IP, local policy).
- **request-size-limiting** — payload capped at `1 KB`.

## Run

```bash
docker compose up -d
```

Kong proxy listens on `http://localhost:8000`, admin API on `http://localhost:8001`.

## Verify

### Rate limit (HTTP 429 on 6th call)
```bash
for i in 1 2 3 4 5 6; do
  curl -s -o /dev/null -w "Request $i -> %{http_code}\n" http://localhost:8000/get
done
```
Expected: first 5 return `200`, the 6th returns `429 Too Many Requests`.
Response headers also include `X-RateLimit-Limit-Minute: 5` and `X-RateLimit-Remaining-Minute`.

### Request size limit (HTTP 413)
```bash
# Small payload — succeeds
curl -i -X POST http://localhost:8000/post \
     -H "Content-Type: application/json" \
     -d '{"hello":"world"}'

# > 1 KB — rejected with 413
curl -i -X POST http://localhost:8000/post \
     -H "Content-Type: application/json" \
     --data "$(printf 'x%.0s' {1..2000})"
```

## Stop
```bash
docker compose down
```
