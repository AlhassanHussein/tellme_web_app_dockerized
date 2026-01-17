from datetime import datetime, timezone
import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class SessionBase(SQLModel):
    name: str = Field(default="Guest")
    expires_at: datetime
    
class Session(SessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    public_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    private_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    messages: List["Message"] = Relationship(back_populates="session")

class MessageBase(SQLModel):
    content: str

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    session: Session = Relationship(back_populates="messages")

class SessionCreate(SQLModel):
    name: Optional[str] = "Guest"
    duration_hours: int

class SessionPublicRead(SQLModel):
    public_id: str
    name: str
    expires_at: datetime

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime

class SessionPrivateRead(SQLModel):
    name: str
    expires_at: datetime
    messages: List[MessageRead]
