from sqlmodel import Field, SQLModel, create_engine

class UserOut(SQLModel):
    id : int | None = Field(primary_key=True, default=None)
    name : str = Field(index=True)
    email : str

class User(UserOut, table=True):
    password : str

class Application(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None) 
    user_id : int = Field(default=None, foreign_key="user.id")
    company : str = Field(index=True)
    position : str | None
    description : str | None
    link : str | None
    status : int = Field(index=True)
    date : str = Field(index=True)

class Notes(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None) 
    application_id : int = Field(default=None, foreign_key="application.id")
    description : str
    date : str = Field(index=True)

engine = create_engine("sqlite:///database.db", echo=True)

def create_database(engine):
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_database(engine)
