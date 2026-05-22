import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def make_session():
    session = MagicMock()
    session.id          = uuid4()
    session.title       = "Intro a Python"
    session.description = "Una charla genial"
    session.starts_at   = datetime.now()
    session.capacity    = 50
    session.created     = datetime.now()
    session.modified    = datetime.now()
    session.speakers    = []
    track = MagicMock()
    track.id   = uuid4()
    track.name = "Backend"
    track.created  = datetime.now()
    track.modified = datetime.now()
    conference = MagicMock()
    conference.id          = uuid4()
    conference.name        = "PyCon 2025"
    conference.description = ""
    conference.starts_at   = datetime.now()
    conference.ends_at     = datetime.now()
    conference.created     = datetime.now()
    conference.modified    = datetime.now()
    track.conference = conference
    session.track    = track
    return session


def test_health():
    # El endpoint /healthz tiene que devolver 200
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_sessions_returns_200():
    with patch('routers.sessions.get_service') as mock_service, \
         patch('routers.sessions.cache_get', return_value=None), \
         patch('routers.sessions.cache_set'):
        mock_service.return_value.get_all.return_value = [make_session()]
        response = client.get("/api/v1/sessions/")
        assert response.status_code == 200


def test_get_session_not_found():
    with patch('routers.sessions.get_service') as mock_service, \
         patch('routers.sessions.cache_get', return_value=None):
        mock_service.return_value.get_by_id.return_value = None
        response = client.get(f"/api/v1/sessions/{uuid4()}")
        assert response.status_code == 404


def test_search_sessions():
    with patch('routers.sessions.get_service') as mock_service:
        mock_service.return_value.search.return_value = [make_session()]
        response = client.get("/api/v1/sessions/search/?query=python")
        assert response.status_code == 200


def test_availability_not_found():
    with patch('routers.sessions.get_service') as mock_service, \
         patch('routers.sessions.cache_get', return_value=None):
        mock_service.return_value.get_availability.return_value = None
        response = client.get(f"/api/v1/sessions/{uuid4()}/availability/")
        assert response.status_code == 404


def test_cache_hit_returns_cached_data():
    cached = [{"id": str(uuid4()), "title": "cached", "starts_at": str(datetime.now()), "capacity": 10}]
    with patch('routers.sessions.cache_get', return_value=cached):
        response = client.get("/api/v1/sessions/")
        assert response.status_code == 200
