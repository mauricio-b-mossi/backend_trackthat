from sqlmodel import Field, SQLModel, create_engine, Relationship
from enum import Enum 
import datetime

class UserBase(SQLModel):
    id : int | None = Field(primary_key=True, default=None)
    name : str = Field(index=True)
    email : str

class User(UserBase, table=True):
    password : str

    applications : list["Application"] = Relationship(back_populates="user")

class Status(Enum):
    ON_GOING = 0
    ACCEPTED = 1
    REJECTED = 2


class ApplicationBase(SQLModel):
    company : str = Field(index=True)
    position : str | None
    description : str | None
    link : str | None
    status : int = Field(index=True, default=Status.ON_GOING)
    date : datetime.date = Field(index=True)

class Application(ApplicationBase, table=True):
    user_id : int | None = Field(foreign_key="user.id", default=None)
    id : int | None = Field(primary_key=True, default=None) 

    user : User = Relationship(back_populates="applications")
    notes : list["Notes"] = Relationship(back_populates="application")

class Notes(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None) 
    application_id : int | None = Field(foreign_key="application.id", default=None)
    description : str
    date : str = Field(index=True)

    application : Application = Relationship(back_populates="notes")

engine = create_engine("sqlite:///database.db", echo=True)

def create_database(engine):
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_database(engine)
