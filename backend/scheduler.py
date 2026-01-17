from datetime import datetime, timezone
from sqlmodel import Session, select
from .models import Session as SessionModel

def cleanup_expired_sessions(db: Session):
    # SQLite stores datetimes as naive, so we compare with naive UTC
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    statement = select(SessionModel).where(SessionModel.expires_at < now)
    results = db.exec(statement)
    for session in results:
        db.delete(session)
    db.commit()
