# receipt-webservice

## Setup

This project will be run using a docker container. Follow the instructions below:

1. Clone the repository

```
git clone https://github.com/drs0057/receipt-webservice.git
```

2. cd into the server folder

```
cd receipt-webservice/server
```

3. Build the docker image

```
docker build -t receipt_service .
```

4. Run the docker container

```
docker run -d -p 8000:8000 receipt_service
```

## Implementation

I decided to bulid this simple webservice using Python and Flask. This is
one of the simplest and easiest combos to quickly get a protoype working.
I chose to have duplicate receipts return the same id, eliminating repeat
calculations on the backend. Look below to read some brief thoughts on testing
and assumptions.

### Testing

Points unit testing: Take a look at the server/tests/test_points.py file to see my approach
to basic unit testing. I used pytest and the pytest.parametrize functionality to
test varying receipt inputs. I wanted to implement this to showcase my approach
to testing-based development. This gave me confidence that my points calculations
were robust and ready for deployment.

### Consideration/Assumptions

Duplicate Receipts: Unique IDs are generated using a SHA-1 hash of the receipt object. This ensures that duplicate receipts do not require recalculation. I am leaving some ambiguity as to what is considered a 'duplicate' receipt. Right now, I have defined duplicate receipts to be receipts that contain the same information for each field. The order in which fields are specified can be rearranged, and the receipt would still be considered identical. In a production environment, this will need to be considered more closely.

Dates/Times: I am using datetime to determine what is a valid date/time in accordance with the ISO 8601 standard. I know there is some logical validation such as months must be 1-12, minutes must be 0-59, etc. I am not sure how verbose this is (for example: there is no 30th day of February). I am leaving some ambiguity since this is just an exercise. In a production environment, I would make sure to understand what is a valid 'date' and 'time' as it pertains to the API contract and enforce it accordingly.
