# app/schema/schemas.py
# Models schemas

from typing import List

from pydantic import BaseModel


# Request schema
class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str


# Request schema
class Classifier(BaseModel):
    sequence: str = "One day I will see the world"
    candidate_labels: List = ["travel", "cooking", "dancing"]


# Response schema
class ShowUser(BaseModel):
    email: str

    class Config:
        orm_mode = True


# Request schema
class Login(BaseModel):
    username: str
    password: str
