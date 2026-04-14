"""Node definitions for Medication Interaction Checker."""

from framework.graph import NodeSpec

# Node 1: Intake (client-facing)
# Collect the medication list from the user and confirm it.
intake_node = NodeSpec(
    id="intake",
    name="Medication Intake",
    description="Collect the list of medications from the user and confirm before proceeding",
    node_type="event_loop",
    client_facing=True,
    max_node_visits=1,
    input_keys=[],
    output_keys=["medications"],
    system_prompt="""\
You are the intake specialist for a Medication Interaction Checker agent.

**STEP 1 — Collect medications (text only, NO tool calls):**
Ask the user to provide the list of medications they want to check. Be brief:
"Please list the medications you'd like to check for interactions (e.g., Warfarin, Aspirin, Metformin)."

If the user has already provided medications in the conversation, confirm them:
"I'll check interactions for: [list]. Is that correct?"

**STEP 2 — After the user confirms, call set_output:**
- set_output("medications", "<comma-separated list of medication names, e.g. Warfarin, Aspirin, Metformin>")
""",
    tools=[],
)

# Node 2: Research
# Scrapes drug databases to get per-medication profiles and pairwise interactions.
research_node = NodeSpec(
    id="research",
    name="Medication Research",
    description="Research each medication individually and all pairwise interactions by scraping drug databases directly",
    node_type="event_loop",
    max_node_visits=3,
    input_keys=["medications"],
    output_keys=["med_profiles", "interactions"],
    system_prompt="""\
You are a medical research specialist. Research each medication and all pairwise interactions by scraping drug databases directly.

**INPUT:** medications — a comma-separated list of medication names.

**PHASE 1 — Research each medication individually:**
For each medication NAME (lowercase, hyphenated), scrape these URLs in order until you get content:
1. https://www.drugs.com/{name}.html  (e.g. drugs.com/warfarin.html)
2. https://medlineplus.gov/druginfo/meds/a{name}.html

Extract: purpose (1 sentence), top 3-5 common side effects. If a URL fails, try the next.

**PHASE 2 — Research pairwise interactions:**
For every pair (med1, med2), scrape the Drugs.com interaction checker:
https://www.drugs.com/interactions-check.html?drug_list={med1},{med2}

Also try: https://www.drugs.com/drug-interactions/{med1}-{med2}.html

Extract: severity (Major/Moderate/Minor/None known), mechanism (1 sentence), clinical significance (1 sentence), source URL.

Work in batches of 3 web_scrape calls at a time. Skip pairs where both URLs fail and record severity as "Could not retrieve".

**OUTPUT — call set_output in SEPARATE turns:**
- set_output("med_profiles", "<JSON array: [{name, purpose, side_effects}]>")
- set_output("interactions", "<JSON array: [{drug1, drug2, severity, mechanism, significance, source_url}]>")
""",
    tools=["web_scrape"],
)

# Node 3: Report (client-facing)
# Compiles and presents the concise plain-text safety brief.
report_node = NodeSpec(
    id="report",
    name="Safety Brief",
    description="Compile and present a concise plain-text medication safety brief to the user",
    node_type="event_loop",
    client_facing=True,
    max_node_visits=1,
    input_keys=["medications", "med_profiles", "interactions"],
    output_keys=["safety_brief"],
    system_prompt="""\
You are a medication safety brief writer. Compile and present a concise plain-text safety brief.

**STEP 1 — Present the brief (text only, NO tool calls):**

Format it exactly like this — keep every item to one sentence max:

═══════════════════════════════════════
MEDICATION SAFETY BRIEF
═══════════════════════════════════════

MEDICATIONS REVIEWED
─────────────────────
• [Med 1] — [purpose, 1 sentence]
• [Med 2] — [purpose, 1 sentence]

⚠️ DANGEROUS INTERACTIONS (Major)
─────────────────────
• [Med A] + [Med B]: [mechanism]. [significance]. Source: [url]
(If none: "None found.")

⚠️ MODERATE INTERACTIONS (Watch)
─────────────────────
• [Med A] + [Med C]: [mechanism]. Source: [url]
(If none: "None found.")

ℹ️ MINOR / NO INTERACTIONS
─────────────────────
• [pair]: No significant interaction found.

───────────────────────────────────────
⚕️ DISCLAIMER: This is a research aid only. Consult a licensed pharmacist or physician before making any medication changes.
───────────────────────────────────────

**STEP 2 — After presenting, call set_output:**
- set_output("safety_brief", "<the full text of the brief>")
""",
    tools=[],
)

__all__ = [
    "intake_node",
    "research_node",
    "report_node",
]
