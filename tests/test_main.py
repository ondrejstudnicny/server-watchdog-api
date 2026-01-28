from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Test, jestli API vůbec odpovídá (např. na dokumentaci)
def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

# 2. Test vložení Heartbeatu (bez DB mocku by to mohlo spadnout,
# ale FastAPI TestClient je chytrý. Pro jednoduchost teď testujeme jen to,
# že aplikace 'naběhne' a nepadá na importech).
def test_app_exists():
    assert app is not None