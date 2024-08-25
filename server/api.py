from flask import Flask, jsonify, request
from processor import ReceiptProcessor

app = Flask(__name__)
receiptProcessor = ReceiptProcessor()


@app.route("/receipts/process", methods=["POST"])
def upload_receipt():
    receipt = request.json
    print()
    print(f"Processing receipt...")
    try:
        ID = receiptProcessor.process_receipt(receipt)
    except ValueError:
        return "The receipt is invalid", 400

    print(f"RECEIPTS: {receiptProcessor.receipts}")
    return jsonify({"id": ID}), 200


@app.route("/receipts/<string:ID>/points", methods=["GET"])
def get_receipt_points(ID: str):
    if ID in receiptProcessor.receipts:
        return jsonify({"points": receiptProcessor.receipts[ID]}), 200
    # Receipt not found
    return "No receipt found for that id", 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
