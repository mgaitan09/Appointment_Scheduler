# Appointment Scheduler Example

## What's inside?

This is a [FastAPI](https://fastapi.tiangolo.com/) implementation of 2 endpoints:

1. A POST endpoint that takes a date/time and user ID (both required). Creates an
   appointment beginning at that time for that user or returns an appropriate
   status code and error if the appointment cannot be made (the user already
   has an appointment that day).
   With these features:
   all appointments must start and end on the hour or half hour
   all appointments are exactly 30 minutes long
   a user can only have 1 appointment on a calendar date

2. A GET endpoint that takes a user ID (required) and returns all appointments for
   the user.

## How to run it?

There are 2 main ways to run this:

#### Locally run the Docker Image: (recommended)

1. run `docker run --rm -p 80:80 mgaitan09/appointment_scheduler`

###### Automated Documentation on how to use the endpoints is provided via Swagger(http://localhost/docs) (after starting the server)

#### Clone the repo and run locally: (recommended)

2.  Build the image or run the code locally
    1. Clone the repo locally
    2. run pip install requirements.txt
    3. run uvicorn main:app --reload

###### Automated Documentation on how to use the endpoints is provided via Swagger(http://localhost:8000/docs) (after starting the server)

## How to use the endpoints?

There are 2 endpoints:

**1. GET Appointments Endpoint**

This is an endpoint that will provide a list of the appointments that the UserID provided has in the system, if there are no appointments it will return an empty list [].

- **URL**

/appointments/{UserID}

{UserID}: int

- **Method:**

  `GET`

- **URL Params**

  **Required:**

  `UserID=[integer]`

- **Success Response:**

  - **Code:** 200 <br />
    **Content:** `{ "UserID": 12345, "appts": [ { "Date": "2021-10-26", "UserID": 12345, "Start_DateTime": "2021-10-26T02:00:00", "End_DateTime": "2021-10-26T02:30:00" } ] }`

* **Sample Call:**

  `curl -X 'GET' \ 'http://localhost/appointments/12345' \ -H 'accept: application/json'`

###### Note 1: it is best to run this call after creating an appointment for an UserID (you can run the example below and then run this again)

###### Note 2: if running locally, port 8000 must be used i.e. http://localhost:8000/appointments

**2. POST New Appointment Endpoint**

This is an endpoint that creates a 30 minutes an appointment for the UserID based on the starting time provided, starting time needs to be at the hour(22:00) or half an hour(22:30) exactly, an error message will describe

- **Method:**

  `POST`

- **URL**

/appointments/

- **Method:**

  `GET`

- **URL Params**

None

- **Data Params**
  **Required:**
  {
  "userid": int,
  "date": date in format "yyyy-mm-dd",
  "time": time in format "hh:mm"
  }

`mm` in time must be `00` or `30` if not it will error out asking for a round hour or half hour input

- **Success Response:**

  - **Code:** 200 <br />
    **Content:** `{ "UserID": 12345, "msg": "New Appointment created for 12345 on 2021-10-26 starting at 2021-10-26 02:00:00" }`

* **Error Response:**

  - **Code:** 400 <br />
    **Content:** `{ "detail": "User 12345 already has an appointments on that date (2021-10-26)" }`

  OR

  - **Code:** 422
    Error: Unprocessable Entity <br />
    **Content:** `{ "detail": [ { "loc": [ "body", "time" ], "msg": "start time must start on the hour or half hour", "type": "value_error" } ] }`

* **Sample Call:**

  ```curl -X 'POST' \
  'http://localhost/appointments/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "userid": "12345",
  "date": "2021-10-26",
  "time": "02:00"
  }'
  ```

###### Note: if running locally, port 8000 must be used i.e. http://localhost:8000/appointments
