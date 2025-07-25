# main.py
from agents.root_agent import get_agent
from adk_local import RuntimeContext

async def main():
    agent = get_agent()
    task = input("🧠 Enter your task: ")
    context = RuntimeContext(task)
    await agent.run(context)
    print("✅ Final Output:\n", context.output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

