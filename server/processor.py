import json
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List

from receipt_points import calculate_receipt_points

REGEX = {
    "retailer": "^[\\w\\s\\-&]+$",
    "total": "^\\d+\\.\\d{2}$",
    "desc": "^[\\w\\s\\-]+$",
    "price": "^\\d+\\.\\d{2}$",
}


class ReceiptProcessor:
    """Responsible for processing receipts, including receipt validation,
    generating ids, calculating points, and storing ids/points."""

    def __init__(self) -> None:
        # Dictionary mapping IDs to points, intended to persist in memory only
        self.receipts = {}

    def process_receipt(self, receipt: List[Dict[str, Any]]) -> str:
        """Processes receipt by validating, generating an id, calculating
        points, persisting the (id, points) in memory, then returning the id.
        """
        # Check if the receipt has been uploaded before, avoid revalidation
        if (ID := self._generate_id(receipt)) in self.receipts:
            print("Duplicate receipt uploaded. Returning previous ID...")
            return ID

        if not self._valid_receipt(receipt):
            raise ValueError("Invalid receipt")

        ID = self._generate_id(receipt)
        self.receipts[ID] = calculate_receipt_points(receipt)
        print(f"New receipt stored: id: {ID} points: {self.receipts[ID]}")
        return ID

    def _generate_id(self, receipt: Dict[str, Any]) -> str:
        """Generates a unique id based on the hash of the receipt. Identical
        receipts will produce the same id."""
        # Convert JSON object to a string, sort keys for consistency
        receiptStr = json.dumps(receipt, sort_keys=True)
        # Generate a unique id based on the hash of the receipt
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, receiptStr))

    def _valid_receipt(self, receipt: Dict[str, Any]) -> bool:
        """Validates the receipt based on the provided API contract."""
        return (
            self._validate_retailer(receipt)
            and self._validate_purchase_date(receipt)
            and self._validate_purchase_time(receipt)
            and self._validate_items(receipt)
            and self._validate_total(receipt)
        )

    def _validate_retailer(self, receipt: Dict[str, Any]) -> bool:
        """Validate the retailer field."""
        return (
            "retailer" in receipt
            and isinstance(receipt["retailer"], str)
            and re.match(REGEX["retailer"], receipt["retailer"])
        )

    def _validate_purchase_date(self, receipt: Dict[str, Any]) -> bool:
        """Validate the purchase date field. Must conform to the
        ISO 8601 standard for dates."""
        if "purchaseDate" not in receipt or not isinstance(
            receipt["purchaseDate"], str
        ):
            return False
        try:
            datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _validate_purchase_time(self, receipt: Dict[str, Any]) -> bool:
        """Validate the purchase time field. Must conform to the
        ISO 8601 standard for time."""
        if "purchaseTime" not in receipt or not isinstance(
            receipt["purchaseTime"], str
        ):
            return False
        try:
            datetime.strptime(receipt["purchaseTime"], "%H:%M")
            return True
        except ValueError:
            return False

    def _validate_items(self, receipt: Dict[str, Any]) -> bool:
        """Validate the items list and each item's description and price."""
        if (
            "items" not in receipt
            or not isinstance(receipt["items"], list)
            or len(receipt["items"]) < 1
        ):
            return False

        for item in receipt["items"]:
            if not (
                self._validate_item_description(item)
                and self._validate_item_price(item)
            ):
                return False
        return True

    def _validate_item_description(self, item: Dict[str, Any]) -> bool:
        """Validate the short description of an item."""
        return (
            "shortDescription" in item
            and isinstance(item["shortDescription"], str)
            and re.match(REGEX["desc"], item["shortDescription"])
        )

    def _validate_item_price(self, item: Dict[str, Any]) -> bool:
        """Validate the price of an item."""
        return (
            "price" in item
            and isinstance(item["price"], str)
            and re.match(REGEX["price"], item["price"])
        )

    def _validate_total(self, receipt: Dict[str, Any]) -> bool:
        """Validate the total field."""
        return (
            "total" in receipt
            and isinstance(receipt["total"], str)
            and re.match(REGEX["total"], receipt["total"])
        )
