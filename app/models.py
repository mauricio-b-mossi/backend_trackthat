from sqlmodel import Field, SQLModel, create_engine

class User(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None)
    name : str
    email : str
    password : str

class Application(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None) 
    user_id : int = Field(default=None, foreign_key="user.id")
    company : str
    position : str | None
    description : str | None
    link : str | None
    status : int
    date : str

class Notes(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None) 
    application_id : int = Field(default=None, foreign_key="application.id")
    description : str
    date : str

engine = create_engine("sqlite:///database.db", echo=True)

def create_database(engine):
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_database(engine)
