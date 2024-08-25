"""Test cases are generated in the context of valid inputs in accordance
with the API contract, i.e. nothing that invalidates the contract should be 
tested here."""

import math
from typing import Any, Dict, List

import pytest
from receipt_processor.configuration import (
    ALPHANUMERIC_POINTS,
    DESC_MULTIPLIER,
    MULTIPLE_TOTAL_POINTS,
    ODD_PURCHASE_DATE_POINTS,
    PAIR_OF_ITEMS_POINTS,
    PURCHASE_TIME_POINTS,
    ROUND_TOTAL_POINTS,
)
from receipt_processor.points import (
    calculate_item_desc_points,
    calculate_item_pairs_points,
    calculate_purchase_date_points,
    calculate_purchase_time_points,
    calculate_receipt_points,
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
        pytest.param("   ", 0, id="Spaces"),
        pytest.param("123", ALPHANUMERIC_POINTS * 3, id="Numbers"),
        pytest.param(
            "_-&",
            0,
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
        pytest.param("35.25", MULTIPLE_TOTAL_POINTS, id="Multiple of 0.25"),
        pytest.param("12.34", 0, id="Random total"),
        pytest.param("0.34", 0, id="Zero dollar amount"),
        pytest.param(
            "0.00",
            ROUND_TOTAL_POINTS + MULTIPLE_TOTAL_POINTS,
            id="Zero dollar and cents",
        ),
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
            id="5 items",
        ),
        pytest.param(
            [(), (), (), (), (), ()],
            3 * PAIR_OF_ITEMS_POINTS,
            id="6 items",
        ),
        pytest.param(
            [(), ()],
            1 * PAIR_OF_ITEMS_POINTS,
            id="2 items",
        ),
        pytest.param(
            [()],
            0,
            id="1 items",
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
            id="Desc of length 18, random price",
        ),
        pytest.param(
            {"shortDescription": "Emils Cheese Pizza", "price": "0.00"},
            0,
            id="Desc of length 18, zero cost item",
        ),
        pytest.param(
            {"shortDescription": "Emils Cheese Pizza", "price": "0.01"},
            math.ceil(0.01 * DESC_MULTIPLIER),
            id="Desc of length 18, 0.01 cost item",
        ),
        pytest.param(
            {"shortDescription": "Emils Cheese Pizz", "price": "12.34"},
            0,
            id="Desc of length 17",
        ),
        pytest.param(
            {"shortDescription": " Emils Cheese Pizz ", "price": "12.34"},
            0,
            id="Desc of length 17 with trimming",
        ),
        pytest.param(
            {"shortDescription": " Emils Cheese Pizza ", "price": "12.34"},
            math.ceil(12.34 * DESC_MULTIPLIER),
            id="Desc of length 18 with trimming",
        ),
        pytest.param(
            {"shortDescription": " abc ", "price": "12.34"},
            math.ceil(12.34 * DESC_MULTIPLIER),
            id="Desc of length 3 with trimming",
        ),
        pytest.param(
            {"shortDescription": " ", "price": "12.34"},
            math.ceil(12.34 * DESC_MULTIPLIER),
            id="Desc of just whitespace",
        ),
        # Hypens are allowed via the contract
        pytest.param(
            {"shortDescription": " ---  ", "price": "12.34"},
            math.ceil(12.34 * DESC_MULTIPLIER),
            id="Hyphens with whitespace",
        ),
    ],
)
def test_calculate_item_desc_points(item: Dict[str, str], expectedPoints: int):
    assert calculate_item_desc_points(item) == expectedPoints


#   ===== Testing purchase dates =====


@pytest.mark.parametrize(
    "purchaseDate, expectedPoints",
    [
        pytest.param("2022-01-01", ODD_PURCHASE_DATE_POINTS, id="Odd day"),
        pytest.param("2022-01-02", 0, id="Even day"),
        pytest.param(
            "2022-02-01",
            ODD_PURCHASE_DATE_POINTS,
            id="Odd day, even year and month",
        ),
    ],
)
def test_calculate_purchase_date_points(
    purchaseDate: str, expectedPoints: int
):
    assert calculate_purchase_date_points(purchaseDate) == expectedPoints


#   ===== Testing purchase times =====


@pytest.mark.parametrize(
    "purchaseTime, expectedPoints",
    [
        pytest.param("13:01", 0, id="1:01pm"),
        pytest.param("15:00", PURCHASE_TIME_POINTS, id="3:00pm"),
        pytest.param("15:01", PURCHASE_TIME_POINTS, id="3:01pm"),
        # 2:00pm is not valid, must be AFTER 2:00pm
        pytest.param("14:00", 0, id="2:00pm"),
        # 4:00pm is not valid, must be BEFORE 4:00pm
        pytest.param("16:00", 0, id="4:00pm"),
        pytest.param("14:01", PURCHASE_TIME_POINTS, id="2:01pm"),
        pytest.param("15:59", PURCHASE_TIME_POINTS, id="3:59pm"),
    ],
)
def test_calculate_purchase_time_points(
    purchaseTime: str, expectedPoints: str
):
    assert calculate_purchase_time_points(purchaseTime) == expectedPoints


#   ===== Integration testing for entire processor =====

# Assuming all composite functions pass testing, this should be simple.
# Just test a few simple configurations.


@pytest.mark.parametrize(
    "receipt, expectedPoints",
    [
        pytest.param(
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {
                        "shortDescription": "Emils Cheese Pizza",
                        "price": "12.25",
                    },
                    {
                        "shortDescription": "Emils Cheese Pizz",
                        "price": "12.25",
                    },
                ],
                "total": "35.35",
            },
            ALPHANUMERIC_POINTS * 6
            + PAIR_OF_ITEMS_POINTS * 1
            + math.ceil(12.25 * DESC_MULTIPLIER)
            + ODD_PURCHASE_DATE_POINTS,
            id="Some valid retailer chars, a couple pairs of items, one valid item desc, odd purchase day",
        ),
        pytest.param(
            {
                "retailer": "T",
                "purchaseDate": "2022-01-02",
                "purchaseTime": "15:00",
                "items": [
                    {
                        "shortDescription": "Emils Cheese Pizz",
                        "price": "12.25",
                    },
                ],
                "total": "35.00",
            },
            ALPHANUMERIC_POINTS * 1
            + ROUND_TOTAL_POINTS
            + MULTIPLE_TOTAL_POINTS
            + PURCHASE_TIME_POINTS,
            id="Valid retail char, round total, valid purchase time",
        ),
    ],
)
def test_process_receipt(receipt: Dict[str, Any], expectedPoints: int):
    assert calculate_receipt_points(receipt) == expectedPoints
