import gradio as gr
import os

from mcp import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent, ToolCollection, MCPClient, LiteLLMModel, PromptTemplates

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("HF_TOKEN")

from smolagents import (
    PromptTemplates,
    PlanningPromptTemplate,
    ManagedAgentPromptTemplate,
    FinalAnswerPromptTemplate,
)

custom_prompts = PromptTemplates(
    system_prompt="You are a helpful coding agent. Always respond with valid Python code inside <code> ... </code> tags.",
    planning=PlanningPromptTemplate(
        initial_plan="Think step by step about how to solve the task.",
        update_plan_pre_messages="Before updating plan, reflect.",
        update_plan_post_messages="After updating plan, refine approach.",
    ),
    managed_agent=ManagedAgentPromptTemplate(
        task="Use tools when needed, otherwise solve directly with code.",
        report="Explain briefly what you are doing before giving code.",
    ),
    final_answer=FinalAnswerPromptTemplate(
        pre_messages="When you are ready to give the final result, format it like this:",
        post_messages="""Final answer:
<code>
{answer}
</code>""",
    ),
)

print(type(custom_prompts))  # still dict (TypedDict)
print(type(custom_prompts['planning']))  # should be PlanningPromptTemplate


# Adjust timeout parameters here
server_params = {
    "url": "https://nazish-qamar-sentiment-prediction.hf.space/gradio_api/mcp/sse",
    "transport": "sse",
    "timeout": 60,           # HTTP request timeout (seconds)
    "sse_read_timeout": 600  # SSE stream read timeout (seconds)
}

try:
    mcp_client = MCPClient(server_params)
    tools = mcp_client.get_tools()
    print("\n".join(f"{t.name}: {t.description}" for t in tools))

    model = LiteLLMModel(
        model_id="ollama/gemma3:1b",       # any identifier you like
        api_base="http://localhost:11434"  # local Ollama server
    )
    print(type(custom_prompts))
    agent = CodeAgent(tools=[*tools], 
                        model=model, 
                        prompt_templates=custom_prompts)

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=["Type the sentence with the tool name"],
        title="Agent with MCP Tools",
        description="This is a simple agent that uses MCP tools to evaluate the sentiment of text."
    )

    demo.launch()

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    mcp_client.disconnect()
