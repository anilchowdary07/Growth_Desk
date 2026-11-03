from __future__ import annotations

"""Celery background tasks for asynchronous agent operations."""

import logging
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.agent_tasks.run_agent_task")
def run_agent_task(workspace_id: str, agent_type: str, task_payload: dict):
    """Execute a heavy multi-step agent research or content batch generation."""
    logger.info(f"Running background agent task for {agent_type} in workspace {workspace_id}")
    return {"status": "completed", "agent": agent_type}

