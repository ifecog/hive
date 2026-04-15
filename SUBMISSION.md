# Hive Agent Take-Home — Ifeoluwa

Two agents built with the [Aden Hive Framework](https://github.com/aden-hive/hive) using Claude (Opus 4.6) as the LLM and Brave Search for web retrieval.

---

## Agents

### 1. Research Agent X (`exports/research_agent_x/`)

A forever-alive interactive research assistant that takes any topic and produces a structured research brief.

**Flow:**

1. **Intake** — clarifies the research topic with the user
2. **Research** — searches the web and scrapes multiple sources
3. **Review** — presents findings and asks if the user wants to go deeper
4. **Report** — writes a cited report and loops back for follow-up

**How to run:**

```bash
hive tui
# Select "Research Agent X" and press Enter
# Enter a topic e.g. "AI agents in healthcare 2025"
```

Or directly:

```bash
hive run exports/research_agent_x --input '{"topic": "AI agents in healthcare 2025"}'
```

**Test topic used:** A common case for hypertension

---

### 2. Medication Checker (`exports/medication_checker/`)

Takes a list of medications as input, researches each one, identifies known interactions, flags dangerous combinations, and outputs a clear safety brief with a disclaimer to consult a doctor.

**Flow:**

1. **Intake** — takes a list of medications from the user
2. **Research** — searches for each medication's use case, side effects, and known interactions
3. **Analysis** — identifies dangerous and moderate interactions
4. **Report** — produces a safety brief with recommendations

**How to run:**

```bash
hive tui
# Select "Medication Checker" and press Enter
# Enter medications e.g. "Lisinopril, Ibuprofen, Aspirin"
```

Or directly:

```bash
hive run exports/medication_checker --input '{"medications": ["Lisinopril", "Ibuprofen", "Aspirin"]}'
```

---

## Setup

### Prerequisites

- Python 3.11+
- Git Bash (on Windows — WSL strongly recommended by the framework)
- Claude API key
- Brave Search API key (free tier at https://brave.com/search/api/)

### Installation

```bash
git clone https://github.com/ifecog/hive.git
cd hive
./quickstart.sh
```

When prompted, select **Anthropic (Claude)** as your LLM provider and enter your API key.

Then set up credentials:

```bash
claude
# Inside the session:
/hive-credentials
```

---

## Framework Feedback

### What worked well

- The `/hive` agent-builder inside Claude Code is genuinely impressive — describing a goal in plain English and watching it scaffold a full node graph, config, and connection code is a great developer experience.
- The template library is a solid starting point. The Deep Research Agent template saved significant time for both agents.
- The TUI dashboard gives real-time visibility into node execution which is very useful for debugging.
- Credential management via `/hive-credentials` is clean and straightforward once you understand the flow.

### Pain points encountered

**1. Windows support is rough**

The documentation warns against Command Prompt and PowerShell, but Git Bash support also has friction. The `hive` CLI threw a directory mismatch error (`hive must be run from the project directory`) that required falling back to `uv run python -m hive tui`. WSL would have avoided this entirely — worth making this clearer upfront in the README for Windows users.

**2. Credential decryption error on new terminal**

After running `/hive-credentials`, opening a new terminal session caused a `CredentialDecryptionError` for the Brave Search key. The fix was running `source ~/.bashrc` to load the `HIVE_CREDENTIAL_KEY` environment variable. This is a subtle gotcha that could frustrate new users — a simple check at startup with a helpful error message would go a long way.

**3. Web tool wiring in the research node**

The Research Agent initially ran without actually calling web search — it acknowledged it couldn't fetch URLs and returned provisional, uncited findings. The tools were registered but not wired correctly to the research node out of the box. Required debugging via `/hive-debugger` to resolve.

**4. `exports/` in `.gitignore`**

The exports folder is gitignored by default, which makes sharing or submitting agents unnecessarily tricky for new users. A note in the docs about using `git add -f` would help.

### Overall impression

Hive's core idea — describe an outcome, get a self-healing agent graph — is genuinely differentiated. The self-improving loop and built-in observability are features I haven't seen combined this cleanly in other frameworks. The rough edges are mostly around Windows support and first-time setup, which are fixable. The framework has strong potential for production use cases where reliability and adaptability matter more than simplicity of setup.

---