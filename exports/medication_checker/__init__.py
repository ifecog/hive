"""
Medication Interaction Checker — research drug interactions and deliver a concise safety brief.

Accepts a list of medications, researches each one and all pairwise interactions,
and outputs a plain-text safety brief with dangerous combinations, moderate interactions,
and a consult-your-doctor disclaimer.
"""

from .agent import MedicationCheckerAgent, default_agent, goal, nodes, edges
from .config import RuntimeConfig, AgentMetadata, default_config, metadata

__version__ = "1.0.0"

__all__ = [
    "MedicationCheckerAgent",
    "default_agent",
    "goal",
    "nodes",
    "edges",
    "RuntimeConfig",
    "AgentMetadata",
    "default_config",
    "metadata",
]
