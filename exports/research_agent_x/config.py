"""Runtime configuration."""

from dataclasses import dataclass

from framework.config import RuntimeConfig

default_config = RuntimeConfig()


@dataclass
class AgentMetadata:
    name: str = "Research Agent X"
    version: str = "1.0.0"
    description: str = (
        "Interactive research agent that rigorously investigates topics through "
        "multi-source search, quality evaluation, and synthesis - with TUI conversation "
        "at key checkpoints for user guidance and feedback."
    )
    intro_message: str = (
        "Hi! I'm Research Agent X. Tell me a topic and I'll investigate it "
        "thoroughly — searching multiple sources, evaluating quality, and synthesizing "
        "a comprehensive report. What would you like me to research?"
    )


metadata = AgentMetadata()
