from flask import Flask, jsonify, request
from receipt_processor import ReceiptProcessor

app = Flask(__name__)

receiptProcessor = ReceiptProcessor()


@app.route("/receipts/process", methods=["POST"])
def upload_receipt():
    receipt = request.json
    print(f"\nProcessing receipt...")
    try:
        ID = receiptProcessor.process_receipt(receipt)
    except ValueError:
        print("Invalid receipt uploaded")
        return "The receipt is invalid", 400

    return jsonify({"id": ID}), 200


@app.route("/receipts/<string:ID>/points", methods=["GET"])
def get_receipt_points(ID: str):
    print("\nProcessing receipt query...")
    if ID in receiptProcessor.receipts:
        print("Valid receipt queried, returning points...")
        return jsonify({"points": receiptProcessor.receipts[ID]}), 200
    # Receipt not found
    print("Invalid receipt queried")
    return "No receipt found for that id", 404


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")
