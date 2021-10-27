from typing import Optional
import datetime as dt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, validator


class Appointment(BaseModel):
    userid: int
    date: dt.date  # YYYY-MM-DD
    time: dt.time

    @validator("time")
    def name_must_contain_space(cls, t):
        if t.minute not in [0, 30]:
            raise ValueError("start time must start on the hour or half hour")
        return t

    class Config:
        schema_extra = {
            "example": {"userid": "12345", "date": "2021-10-26", "time": "02:00"}
        }


class Appointments_by_UserID(BaseModel):
    UserID: int
    appts: list


class Appointments_Confirmation(BaseModel):
    UserID: int
    msg: str


app = FastAPI()


class Appointments:
    """An Appointment object simulating interaction with the database
    and Appointment creation logic that would interact with the database too"""

    def __init__(self):
        self.appointments_db = []

    def add(self, newappointment):
        # this list comprehension will return any appointments that already exists for that UserID and that Date
        if [
            anyappt
            for anyappt in self.appointments_db
            if anyappt.get("UserID", []) == newappointment["UserID"]
            and anyappt.get("Date", []) == newappointment["Date"]
        ]:
            raise HTTPException(
                status_code=400,
                detail=f"User {newappointment['UserID']} already has an appointments on that date ({newappointment['Date']})",
            )

        self.appointments_db.append(
            {
                "Date": newappointment["Date"],
                "UserID": newappointment["UserID"],
                "Start_DateTime": newappointment["Start_DateTime"],
                "End_DateTime": newappointment["End_DateTime"],
            }
        )

    def get(self, userid):
        appointments_for_userid = [
            anyappt
            for anyappt in self.appointments_db
            if anyappt.get("UserID", []) == userid
        ]
        return appointments_for_userid


appts_db = Appointments()


@app.post("/appointments/", status_code=200, response_model=Appointments_Confirmation)
def new_appointment(appointment: Appointment):
    appointment = appointment.dict()
    start_time = appointment["time"].replace(second=0, microsecond=0)
    start_datetime = dt.datetime.combine(appointment["date"], start_time)
    end_datetime = start_datetime + dt.timedelta(minutes=30)
    print(f"{start_datetime} to {start_datetime+dt.timedelta(minutes=30)}")
    newrow = {
        "Date": appointment["date"],
        "UserID": appointment["userid"],
        "Start_DateTime": start_datetime,
        "End_DateTime": end_datetime,
    }
    appts_db.add(newrow)
    response = {}
    response["UserID"] = appointment["userid"]
    response[
        "msg"
    ] = f"New Appointment created for {appointment['userid']} on {appointment['date']} starting at {start_datetime}"
    return response


@app.get(
    "/appointments/{userid}", status_code=200, response_model=Appointments_by_UserID
)
async def get_appointments(userid: int):
    appts = {}
    appts["UserID"] = userid
    appts["appts"] = appts_db.get(userid)
    return appts
