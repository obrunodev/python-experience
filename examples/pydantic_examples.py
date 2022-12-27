from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class User(BaseModel):
    id: int
    name = "Bruno Pianca"
    signup_ts: Union[datetime, None] = None
    friends: List[int] = []
    

external_data = {
    "id": 123,
    "signup_ts": "2022-10-01 14:21",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
print(user.id)
