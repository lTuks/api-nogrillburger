from pymongo import MongoClient
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

URL_mongo = "mongodb+srv://dbNoGrill:XFN0bN4NJqQ0pYXz@nogrillburger.fvgs7.mongodb.net/NoGrillBurger?retryWrites=true&w=majority"
client = MongoClient(URL_mongo)
db = client["NoGrillBurger"]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Burger(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    cost: float
    ingredients: list

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Other(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    cost: float
    description: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Client(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    cellphone: str
    address: str
    orders: Optional[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Order(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    client_id: PyObjectId
    burger_id: Optional[PyObjectId]
    other_id: Optional[PyObjectId]
    price: float
    delivery: bool
    active: bool
    date: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Stock(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    burger_id: Optional[PyObjectId]
    other_id: Optional[PyObjectId]
    cost: float
    amount: int
    date: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
