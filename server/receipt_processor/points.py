import math
from datetime import datetime
from typing import Any, Dict, List

from .configuration import (
    ALPHANUMERIC_POINTS,
    DESC_MULTIPLIER,
    MULTIPLE_TOTAL_POINTS,
    ODD_PURCHASE_DATE_POINTS,
    PAIR_OF_ITEMS_POINTS,
    PURCHASE_TIME_POINTS,
    ROUND_TOTAL_POINTS,
)


def calculate_receipt_points(receipt: Dict[str, Any]) -> int:
    """Takes in a valid JSON receipt and returns assigned points.
    Assumes the input object is valid in accordance with the provided
    API contract."""
    points = 0
    # Calculate points based on retailer name
    points += calculate_retailer_points(receipt["retailer"])

    # Calculate points based on total amount (round dollar amount and multiple)
    points += calculate_total_points(receipt["total"])

    # Calculate points based on pairs of items
    points += calculate_item_pairs_points(receipt["items"])

    # Calculate points based on item descriptions
    for item in receipt["items"]:
        points += calculate_item_desc_points(item)

    # Calculate points based on purchaseDate
    points += calculate_purchase_date_points(receipt["purchaseDate"])

    # Calculate points based on purchaseTime
    points += calculate_purchase_time_points(receipt["purchaseTime"])

    return points


def calculate_retailer_points(retailer: str) -> int:
    return sum(ALPHANUMERIC_POINTS for char in retailer if char.isalnum())


def calculate_total_points(total: str) -> int:
    points = 0
    if int(total.split(".")[1]) == 0:
        points += ROUND_TOTAL_POINTS
    if float(total) % 0.25 == 0:
        points += MULTIPLE_TOTAL_POINTS
    return points


def calculate_item_pairs_points(items: List[Dict[str, str]]) -> int:
    return (len(items) // 2) * PAIR_OF_ITEMS_POINTS


def calculate_item_desc_points(item: Dict[str, str]) -> int:
    if len(item["shortDescription"].strip()) % 3 == 0:
        return math.ceil(float(item["price"]) * DESC_MULTIPLIER)
    return 0


def calculate_purchase_date_points(purchaseDate: str) -> int:
    return (
        ODD_PURCHASE_DATE_POINTS if int(purchaseDate.split("-")[-1]) % 2 else 0
    )


def calculate_purchase_time_points(purchaseTime: str) -> int:
    minTime = datetime.strptime("14:00", "%H:%M").time()
    maxTime = datetime.strptime("16:00", "%H:%M").time()
    formattedPurchaseTime = datetime.strptime(purchaseTime, "%H:%M").time()
    return (
        PURCHASE_TIME_POINTS
        if minTime < formattedPurchaseTime < maxTime
        else 0
    )
