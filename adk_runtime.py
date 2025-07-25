# adk_runtime.py
import asyncio

class RuntimeContext:
    def __init__(self, task, llm, memory, logger):
        self.task, self.llm, self.memory, self.logger = task, llm, memory, logger

    def complete(self, output): self.output = output

    async def call(self, agent_name, task):
        # dynamically import agent module
        mod = __import__(f"agents.{agent_name}", fromlist=['get_agent'])
        return await mod.get_agent().run_with_adk(task, config={'llm': self.llm})
