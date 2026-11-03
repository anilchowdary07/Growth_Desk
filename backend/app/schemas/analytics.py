from __future__ import annotations

"""Analytics schemas."""

from pydantic import BaseModel


class MetricCard(BaseModel):
    label: str
    value: str | int | float
    change: float | None = None
    trend: str = "neutral"  # up, down, neutral


class TimeSeriesPoint(BaseModel):
    date: str
    value: float | int


class OverviewAnalytics(BaseModel):
    total_reach: MetricCard
    engagement_rate: MetricCard
    new_leads: MetricCard
    content_published: MetricCard
    content_trend: list[TimeSeriesPoint]
    engagement_trend: list[TimeSeriesPoint]
    leads_by_source: list[dict]
    top_content: list[dict]
    growth_recommendations: list[str]
