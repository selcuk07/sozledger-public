# soz-ledger-crewai

Soz Ledger integration for [CrewAI](https://www.crewai.com/). Automatically records every completed task as a verifiable promise on the Soz Ledger trust protocol.

## Install

```bash
pip install soz-ledger-crewai
```

## Usage

```python
from crewai import Task
from soz_ledger import SozLedgerClient
from soz_ledger_crewai import soz_task_callback

client = SozLedgerClient(api_key="your_key", base_url="https://api-production-c4c8.up.railway.app")

callback = soz_task_callback(
    client,
    agent_entity_id="ent_your_agent",
    promisee_entity_id="ent_user",  # optional, defaults to agent_entity_id
)

task = Task(description="Summarise the quarterly report", callback=callback)
```

## How It Works

When a CrewAI task completes successfully, the callback:

1. Creates a promise with the task description
2. Submits evidence with the agent name and output preview
3. Fulfills the promise

One promise per completed task -- clean and reliable.

## Requirements

- Python >= 3.11
- `soz-ledger >= 0.2.0`
- `crewai >= 0.80.0`
