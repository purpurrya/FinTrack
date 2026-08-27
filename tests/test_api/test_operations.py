from decimal import Decimal


def test_add_expense_success(client, user, make_wallet):
    wallet = make_wallet()

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "test",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 200
    assert response.json()["wallet_id"] == wallet.id
    assert response.json()["type"] == "expense"
    assert Decimal(str(response.json()["amount"])) == Decimal("50.0")
    assert response.json()["category"] == "test"


def test_add_expense_negative_amount(client, user, make_wallet):
    make_wallet()

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -100.0,
            "description": "test",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 422


def test_add_expense_empty_name(client, user, make_wallet):
    make_wallet()

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": " ",
            "amount": -100.0,
            "description": "test",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 422


def test_add_expense_wallet_not_exists(client, user):
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "test",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 404


def test_add_expense_unathorized(client):
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -100.0,
            "description": "test",
        },
        headers={"Authorization": "Bearer notexists"},
    )

    assert response.status_code == 401


def test_add_expense_not_enough_money(client, user, make_wallet):
    make_wallet(balance=200)

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 250.0,
            "description": "test",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 400
