---
agent: "python-mcp-expert"
description: "Generate a complete MCP server project in Python with tools, resources, and proper configuration"
---

# Generate Python MCP Server

Create a complete Model Context Protocol (MCP) server in Python with the following specifications:

## Requirements

1. **Project Structure**: Create a new Python project with proper structure using uv
2. **Dependencies**: Include the MCP Python SDK 2.x (`mcp>=2,<3`) with uv
3. **Transport Type**: Choose between stdio (for local) or streamable-http (for remote)
4. **Tools**: Create at least one useful tool with proper type hints
5. **Error Handling**: Include comprehensive error handling and validation

## Implementation Details

### Project Setup

- Initialize with `uv init project-name`
- Add MCP SDK: `uv add "mcp>=2,<3"` (and `uv add --optional dev "mcp[cli]>=2,<3"` for `mcp dev`)
- Create main server file (e.g., `server.py`)
- Add `.gitignore` for Python projects
- Configure for direct execution with `if __name__ == "__main__"`

### Server Configuration

- Use `MCPServer` class from `mcp.server.mcpserver` (formerly `FastMCP`; `mcp.server.fastmcp` was removed in 2.x)
- Set server name (positional) and optional instructions (keyword: `instructions=...`)
- Choose transport: stdio (default) or streamable-http
- For HTTP: pass host, port, and stateless mode to `mcp.run(...)`, not to the constructor

### Tool Implementation

- Use `@mcp.tool()` decorator on functions
- Always include type hints - they generate schemas automatically
- Write clear docstrings - they become tool descriptions
- Use Pydantic models or TypedDicts for structured outputs
- Support async operations for I/O-bound tasks
- Include proper error handling

### Resource/Prompt Setup (Optional)

- Add resources with `@mcp.resource()` decorator
- Use URI templates for dynamic resources: `"resource://{param}"`
- Add prompts with `@mcp.prompt()` decorator
- Return strings or Message lists from prompts

### Code Quality

- Use type hints for all function parameters and returns
- Write docstrings for tools, resources, and prompts
- Follow PEP 8 style guidelines
- Use async/await for asynchronous operations
- Implement context managers for resource cleanup
- Add inline comments for complex logic

## Example Tool Types to Consider

- Data processing and transformation
- File system operations (read, analyze, search)
- External API integrations
- Database queries
- Text analysis or generation (with sampling)
- System information retrieval
- Math or scientific calculations

## Configuration Options

- **For stdio Servers**:
  - Simple direct execution
  - Test with `uv run mcp dev server.py`
- **For HTTP Servers**:
  - Port configuration via environment variables
  - Stateless mode for scalability: `mcp.run(transport="streamable-http", stateless_http=True)`
  - JSON response mode: `json_response=True` (also a `run()` argument)
  - CORS configuration for browser clients
  - Mounting to existing ASGI servers (Starlette/FastAPI)

## Testing Guidance

- Explain how to run the server:
  - stdio: `python server.py` or `uv run server.py`
  - HTTP: `python server.py` then connect to `http://localhost:PORT/mcp`
- Test with MCP Inspector: `uv run mcp dev server.py`
- Add a protocol-level test with the in-memory client: `async with Client(mcp, mode="legacy") as client:` (`from mcp.client import Client`)
- Include example tool invocations
- Add troubleshooting tips

## Additional Features to Consider

- Context usage for logging, progress, and notifications
- LLM sampling for AI-powered tools
- User input elicitation for interactive workflows
- Lifespan management for shared resources (databases, connections)
- Structured output with Pydantic models
- Icons for UI display
- Image handling with Image class
- Completion support for better UX

## Best Practices

- Use type hints everywhere - they're not optional
- Return structured data when possible
- Log to stderr (or use Context logging) to avoid stdout pollution
- Clean up resources properly
- Validate inputs early
- Provide clear error messages
- Test tools independently before LLM integration

Generate a complete, production-ready MCP server with type safety, proper error handling, and comprehensive documentation.
