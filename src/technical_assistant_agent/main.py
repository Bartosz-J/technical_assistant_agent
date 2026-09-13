from technical_assistant_agent.agent.agent import Agent
from technical_assistant_agent.llm.llm import LLM
from technical_assistant_agent.tools.registry import ToolRegistry

def main():
    llm = LLM()
    tool_registry = ToolRegistry()

    agent = Agent(
        llm = llm,
        tools = tool_registry
    )

    print(tool_registry.list_tools)

    print("koniec")

if __name__ == '__main__':
    main()

