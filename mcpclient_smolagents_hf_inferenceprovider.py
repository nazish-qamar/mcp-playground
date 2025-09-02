import gradio as gr
import os

from mcp import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent, ToolCollection, MCPClient

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("HF_TOKEN")

# Adjust timeout parameters here
server_params = {
    "url": "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse",
    "transport": "sse",
    "timeout": 60,           # HTTP request timeout (seconds)
    "sse_read_timeout": 600  # SSE stream read timeout (seconds)
}

try:
    with MCPClient(server_params) as tools:
        # Tools from the remote server are available
        print("\n".join(f"{t.name}: {t.description}" for t in tools))
        model = InferenceClientModel(token=os.getenv("HF_TOKEN"))
        agent = CodeAgent(tools=[*tools], model=model)

        demo = gr.ChatInterface(
            fn=lambda message, history: str(agent.run(message)),
            type="messages",
            examples=["Prime factorization of 68"],
            title="Agent with MCP Tools",
            description="This is a simple agent that uses MCP tools to answer questions."
        )

        demo.launch()

except Exception as e:
    print(f"Error occurred: {e}")
