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
    system_prompt=(
        "You are a coding agent with two Python functions available:\n"
        " - letter_counter(word: str, letter: str) -> int\n"
        " - reverse_text(text: str) -> str\n\n"
        "RULES (must follow exactly):\n"
        "1) Never import any module. Never reference files.\n"
        "2) Never use Markdown code fences (no ``` anywhere).\n"
        "3) When you need to run code, output a SINGLE block wrapped ONLY with <code> and </code>.\n"
        "4) Inside <code>…</code> put PURE Python lines; no commentary, no backticks, no language tags.\n"
        "5) Always print the final value (e.g., result = ...; print(result))."
    ),
    planning=PlanningPromptTemplate(
        initial_plan="Decide whether to call reverse_text or letter_counter, then write minimal Python.",
        update_plan_pre_messages="Confirm which function is needed; ensure no markdown fences.",
        update_plan_post_messages="Produce a single <code>…</code> block that prints the answer."
    ),
    managed_agent=ManagedAgentPromptTemplate(
        task="Use ONLY the provided functions. No imports. No backticks.",
        report="State which function you call, then provide a single <code>…</code> block."
    ),
    final_answer=FinalAnswerPromptTemplate(
        pre_messages="Return the final value ONLY, wrapped exactly as below:",
        post_messages=(
            "Final answer:\n"
            "<code>\n"
            "{answer}\n"
            "</code>"
        ),
    ),
)

# Adjust timeout parameters here
server_params = {
    "url": "https://nazish-qamar-word-operations.hf.space/gradio_api/mcp/sse",
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
                        prompt_templates=custom_prompts
                    )

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=["Type the question"],
        title="Agent with MCP Tools",
        description="This is a simple agent that uses MCP tools to create the response."
    )

    demo.launch()

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    mcp_client.disconnect()
