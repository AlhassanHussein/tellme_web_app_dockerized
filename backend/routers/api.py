from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
import uuid

from ..database import get_session
from ..models import (
    Session as SessionModel, SessionCreate, SessionPublicRead, SessionPrivateRead,
    Message, MessageCreate, MessageRead
)
from ..scheduler import cleanup_expired_sessions

router = APIRouter(prefix="/api")

def get_valid_session_public(public_id: str, db: Session = Depends(get_session)):
    # Cleanup on request
    cleanup_expired_sessions(db)
    
    statement = select(SessionModel).where(SessionModel.public_id == public_id)
    session = db.exec(statement).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
        
    # SQLite returns naive datetime, ensure we compare correctly
    if session.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        # Double check, though cleanup should have handled it
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=410, detail="Session expired")
        
    return session

def get_valid_session_private(private_id: str, db: Session = Depends(get_session)):
    # Cleanup on request
    cleanup_expired_sessions(db)
    
    statement = select(SessionModel).where(SessionModel.private_id == private_id)
    session = db.exec(statement).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
        
    if session.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=410, detail="Session expired")
        
    return session

@router.post("/generate", response_model=dict)
def generate_session(session_in: SessionCreate, db: Session = Depends(get_session)):
    # Validate duration
    if session_in.duration_hours not in [6, 12, 24]:
        raise HTTPException(status_code=400, detail="Invalid duration. Must be 6, 12, or 24.")
    
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = now + timedelta(hours=session_in.duration_hours)
    
    # Handle optional name (empty string -> Guest)
    name = session_in.name if session_in.name and session_in.name.strip() else "Guest"
    
    new_session = SessionModel(
        name=name,
        expires_at=expires_at,
        created_at=now
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "public_id": new_session.public_id,
        "private_id": new_session.private_id,
        "expires_at": new_session.expires_at,
        "name": new_session.name
    }

@router.get("/public/{public_id}", response_model=SessionPublicRead)
def get_public_session(session: SessionModel = Depends(get_valid_session_public)):
    return session

@router.post("/public/{public_id}/message", response_model=dict)
def send_message(public_id: str, message_in: MessageCreate, db: Session = Depends(get_session)):
    # Manually getting session to reuse validation
    # Use get_valid_session_public logic but we need db session to write message
    session = get_valid_session_public(public_id, db)
    
    if not message_in.content or not message_in.content.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    new_message = Message(
        session_id=session.id,
        content=message_in.content,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(new_message)
    db.commit()
    
    return {"status": "success", "message": "Message sent anonymously"}

@router.get("/private/{private_id}", response_model=SessionPrivateRead)
def get_private_session(session: SessionModel = Depends(get_valid_session_private)):
    return session
