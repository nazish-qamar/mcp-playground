import gradio as gr
import os
from smolagents import InferenceClientModel, CodeAgent, ToolCollection, MCPClient
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("HF_TOKEN")
if not token:
    raise ValueError("Please set HF_TOKEN in your .env file or environment")

# Initialize MCP client and tools outside the context manager
def initialize_agent():
    try:
        mcp_client = MCPClient({"url": "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse"})
        mcp_client.connect()  # Explicitly connect
        tools = mcp_client.get_tools()
        
        model = InferenceClientModel(token=token)
        agent = CodeAgent(
            tools=[*tools], 
            model=model, 
            additional_authorized_imports=["json", "ast", "urllib", "base64"]
        )
        
        return agent, mcp_client
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return None, None

# Initialize the agent and client
agent, mcp_client = initialize_agent()

if agent is None:
    raise RuntimeError("Failed to initialize the agent and MCP client")

def chat_fn(message, history):
    try:
        response = agent.run(message)
        return str(response)
    except Exception as e:
        return f"Error: {str(e)}"

# Create the Gradio interface
demo = gr.ChatInterface(
    fn=chat_fn,
    type="messages",
    examples=["Analyze the sentiment of the following text 'This is awesome'"],
    title="Agent with MCP Tools",
    description="This is a simple agent that uses MCP tools to answer questions.",
)

if __name__ == "__main__":
    try:
        demo.launch()
    finally:
        # Clean up the MCP client when the app shuts down
        if mcp_client:
            mcp_client.disconnect()