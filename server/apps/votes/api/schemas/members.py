from pydantic import BaseModel


class MemberAuth(BaseModel):
    invite_code: str
