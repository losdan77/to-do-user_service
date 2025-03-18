from pydantic import BaseModel

class SChangePassword(BaseModel):
    old_password: str
    new_password: str
    verify_new_password: str