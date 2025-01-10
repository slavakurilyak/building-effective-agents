from pydantic import BaseModel
from typing import Optional

class LeadRecord(BaseModel):
    twitter_handle: str
    bio: str
    followers: int
    icp_match: bool
    last_message_sent: Optional[str]  # e.g., the timestamp or a short note
    replied: bool

class MessageRecord(BaseModel):
    twitter_handle: str
    direction: str  # 'inbound' or 'outbound'
    content: str