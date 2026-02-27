# Rick and Morty Recruitment Backend

This project is a backend service that consumes the [Rick and Morty API](https://rickandmortyapi.com/documentation/) and provides additional endpoints:

- `/search` — combined search for characters, locations, and episodes by name
- `/top-pairs` — character pairs that appear together in the most episodes

The application is fully Dockerized and can run **without installing Python locally**.

---

##  Run the API

```bash
docker run -p 8000:8000 rm-python
```

The API will be available at [http://localhost:8000](http://localhost:8000)

##  Test endpoints in the browser or via curl

**Example `/search`:**

```bash
curl "http://localhost:8000/search?term=rick&limit=5"
```

**Example `/top-pairs`:**

```bash
curl "http://localhost:8000/top-pairs?min=10&limit=5"
```

**FastAPI interactive documentation (Swagger UI):**

[http://localhost:8000/docs](http://localhost:8000/docs)

**Redoc documentation:**

[http://localhost:8000/redoc](http://localhost:8000/redoc)

---

##  Running Unit Tests

All tests are included and run fully inside Docker.

**Build the Docker image (if not already built):**

```bash
docker build -t rm-python .
```

**Run tests:**

```bash
docker run rm-python pytest
```

Tests use mocked API calls, so they are fast and deterministic.

---

##  Example API Usage

### Search endpoint

`GET /search?term=rick&limit=3`

**Response:**

```json
[
  {
    "name": "Rick Sanchez",
    "type": "character",
    "url": "https://rickandmortyapi.com/api/character/1"
  },
  {
    "name": "Earth (C-137)",
    "type": "location",
    "url": "https://rickandmortyapi.com/api/location/1"
  }
]
```

### Top Pairs endpoint

`GET /top-pairs?min=10&limit=2`

**Response:**

```json
[
  {
    "character1": {
      "name": "Rick Sanchez",
      "url": "https://rickandmortyapi.com/api/character/1"
    },
    "character2": {
      "name": "Morty Smith",
      "url": "https://rickandmortyapi.com/api/character/2"
    },
    "episodes": 51
  }
]
```

---

##  Notes

- The API is implemented using **FastAPI** and **Python 3.11**
- Tests are written using **pytest** and mock the Rick and Morty API
- The Docker image can run both the API and tests
- `PYTHONPATH=/app` is set in Docker so tests can import the application properly
