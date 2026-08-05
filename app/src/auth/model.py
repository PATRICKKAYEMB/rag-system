from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
import uuid
from datetime import datetime



class User:
    uid:uuid.UUID = Field(
            sa_column=Column(
                pg.UUID,
                nullable=False,
                primary_key=True,
                default=uuid.uuid4
            ))
        
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool=Field(default=False)
    create_at:datetime= Field(sa_column=Column(
            pg.TIMESTAMP,default=datetime.now
        ))
    update_at:datetime= Field(sa_column=Column(
            pg.TIMESTAMP,default=datetime.now
        ))

    def __repr__(self):
        return f"<User{self.username}>"