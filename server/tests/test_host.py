"""Tests endpoint performance in accordance with the provided
api contract."""
from host import app
from copy import deepcopy
import pytest
from flask import jsonify

# Valid receipt that will be used for several tests, including
# being injected with new fields
VALID_RECEIPT = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
        "shortDescription": "Mountain Dew 12PK",
        "price": "6.49"
        },{
        "shortDescription": "Emils Cheese Pizza",
        "price": "12.25"
        },{
        "shortDescription": "Knorr Creamy Chicken",
        "price": "1.26"
        },{
        "shortDescription": "Doritos Nacho Cheese",
        "price": "3.35"
        },{
        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
        "price": "12.00"
        }
    ],
    "total": "35.35"
}

#   ===== Testing valid usage =====

# Lots of testcases here to inject different fields
@pytest.mark.parametrize(
    "validReceipt",
    [
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "retailer": "T"},
            id="retailer single char"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "retailer": "&-_  "},
            id="retailer with special characters"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "retailer": "  Store Name  "},
            id="retailer with leading and trailing spaces"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseDate": "2022-12-31"},
            id="purchaseDate end of year"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseTime": "00:00"},
            id="purchaseTime start of day"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseTime": "23:59"},
            id="purchaseTime end of day"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "---", "price": "19.99"}]},
            id="item description with dash"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Item", "price": "09.99"}]},
            id="price with leading zero"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Item", "price": "10.00"}]},
            id="price at a round number"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Item", "price": "10000.00"}]},
            id="price with large amount"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "total": "10000.00"},
            id="total with large amount"
        ),
    ]
)
def test_receipts_process_valid_receipt(validReceipt):
    with app.test_client() as server:
        response = server.post(f'/receipts/process', json=validReceipt)
        assert response.status_code == 200
        response_json = response.get_json()
        assert "id" in response_json


def test_endpoint_integration_valid_receipt():
    """Tests end-to-end usage of the webservice"""
    with app.test_client() as server:
        # Post valid receipt
        response = server.post(f'/receipts/process', json=VALID_RECEIPT)
        assert response.status_code == 200
        response_json = response.get_json()
        assert "id" in response_json

        ID = response_json["id"]
        response = server.get(f'receipts/{ID}/points')
        assert response.status_code == 200
        response_json = response.get_json()
        assert "points" in response_json


#   ===== Tesing inappropriate usage =====

# Lots of testcases here to inject invalid receipt fields
@pytest.mark.parametrize(
    "invalidReceipt",
    [
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "retailer": ""},
            id="empty retailer"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "retailer": "Invalid*Store!"},
            id="retailer invalid characters"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseDate": "01-01-2022"},
            id="purchaseDate invalid format"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseDate": "2022-02-30"},
            id="purchaseDate non-existent date"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseTime": "1:01 PM"},
            id="purchaseTime invalid format"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "purchaseTime": "25:01"},
            id="purchaseTime out of range"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": []},
            id="empty items list"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": "not a list"},
            id="items non-list type"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "", "price": "6.49"}]},
            id="shortDescription empty string"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Invalid*Description!", "price": "6.49"}]},
            id="shortDescription invalid characters"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6."}]},
            id="price missing cents"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Mountain Dew 12PK", "price": "ABC"}]},
            id="price non-numeric characters"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6.999"}]},
            id="price extra decimals"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "total": "35."},
            id="total missing cents"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "total": "35.355"},
            id="total extra decimals"
        ),
        pytest.param(
            {**deepcopy(VALID_RECEIPT), "total": "35.AB"},
            id="total non-numeric characters"
        ),
    ]
)
def test_receipts_process_invalid_receipt(invalidReceipt):
    with app.test_client() as server:
        response = server.post(f'/receipts/process', json=invalidReceipt)
        assert response.status_code == 400
        assert response.data == b"The receipt is invalid"

def test_receipts_process_invalid_method():
    with app.test_client() as server:
        response = server.get(f'/receipts/process')
        assert response.status_code == 405

def test_receipts_points_invalid_id():
    with app.test_client() as server:
        ID = "2c37898a-dc27-56ac-b9d4-cb755b426579"
        response = server.get(f'/receipts/{ID}/points')
        assert response.status_code == 404
        assert response.data == b"No receipt found for that id"

def test_receipts_points_invalid_method():
    with app.test_client() as server:
        ID = "2c37898a-dc27-56ac-b9d4-cb755b426579"
        response = server.post(f'/receipts/{ID}/points')
        assert response.status_code == 405