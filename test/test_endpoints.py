from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_pdf():
    payload = {
        "nombre": "Leonel",
        "apellido": "Garcia",
        "edad": "29",
        "telefono": "1234567890",
        "correo": "leonel@example.com"
    }

    response = client.post("/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "document_code" in data
    assert len(data["document_code"]) == 10

def test_get_pdf():
    # Generar un PDF primero
    payload = {
        "nombre": "Leonel",
        "apellido": "Garcia",
        "edad": "29",
        "telefono": "1234567890",
        "correo": "leonel@example.com"
    }
    create_response = client.post("/create", json=payload)
    document_code = create_response.json()["document_code"]

    # Recuperar el PDF
    response = client.get(f"/document/{document_code}")

    # Verificar el código de estado
    assert response.status_code == 200

    # Verificar el contenido de la respuesta
    data = response.json()
    assert data["success"] is True
    assert "document_b64" in data
    assert isinstance(data["document_b64"], str)
    
def test_get_pdf_not_found():
    # Usar un código inexistente
    response = client.get("/document/INVALIDCODE")

    # Verificar el código de estado
    assert response.status_code == 200

    # Verificar el contenido de la respuesta
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Documento no encontrado"