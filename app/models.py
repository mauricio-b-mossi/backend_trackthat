from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id : int | None = Field(primary_key=True, default=None)
    name : str
