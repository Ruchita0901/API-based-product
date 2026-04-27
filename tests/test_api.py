from fastapi.testclient import TestClient
from record_label_api.main import app as record_app
from book_service.app import app as book_app

record_client = TestClient(record_app)
book_client = TestClient(book_app)


def test_record_label_auth_required():
    response = record_client.get("/artists")
    assert response.status_code == 401


def test_record_label_list_artists():
    response = record_client.get("/artists?offset=0&limit=2", auth=("admin", "admin123"))
    assert response.status_code == 200
    payload = response.json()
    assert payload["limit"] == 2
    assert payload["total"] >= 3


def test_record_label_get_artist_by_name():
    response = record_client.get("/artists/The Rolling Stones", auth=("admin", "admin123"))
    assert response.status_code == 200
    assert response.json()["username"] == "rollingstones"


def test_book_rest_crud():
    response = book_client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    create_resp = book_client.post("/books", json={"title": "Dune", "author": "Frank Herbert"})
    assert create_resp.status_code == 201
    book_id = create_resp.json()["id"]

    update_resp = book_client.put(f"/books/{book_id}", json={"author": "F. Herbert"})
    assert update_resp.status_code == 200
    assert update_resp.json()["author"] == "F. Herbert"

    delete_resp = book_client.delete(f"/books/{book_id}")
    assert delete_resp.status_code == 204


def test_book_rpc_endpoints():
    create_resp = book_client.post("/createBook", json={"title": "Neuromancer", "author": "William Gibson"})
    assert create_resp.status_code == 201
    book_id = create_resp.json()["id"]

    get_resp = book_client.post("/getBook", json={"id": book_id})
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Neuromancer"


def test_book_graphql_query_and_mutation():
    query = {"query": "query { book(id: 1) { title author } }"}
    response = book_client.post("/graphql", json=query)
    assert response.status_code == 200
    assert response.json()["data"]["book"]["title"] == "1984"

    mutation = {"query": "mutation { createBook(title: \"Foundation\", author: \"Isaac Asimov\") { book { id title author } } }"}
    response = book_client.post("/graphql", json=mutation)
    assert response.status_code == 200
    assert response.json()["data"]["createBook"]["book"]["title"] == "Foundation"
