import jsonify
from flask import Flask, request
from processor import ReceiptProcessor

app = Flask(__name__)
receiptProcessor = ReceiptProcessor()


@app.route("/receipts/process", methods=["POST"])
def receipts():
    receipt = request.json
    print()
    print(f"Processing receipt...")
    try:
        ID = receiptProcessor.process_receipt(receipt)
    except ValueError:
        return "The receipt is invalid", 400

    print(f"RECEIPTS: {receiptProcessor.receipts}")
    return f"You just posted: {receipt}\nid: {ID}"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
