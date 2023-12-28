from pydantic import BaseModel


class SendVoteAnswer(BaseModel):
    option_id: int
