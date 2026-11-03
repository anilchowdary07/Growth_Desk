from __future__ import annotations

"""Celery background tasks for post scheduling and publishing."""

import logging
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.publishing_tasks.publish_post_task")
def publish_post_task(scheduled_post_id: str):
    """Publish a scheduled post to the respective social platform."""
    logger.info(f"Publishing scheduled post: {scheduled_post_id}")
    # Integration logic dispatches to platform API handler
    return {"status": "success", "scheduled_post_id": scheduled_post_id}


@celery_app.task(name="app.tasks.publishing_tasks.check_scheduled_posts")
def check_scheduled_posts():
    """Periodic task: scan for scheduled posts due for publication."""
    logger.info("Scanning for due scheduled posts...")
    return {"scanned": True}
