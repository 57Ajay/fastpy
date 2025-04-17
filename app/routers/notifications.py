from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from typing import Annotated
from pydantic import BaseModel, EmailStr
from app.utils import send_email, write_log

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationRequest(BaseModel):
    message: str

@router.post("/log/email")
async def send_notificationbg(
    notification: NotificationRequest,
    background_tasks: BackgroundTasks,
    email: Annotated[str, EmailStr]=Query(...)
    ):
    """
    Send a notification email in the background.
    """
    try:
        background_tasks.add_task(write_log, f"Sending email to {email} with message: {notification.message}")
        background_tasks.add_task(send_email, email, notification.message)
        return {"status": "Notification queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
