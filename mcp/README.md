# MCP Server & Client Demo

This directory contains a Model Context Protocol (MCP) server and client demonstration using the OpenAI Agents SDK.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that allows AI models to securely interact with external tools, data sources, and services. It provides a standardized way for AI agents to discover and use capabilities exposed by servers.

## Files

### `mcp-server.py` - MCP Server

A simple MCP server built with FastMCP that exposes:

| Type | Name | Description |
|------|------|-------------|
| Tool | `add(a, b)` | Adds two numbers and returns the result |
| Resource | `hello://{name}` | Returns a personalized greeting message |

### `mcp-client.py` - MCP Client (Agent)

An AI agent that connects to the MCP server and uses its tools:

- Uses OpenAI's GPT-3.5-turbo model
- Connects to the server via SSE (Server-Sent Events)
- Demonstrates tool usage with two example queries:
  - Adding numbers (7 + 22)
  - Requesting a personalized greeting for "Jack"
- Includes OpenAI tracing for debugging and observability

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key

## Setup

1. **Install dependencies** (from the project root):

   ```bash
   uv sync
   ```

2. **Set your OpenAI API key:**

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

## Running

You need two terminals - one for the server and one for the client.

### Terminal 1: Start the MCP Server

```bash
uv run mcp run mcp/mcp-server.py --transport sse
```

The server will start on `http://localhost:8000` and expose an SSE endpoint at `/sse`.

### Terminal 2: Run the MCP Client

```bash
uv run python mcp/mcp-client.py
```

## Expected Output

When running the client, you should see output similar to:

```
View trace: https://platform.openai.com/traces/trace?trace_id=...

Running: Add the two numbers: 7 and 22.
29

Running: Can you say hello to Jack?
Hello, Jack!
```

The trace URL allows you to view detailed execution logs on the OpenAI platform.
