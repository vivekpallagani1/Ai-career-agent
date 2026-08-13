class AgentOrchestrator:
    """Routes actions to the correct AI agent or service."""

    def route(self, action: str, context: dict | None = None) -> str:
        context = context or {}
        return f'Queued {action} for {context.get("user_id", "unknown-user")}'
