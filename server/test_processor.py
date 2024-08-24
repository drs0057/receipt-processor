import math
from typing import Any, Dict, List

import pytest
from processor import (
    ALPHANUMERIC_POINTS,
    DESC_MULTIPLIER,
    MULTIPLE_TOTAL_POINTS,
    ODD_PURCHASE_DATE_POINTS,
    PAIR_OF_ITEMS_POINTS,
    PURCHASE_TIME_POINTS,
    ROUND_TOTAL_POINTS,
    calculate_item_desc_points,
    calculate_item_pairs_points,
    calculate_purchase_date_points,
    calculate_purchase_time_points,
    calculate_retailer_points,
    calculate_total_points,
)

#   ===== Testing retailer name =====


@pytest.mark.parametrize(
    "retailer, expectedPoints",
    [
        pytest.param(
            "Target", ALPHANUMERIC_POINTS * 6, id="Baseline retailer"
        ),
        pytest.param("Targe", ALPHANUMERIC_POINTS * 5, id="Chars"),
        pytest.param("T", ALPHANUMERIC_POINTS * 1, id="Char"),
        pytest.param(
            "Made up realtor", ALPHANUMERIC_POINTS * 13, id="Chars and spaces"
        ),
        pytest.param(
            "Target123", ALPHANUMERIC_POINTS * 9, id="Chars and numbers"
        ),
        pytest.param(
            "12 12", ALPHANUMERIC_POINTS * 4, id="Numbers and spaces"
        ),
        pytest.param("   ", ALPHANUMERIC_POINTS * 0, id="Spaces"),
        pytest.param("123", ALPHANUMERIC_POINTS * 3, id="Numbers"),
        pytest.param(
            "_-&",
            ALPHANUMERIC_POINTS * 0,
            id="Chars that the API allows but are nonalphanumeric",
        ),
    ],
)
def test_calculate_retailer_points(retailer: str, expectedPoints: int):
    assert calculate_retailer_points(retailer) == expectedPoints


#   ===== Testing total value ======


@pytest.mark.parametrize(
    "total, expectedPoints",
    [
        pytest.param("35.35", 0, id="Baseline total"),
        pytest.param(
            "35.00",
            ROUND_TOTAL_POINTS + MULTIPLE_TOTAL_POINTS,
            id="Round total",
        ),
        pytest.param("35.25", MULTIPLE_TOTAL_POINTS, id="Multiple total"),
        pytest.param("35.25", MULTIPLE_TOTAL_POINTS, id="Multiple total"),
    ],
)
def test_calculate_total_points(total: str, expectedPoints: int):
    assert calculate_total_points(total) == expectedPoints


#   ===== Testing item pairs =====


@pytest.mark.parametrize(
    "items, expectedPoints",
    [
        pytest.param(
            [(), (), (), (), ()],
            2 * PAIR_OF_ITEMS_POINTS,
            id="Baseline items",
        ),
    ],
)
def test_calculate_item_pairs_points(
    items: List[Dict[str, Any]], expectedPoints: int
):
    assert calculate_item_pairs_points(items) == expectedPoints


#   ===== Testing item description ======


@pytest.mark.parametrize(
    "item, expectedPoints",
    [
        pytest.param(
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            math.ceil(12.25 * DESC_MULTIPLIER),
            id="Baseline item",
        ),
    ],
)
def test_calculate_item_desc_points(item: Dict[str, str], expectedPoints: int):
    assert calculate_item_desc_points(item) == expectedPoints


#   ===== Testing purchase dates =====


@pytest.mark.parametrize(
    "purchaseDate, expectedPoints",
    [pytest.param("2022-01-01", ODD_PURCHASE_DATE_POINTS, id="Baseline date")],
)
def test_calculate_purchase_date_points(
    purchaseDate: str, expectedPoints: int
):
    assert calculate_purchase_date_points(purchaseDate) == expectedPoints


#   ===== Testing purchase times =====


@pytest.mark.parametrize(
    "purchaseTime, expectedPoints",
    [pytest.param("13:01", 0, id="Baseline purchase time")],
)
def test_calculate_purchase_time_points(
    purchaseTime: str, expectedPoints: str
):
    assert calculate_purchase_time_points(purchaseTime) == expectedPoints
