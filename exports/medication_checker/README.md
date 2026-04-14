# Medication Interaction Checker

**Version**: 1.0.0
**Type**: Multi-node agent
**Created**: 2026-04-14

## Overview

Accept a list of medications, research each one and all pairwise interactions, then output a concise plain-text safety brief — each med's purpose, dangerous combinations, moderate interactions to watch, and a consult-your-doctor disclaimer. No HTML. No fluff.

## Architecture

### Execution Flow

```
intake → research → report
```

### Nodes (3 total)

1. **intake** (event_loop)
   - Collect the list of medications from the user and confirm before proceeding
   - Writes: `medications`
   - Client-facing: Yes (blocks for user input)
2. **research** (event_loop)
   - Research each medication individually and all pairwise interactions by scraping drug databases directly
   - Reads: `medications`
   - Writes: `med_profiles, interactions`
   - Tools: `web_scrape`
   - Max visits: 3
3. **report** (event_loop)
   - Compile and present a concise plain-text medication safety brief to the user
   - Reads: `medications, med_profiles, interactions`
   - Writes: `safety_brief`
   - Client-facing: Yes (blocks for user input)

### Edges (2 total)

- `intake` → `research` (condition: on_success, priority=1)
- `research` → `report` (condition: on_success, priority=1)


## Goal Criteria

### Success Criteria

**Each medication's purpose and common side effects identified** (weight 0.2)
- Metric: meds_researched
- Target: 100%
**All pairwise interactions researched from reputable sources** (weight 0.3)
- Metric: pairs_researched
- Target: 100%
**Dangerous (Major) interactions clearly flagged** (weight 0.25)
- Metric: dangerous_interactions_flagged
- Target: true
**Moderate interactions identified and noted** (weight 0.1)
- Metric: moderate_interactions_noted
- Target: true
**Concise plain-text safety brief delivered in the conversation** (weight 0.15)
- Metric: brief_delivered
- Target: true

### Constraints

**Only report interactions found in retrieved sources — no fabrication** (hard)
- Category: accuracy
**Cite source URLs for all flagged interactions** (hard)
- Category: accuracy
**Always include consult-doctor disclaimer** (hard)
- Category: safety
**Output must be concise — no verbose explanations, straight to the point** (hard)
- Category: quality

## Required Tools

- `web_scrape`

## MCP Tool Sources

### hive-tools (stdio)
Hive tools MCP server

**Configuration:**
- Command: `uv`
- Args: `['run', 'python', 'mcp_server.py', '--stdio']`
- Working Directory: `tools`

Tools from these MCP servers are automatically loaded when the agent runs.

## Usage

### Basic Usage

```python
from framework.runner import AgentRunner

# Load the agent
runner = AgentRunner.load("exports/medication_checker")

# Run with input
result = await runner.run({"input_key": "value"})

# Access results
print(result.output)
print(result.status)
```

### Input Schema

The agent's entry node `intake` requires:


### Output Schema

Terminal nodes: `report`

## Version History

- **1.0.0** (2026-04-14): Initial release
  - 3 nodes, 2 edges
  - Goal: Medication Interaction Checker
