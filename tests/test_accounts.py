import pytest
from fastapi.testclient import TestClient

VALID_ACCOUNT = {
    "owner_name": "Иван Иванов",
    "account_number": "RU123456789012345678",
    "balance": 1000.0,
    "currency": "RUB",
    "account_type": "checking",
}


class TestCreateAccount:
    def test_create_account_success(self, client: TestClient):
        response = client.post("/accounts/", json=VALID_ACCOUNT)
        assert response.status_code == 201
        data = response.json()
        assert data["owner_name"] == "Иван Иванов"
        assert data["account_number"] == "RU123456789012345678"
        assert data["balance"] == 1000.0
        assert data["currency"] == "RUB"
        assert data["is_active"] is True
        assert "id" in data

    def test_create_account_duplicate_number(self, client: TestClient):
        client.post("/accounts/", json=VALID_ACCOUNT)
        response = client.post("/accounts/", json=VALID_ACCOUNT)
        assert response.status_code == 409

    def test_create_account_invalid_number_format(self, client: TestClient):
        data = {**VALID_ACCOUNT, "account_number": "invalid"}
        response = client.post("/accounts/", json=data)
        assert response.status_code == 422

    def test_create_account_negative_balance(self, client: TestClient):
        data = {**VALID_ACCOUNT, "balance": -100.0}
        response = client.post("/accounts/", json=data)
        assert response.status_code == 422

    def test_create_account_empty_owner(self, client: TestClient):
        data = {**VALID_ACCOUNT, "owner_name": "   "}
        response = client.post("/accounts/", json=data)
        assert response.status_code == 422

    def test_create_account_invalid_currency(self, client: TestClient):
        data = {**VALID_ACCOUNT, "account_number": "RU111111111111111111", "currency": "JPY"}
        response = client.post("/accounts/", json=data)
        assert response.status_code == 422

    def test_create_account_default_balance(self, client: TestClient):
        data = {k: v for k, v in VALID_ACCOUNT.items() if k != "balance"}
        data["account_number"] = "RU999999999999999999"
        response = client.post("/accounts/", json=data)
        assert response.status_code == 201
        assert response.json()["balance"] == 0.0


class TestGetAccount:
    def test_get_account_success(self, client: TestClient):
        created = client.post("/accounts/", json=VALID_ACCOUNT).json()
        response = client.get(f"/accounts/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_get_account_not_found(self, client: TestClient):
        response = client.get("/accounts/99999")
        assert response.status_code == 404

    def test_get_account_invalid_id(self, client: TestClient):
        response = client.get("/accounts/abc")
        assert response.status_code == 422


class TestListAccounts:
    def test_list_empty(self, client: TestClient):
        response = client.get("/accounts/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_multiple(self, client: TestClient):
        accounts = [
            {**VALID_ACCOUNT, "account_number": f"RU{str(i).zfill(18)}"}
            for i in range(3)
        ]
        for acc in accounts:
            client.post("/accounts/", json=acc)
        response = client.get("/accounts/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_list_pagination(self, client: TestClient):
        for i in range(5):
            client.post("/accounts/", json={**VALID_ACCOUNT, "account_number": f"RU{str(i).zfill(18)}"})
        response = client.get("/accounts/?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestUpdateAccount:
    def test_update_account_success(self, client: TestClient):
        created = client.post("/accounts/", json=VALID_ACCOUNT).json()
        response = client.put(f"/accounts/{created['id']}", json={"balance": 5000.0, "is_active": False})
        assert response.status_code == 200
        data = response.json()
        assert data["balance"] == 5000.0
        assert data["is_active"] is False

    def test_update_account_not_found(self, client: TestClient):
        response = client.put("/accounts/99999", json={"balance": 100.0})
        assert response.status_code == 404

    def test_update_account_partial(self, client: TestClient):
        created = client.post("/accounts/", json=VALID_ACCOUNT).json()
        response = client.put(f"/accounts/{created['id']}", json={"owner_name": "Пётр Петров"})
        assert response.status_code == 200
        assert response.json()["owner_name"] == "Пётр Петров"
        assert response.json()["balance"] == VALID_ACCOUNT["balance"]

    def test_update_account_negative_balance(self, client: TestClient):
        created = client.post("/accounts/", json=VALID_ACCOUNT).json()
        response = client.put(f"/accounts/{created['id']}", json={"balance": -1.0})
        assert response.status_code == 422


class TestDeleteAccount:
    def test_delete_account_success(self, client: TestClient):
        created = client.post("/accounts/", json=VALID_ACCOUNT).json()
        response = client.delete(f"/accounts/{created['id']}")
        assert response.status_code == 200
        get_response = client.get(f"/accounts/{created['id']}")
        assert get_response.status_code == 404

    def test_delete_account_not_found(self, client: TestClient):
        response = client.delete("/accounts/99999")
        assert response.status_code == 404
