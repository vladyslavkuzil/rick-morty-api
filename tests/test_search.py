from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_search_returns_results(monkeypatch):
    def mock_get(url, params=None):
        class MockResponse:
            status_code = 200

            def json(self):
                return {
                    "results": [
                        {"name": "Rick Sanchez", "url": "url1"}
                    ]
                }

            def raise_for_status(self):
                pass

        return MockResponse()

    import requests
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get("/search?term=rick")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3  
    assert data[0]["name"] == "Rick Sanchez"
    assert "type" in data[0]
    assert "url" in data[0]


def test_search_limit(monkeypatch):
    def mock_get(url, params=None):
        class MockResponse:
            status_code = 200

            def json(self):
                return {
                    "results": [
                        {"name": "Rick Sanchez", "url": "url1"}
                    ]
                }

            def raise_for_status(self):
                pass

        return MockResponse()

    import requests
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get("/search?term=rick&limit=1")
    data = response.json()
    assert len(data) == 1