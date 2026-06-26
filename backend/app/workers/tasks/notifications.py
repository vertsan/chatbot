import structlog

from app.workers.celery_app import celery_app

logger = structlog.get_logger()


@celery_app.task
def send_email_notification(user_id: str, subject: str, body: str) -> dict:  # noqa: ARG001
    logger.info("Sending email notification", user_id=user_id, subject=subject)
    try:
        # TODO: Implement email sending
        return {"status": "sent", "user_id": user_id}
    except Exception as exc:
        logger.error("Email notification failed", error=str(exc))
        return {"status": "failed", "error": str(exc)}
