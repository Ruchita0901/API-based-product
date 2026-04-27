from pathlib import Path
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import List

OPENAPI_YAML_PATH = Path(__file__).parent / "openapi.yaml"

app = FastAPI(
    title="Record Label API",
    description="A secure record label API with pagination and Basic Authentication.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)
security = HTTPBasic()

class Artist(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "The Rolling Stones"})
    genre: str = Field(..., json_schema_extra={"example": "Rock"})
    albums: int = Field(..., ge=0, json_schema_extra={"example": 30})
    username: str = Field(..., json_schema_extra={"example": "rollingstones"})

class ArtistList(BaseModel):
    total: int
    offset: int
    limit: int
    data: List[Artist]

artists = [
    {
        "name": "The Rolling Stones",
        "genre": "Rock",
        "albums": 30,
        "username": "rollingstones",
    },
    {
        "name": "Beyonce",
        "genre": "Pop",
        "albums": 7,
        "username": "beyonce",
    },
    {
        "name": "Daft Punk",
        "genre": "Electronic",
        "albums": 4,
        "username": "daftpunk",
    },
]


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    valid_username = secrets.compare_digest(credentials.username, "admin")
    valid_password = secrets.compare_digest(credentials.password, "admin123")
    if not (valid_username and valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/openapi.yaml", include_in_schema=False)
def openapi_yaml():
    return FileResponse(OPENAPI_YAML_PATH, media_type="application/yaml")


@app.get("/artists", response_model=ArtistList)
def get_artists(
    offset: int = 0,
    limit: int = 10,
    current_user: str = Depends(get_current_user),
):
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be 0 or greater")
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be 1 or greater")
    slice_end = offset + limit
    return {
        "total": len(artists),
        "offset": offset,
        "limit": limit,
        "data": artists[offset:slice_end],
    }


@app.post("/artists", status_code=status.HTTP_201_CREATED, response_model=Artist)
def create_artist(
    artist: Artist,
    current_user: str = Depends(get_current_user),
):
    existing = next(
        (
            item
            for item in artists
            if item["username"] == artist.username
            or item["name"].lower() == artist.name.lower()
        ),
        None,
    )
    if existing:
        raise HTTPException(status_code=400, detail="Artist with this name or username already exists")
    artists.append(artist.dict())
    return artist


@app.get("/artists/{artistname}", response_model=Artist)
def get_artist(
    artistname: str,
    current_user: str = Depends(get_current_user),
):
    artist = next(
        (item for item in artists if item["name"].lower() == artistname.lower()),
        None,
    )
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist
