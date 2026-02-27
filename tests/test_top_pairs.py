from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_top_pairs_basic(monkeypatch):
    def mock_get(url, params=None):
        class MockResponse:
            status_code = 200

            def json(self):
                if "episode" in url:
                    return {
                        "info": {"pages": 1},
                        "results": [
                            {
                                "characters": [
                                    "char1",
                                    "char2",
                                    "char3",
                                ]
                            }
                        ],
                    }
                else:
                    return {
                        "name": url,
                        "url": url,
                    }

            def raise_for_status(self):
                pass

        return MockResponse()

    import requests
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get("/top-pairs")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    assert data[0]["episodes"] == 1
    assert "character1" in data[0]
    assert "character2" in data[0]