import pytest
from processor import process_receipt

base_receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00",
        },
    ],
    "total": "35.35",
}


@pytest.mark.parametrize(
    "retailer, expected_points",
    [
        pytest.param("Target", 28, id="Baseline provided by Fetch"),
        pytest.param("Targe", 27, id="Valid alphanum with less characters"),
    ],
)
def test_process_receipt_varying_retailer(retailer, expected_points):
    receipt = base_receipt.copy()
    receipt["retailer"] = retailer
    assert process_receipt(receipt) == expected_points
