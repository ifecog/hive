"""Runtime configuration for Medication Checker Agent."""

from dataclasses import dataclass

from framework.config import RuntimeConfig

default_config = RuntimeConfig(model="claude-haiku-4-5-20251001")


@dataclass
class AgentMetadata:
    name: str = "Medication Interaction Checker"
    version: str = "1.0.0"
    description: str = (
        "Accept a list of medications, research each one and all pairwise interactions, "
        "then output a concise plain-text safety brief — each med's purpose, dangerous "
        "combinations, moderate interactions to watch, and a consult-your-doctor disclaimer."
    )
    intro_message: str = (
        "Hi! I'm your Medication Interaction Checker. "
        "Give me a list of medications and I'll research interactions between them — "
        "purpose of each drug, dangerous combinations, and anything to watch out for. "
        "What medications would you like me to check?"
    )


metadata = AgentMetadata()
