import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_inicio():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Tienda DevOps 2.0"}

def test_calcular_compra_valida():
    data = {"precio" : 100, "descuento": 10}
    response = client.post("/compra", json = data)
    assert response.status_code == 200
    assert response.json()["subtotal"] == pytest.approx(90.0)
    assert response.json()["total"] == pytest.approx(104.4)

def test_calcular_compra_precio_negativo():
    data = {"precio" : -100, "descuento": 10}
    response = client.post("/compra", json = data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Precio Inválido"

def test_calcular_compra_descuento_invalido():
    data = {"precio" : 100, "descuento": 150}
    response = client.post("/compra", json = data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Descuento Inválido"

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "1.1.0"

def test_revision():
    response = client.get("/revision")
    assert response.status_code == 200
    assert response.json()["estado"] == "ok"