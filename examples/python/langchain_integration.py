"""
Soz Ledger -- LangChain Integration Example
=============================================
Shows how to attach SozLedgerCallbackHandler to a LangChain agent so that
every tool call is automatically recorded as a verifiable promise.

Requirements:
    pip install soz-ledger soz-ledger-langchain langchain langchain-openai
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from soz_ledger import SozLedgerClient
from soz_ledger_langchain import SozLedgerCallbackHandler


# ── 1. Define a simple tool ──────────────────────────────────────────────────
@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Top result for '{query}': Example page about AI trust protocols."


# ── 2. Set up Soz Ledger ─────────────────────────────────────────────────────
def main():
    client = SozLedgerClient(
        api_key="your_api_key",
        base_url="https://api-production-c4c8.up.railway.app",
    )

    # Register entities
    agent_entity = client.entities.create(
        name="langchain-research-agent",
        type="agent",
        metadata={"framework": "langchain", "model": "gpt-4o"},
    )
    user_entity = client.entities.create(name="demo-user", type="human")

    # ── 3. Create the callback handler ────────────────────────────────────────
    handler = SozLedgerCallbackHandler(
        client=client,
        agent_entity_id=agent_entity.id,
        promisee_entity_id=user_entity.id,
    )

    # ── 4. Build a LangChain agent with the handler ───────────────────────────
    llm = ChatOpenAI(model="gpt-4o")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful research assistant."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, [search_web], prompt)
    executor = AgentExecutor(agent=agent, tools=[search_web])

    # Every tool call the agent makes will now create a Soz Ledger promise
    result = executor.invoke(
        {"input": "Find information about AI trust protocols"},
        config={"callbacks": [handler]},
    )
    print(f"Agent output: {result['output']}")

    # ── 5. Check trust score ──────────────────────────────────────────────────
    score = client.scores.get(agent_entity.id)
    print(f"\nTrust profile for '{agent_entity.name}':")
    print(f"  Level         : {score.level}")
    print(f"  Overall score : {score.overall_score}")
    print(f"  Fulfilled     : {score.fulfilled_count}")
    print(f"  Broken        : {score.broken_count}")

    client.close()


if __name__ == "__main__":
    main()
