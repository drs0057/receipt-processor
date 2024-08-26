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

Once the Docker container is running, you can interact with the two endpoints at:

```
localhost:8000/receipts/process
localhost:8000/receipts/{id}/points
```

## Implementation

I decided to build this simple web service using Python and Flask. This is
one of the simplest and easiest combos to quickly get a protoype working.
I chose to have duplicate receipts return the same ID, eliminating repeat
calculations. IDs are generated using Python's uuid library. Point values are
placed in constant variables so that they can be changed, if desired,
without breaking any logic. Look below to read some brief thoughts on testing and assumptions.

### Testing

I used pytest to test the correctness of my endpoints and my points calculations.
I wanted to implement this to showcase my approach to testing-based development.
This gave me confidence that my points calculations were correct and that my
endpoints abide by the provided openapi contract.

API testing (31 tests): Look in the server/tests/test_host.py file to see how I tested my
APIs. This testing is to ensure that my 'processing' endpoint accepts valid receipts and
denies invalid ones, and that my 'points' endpoint accepts valid IDs and denies invalid ones.
Most of this testing revolves around the regex provided in the API contract.

Points testing (40 tests): Take a look at the server/tests/test_points.py file to see my approach
to basic unit testing. These tests assume that the API contract is satisfied and
the receipts are valid. I test various receipt fields and make sure points and added appropriately.

### Consideration/Assumptions

Duplicate Receipts: Unique IDs are generated using a SHA-1 hash of the receipt object. The hash is used to seed the generation of a uuid. This ensures that duplicate receipts do not require recalculation. I am leaving some ambiguity as to what is considered a 'duplicate' receipt. Right now, I have defined duplicate receipts to be receipts that contain the same information for each field. The order in which fields are specified can be rearranged, and the receipt would still be considered identical. In a production environment, this will need to be considered more closely.

Dates/Times: I am using datetime to determine what is a valid date/time in accordance with the ISO 8601 standard. I know there is some logical validation such as months must be 1-12, minutes must be 0-59, no 30th day in February, etc. I did not extensively test how verbose the datetime validation is, and am leaving some ambiguity since this is just an exercise. In a production environment, I would make sure to understand what is a valid 'date' and 'time' as it pertains to the API contract and enforce it accordingly.
