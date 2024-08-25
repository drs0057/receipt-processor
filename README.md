# receipt-webservice

## Setup

## Elaboration

### Testing

### Consideration/Assumptions
Duplicate Receipts: Unique IDs are generated using a SHA-1 hash of the receipt object. This ensures that duplicate receipts do not require recalculation. I am leaving some ambiguity as to what is considered a 'duplicate' receipt. Right now, I have defined duplicate receipts to be receipts that contain the same information for each field. The order in which fields are specified can be rearranged, and the receipt would still be considered identical. In a production environment, this will need to be considered more closely.

Dates/Times: I am using datetime to determine what is a valid date/time in accordance with the ISO 8601 standard. I know there is some logical validation such as months must be 1-12, minutes must be 0-59, etc. I am not sure how verbose this is (for example: there is no 30th day of February). I am leaving some ambiguity since this is just an exercise. In a production environment, I would make sure to understand what is a valid 'date' and 'time' as it pertains to the API contract and enforce it accordingly.

