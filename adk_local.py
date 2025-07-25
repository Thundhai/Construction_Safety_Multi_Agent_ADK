# adk_local.py

import asyncio
import importlib

class RuntimeContext:
    def __init__(self, task=None, llm=None, memory=None, logger=None):
        self.task = task or {}
        self.input = task  # agents expect context.input
        self.output = None
        self.llm = llm or SimpleLLM()
        self.memory = memory or {}
        self.logger = logger or SimpleLogger()

    def complete(self, output):
        self.output = output

    async def call(self, agent_name, task):
        module = importlib.import_module(f"{agent_name}")
        agent = module.get_agent()
        ctx = RuntimeContext(task, llm=self.llm, memory=self.memory, logger=self.logger)
        await agent.run(ctx)
        return ctx

class SimpleLLM:
    async def complete(self, prompt):
        class R: text = f"[Stub LLM] Response to prompt: {prompt}"
        return R()

class SimpleLogger:
    def info(self, msg): print(f"[INFO] {msg}")
    def warning(self, msg): print(f"[WARNING] {msg}")
    def error(self, msg): print(f"[ERROR] {msg}")

