from cicd_demo.app import app


def test_index():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello from CI/CD", "version": "1.0"}


def test_health():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_unknown_route_returns_not_found():
    response = app.test_client().get("/missing")

    assert response.status_code == 404
