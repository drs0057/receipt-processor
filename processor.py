from datetime import datetime
import math

def process_receipt(receipt):
    """Takes in a JSON object of a receipt and returns assigned points."""
    points = 0
    # One point for every alphanumeric character in the retailer name.
    points += sum(1 for char in receipt["retailer"] if char.isalnum())

    # 50 points if the total is a round dollar amount with no cents.
    if int(receipt["total"].split('.')[1]) == 0:
        points += 50

    # 25 points if the total is a multiple of 0.25.
    if float(receipt["total"]) % .25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    points += (len(receipt["items"]) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer. 
    # The result is the number of points earned.
    for item in receipt["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points += math.ceil(float(item["price"]) * 0.2)

    # 6 points if the day in the purchase date is odd.
    if int(receipt["purchaseDate"].split('-')[-1]) % 2:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    minTime = datetime.strptime("14:00", "%H:%M").time()
    maxTime = datetime.strptime("16:00", "%H:%M").time()
    purchaseTime = datetime.strptime(receipt["purchaseTime"], "%H:%M").time()
    if minTime < purchaseTime < maxTime:
        points += 10

    return points


receipt = {
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

points = process_receipt(receipt)
print(points)