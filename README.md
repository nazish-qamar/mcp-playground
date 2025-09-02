# mcp-playground

## installing dependency
### command: uv pip install "mcp[cli]"
## starting server
### command: mcp dev server.py
##
## case 1. running tiny agents - using external mcp server
## When we don't write a server, but instead use an existing MCP server, like package published to npm (@playwright/mcp).
## So, in this case in our agent.json, we tell tiny-agents:
## “When I run this agent, start this external MCP server via npx and expose its tools to me.”
## So the agent had access to the tools that Playwright’s MCP server provides (browser automation, 
## scraping, etc.).
### command: tiny-agents run agent.json
##
## case 2. write our own MCP server by making a Gradio app with demo.launch(mcp_server=True).
## That automatically exposes our letter_counter function as a tool, accessible to any MCP-compatible client.
## Now tiny-agents connects to our server (instead of a third-party one) and can use our tool.
## with this setup now we have to option- 1) A Gradio UI; and 2) MCP Server that can be connected to compatible clients
## step1: running the server: python gradio_server_app.py
## step2: run the gradio application: directly visit the link http://127.0.0.1:7860
## or run the tiny agent defined in letter_counter_agents.json by 
### command: tiny-agents run letter_counter_agents.json
### To view the schema, visit - http://127.0.0.1:7860/gradio_api/mcp/schema

## For testing with continue.dev
### I had to create ".continue\mcpServers" dir and add sentiment-analysis.yaml file
### next create ".continue\mcpServers" and add local-models.yaml, where I added configuration for ollama running locally 

## MCP Client with smolagent
### If you are huggingface pro user or still have free credits then can use inferenceprovider from huggingface. Example in mcpclient_smolagents_hf_inferenceprovider.py

### Alternatively use local ollama model. Example in mcpclient_smolagents_ollama_model.py. Need to install smolagents[litellm] first.