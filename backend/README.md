# AI GrowthDesk Backend

Production-ready backend for AI GrowthDesk — an Autonomous AI Marketing Workforce platform.

## Architecture
- FastAPI application with async RESTful endpoints under `/api/v1`
- Multi-tenant workspace data isolation at every layer
- BYOK (Bring Your Own Key) model with Fernet encryption
- Specialized AI agent workforce (Marketing Director, Research, Brand Strategist, Content Creator, Creative Director, Social Media Manager, Community Manager, Lead Agent, Advertising, SEO, Growth Analyst)
- PostgreSQL + pgvector for Brand Brain knowledge base RAG
- Redis + Celery for background scheduling and async operations

