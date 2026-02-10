# soz-ledger-langchain

Soz Ledger integration for [LangChain](https://www.langchain.com/). Automatically records every tool call as a verifiable promise on the Soz Ledger trust protocol.

## Install

```bash
pip install soz-ledger-langchain
```

## Usage

```python
from soz_ledger import SozLedgerClient
from soz_ledger_langchain import SozLedgerCallbackHandler

client = SozLedgerClient(api_key="your_key", base_url="https://api-production-c4c8.up.railway.app")

handler = SozLedgerCallbackHandler(
    client=client,
    agent_entity_id="ent_your_agent",
    promisee_entity_id="ent_user",  # optional, defaults to agent_entity_id
)

# Attach to any LangChain agent or chain
agent.invoke({"input": "..."}, config={"callbacks": [handler]})
```

## How It Works

| LangChain Event | Soz Ledger Action |
|-----------------|-------------------|
| `on_tool_start` | Creates a promise |
| `on_tool_end` | Submits evidence + fulfills promise |
| `on_tool_error` | Submits evidence + breaks promise |

Each tool call gets its own promise, tracked by `run_id` for safe concurrent execution.

## Requirements

- Python >= 3.11
- `soz-ledger >= 0.2.0`
- `langchain-core >= 0.2.0`
