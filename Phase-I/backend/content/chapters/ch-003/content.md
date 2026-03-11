# Chapter 3: Model Context Protocol (MCP)

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand what MCP is and why it was created
- Explain the MCP architecture and key components
- Set up MCP servers and clients
- Connect agents to external data sources via MCP
- Build custom MCP resources and tools

## Introduction to Model Context Protocol

The **Model Context Protocol (MCP)** is an open standard that enables AI models and agents to securely connect to external data sources, tools, and services.

### The Problem MCP Sololves

Before MCP, connecting AI agents to external systems required:
- Custom integrations for each data source
- Managing authentication and security manually
- Building separate connectors for each model
- Handling rate limiting and caching independently

### The MCP Solution

MCP provides:
- **Standardized Interface** - One protocol for all connections
- **Security First** - Sandboxed execution and access control
- **Composable** - Mix and match servers and clients
- **Model Agnostic** - Works with any AI model

## MCP Architecture Overview

### Core Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Agent      │────▶│   MCP Client    │────▶│   MCP Server    │
│   (Claude)      │     │   (SDK)         │     │   (Data Source) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                       │
                               ▼                       ▼
                        Protocol Layer          Resources
                        - JSON-RPC              - Files
                        - Streaming             - Databases
                        - Notifications         - APIs
```

### The Three Pillars of MCP

1. **Resources** - Data that agents can read
   - Files, databases, APIs
   - Read-only access by default
   - Structured or unstructured content

2. **Tools** - Actions that agents can execute
   - Functions with defined schemas
   - Can modify external state
   - Return structured results

3. **Prompts** - Templates for agent interactions
   - Pre-defined conversation patterns
   - Parameterized instructions
   - Consistent behavior enforcement

## Setting Up MCP

### Installation

```bash
# Install the MCP SDK
pip install mcp

# For Python-based servers
pip install mcp[python]
```

### Basic MCP Server Structure

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool

# Create server instance
server = Server("my-data-server")

# Define resources
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="docs://company-handbook",
            name="Company Handbook",
            description="Employee documentation and policies"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "docs://company-handbook":
        return "# Company Handbook\n\nWelcome to our company..."
    raise ValueError(f"Unknown resource: {uri}")

# Define tools
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_handbook",
            description="Search the company handbook",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, args: dict):
    if name == "search_handbook":
        return search_handbook(args["query"])
    raise ValueError(f"Unknown tool: {name}")

# Run the server
async with stdio_server() as streams:
    await server.run(
        streams[0],
        streams[1],
        server.create_initialization_options()
    )
```

## MCP Resources

### What Are Resources?

Resources are data sources that agents can access:
- **File-based**: Documents, code repositories, configs
- **Database**: SQL, NoSQL, graph databases
- **API-based**: REST, GraphQL, gRPC endpoints
- **Streaming**: Real-time data feeds

### Resource URIs

Resources are identified by URIs:
```
file:///path/to/document.md
postgres://localhost/mydb/table
https://api.example.com/v1/endpoint
memory://session/context
```

### Reading Resources

```python
from mcp import Client

client = Client("my-server")

# List available resources
resources = await client.list_resources()
for resource in resources:
    print(f"{resource.uri}: {resource.name}")

# Read a specific resource
content = await client.read_resource("file:///docs/guide.md")
print(content)
```

### Resource Templates

```python
@server.list_resource_templates()
async def list_resource_templates():
    return [
        {
            "uriTemplate": "docs://{category}/{document}",
            "name": "Documentation",
            "description": "Access documentation by category and document name"
        }
    ]

@server.read_resource()
async def read_resource(uri: str):
    # Parse template: docs://api/getting-started
    parts = uri.replace("docs://", "").split("/")
    category = parts[0]
    document = parts[1]
    
    return load_document(category, document)
```

## MCP Tools

### Defining Tools

Tools are functions agents can invoke:

```python
from mcp.types import Tool

tool = Tool(
    name="calculate_quiz_score",
    description="Calculate quiz score percentage",
    inputSchema={
        "type": "object",
        "properties": {
            "correct": {"type": "integer", "description": "Number of correct answers"},
            "total": {"type": "integer", "description": "Total questions"}
        },
        "required": ["correct", "total"]
    }
)
```

### Implementing Tool Handlers

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    if name == "calculate_quiz_score":
        correct = arguments["correct"]
        total = arguments["total"]
        
        if total == 0:
            return [{"type": "text", "text": "Error: Total cannot be zero"}]
        
        percentage = (correct / total) * 100
        return [{
            "type": "text",
            "text": f"Score: {correct}/{total} ({percentage:.1f}%)"
        }]
    
    raise ValueError(f"Unknown tool: {name}")
```

### Tool Result Types

```python
# Text results
return [{"type": "text", "text": "Operation completed"}]

# Image results
return [{
    "type": "image",
    "data": base64_encoded_image,
    "mimeType": "image/png"
}]

# Structured results
return [{
    "type": "resource",
    "resource": {
        "uri": "result://quiz/123",
        "content": {"score": 85, "grade": "B"}
    }
}]
```

## MCP Prompts

### What Are Prompts?

Prompts are pre-defined conversation templates:
- Standardize common interactions
- Include parameter placeholders
- Ensure consistent behavior

### Defining Prompts

```python
@server.list_prompts()
async def list_prompts():
    return [
        {
            "name": "explain_concept",
            "description": "Explain a technical concept at a specified level",
            "arguments": [
                {
                    "name": "concept",
                    "description": "The concept to explain",
                    "required": True
                },
                {
                    "name": "level",
                    "description": "Explanation level (beginner, intermediate, advanced)",
                    "required": False,
                    "default": "intermediate"
                }
            ]
        }
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "explain_concept":
        concept = arguments.get("concept")
        level = arguments.get("level", "intermediate")
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Explain {concept} at a {level} level"
                }
            ],
            "system": f"""You are an expert educator.
            Explain concepts clearly using examples.
            Target audience: {level} level understanding."""
        }
```

## Connecting Agents via MCP

### Client Configuration

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure server parameters
server_params = StdioServerParameters(
    command="python",
    args=["my_mcp_server.py"],
    env={"API_KEY": "secret"}
)

# Connect to server
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize connection
        await session.initialize()
        
        # List available resources
        resources = await session.list_resources()
        
        # List available tools
        tools = await session.list_tools()
        
        # Read a resource
        content = await session.read_resource("file:///data/info.txt")
        
        # Call a tool
        result = await session.call_tool("my_tool", {"arg": "value"})
```

### Multiple Server Connections

```python
from mcp import ClientSession

# Connect to multiple servers
async with (
    stdio_client(file_server_params) as (r1, w1),
    stdio_client(db_server_params) as (r2, w2),
    stdio_client(api_server_params) as (r3, w3)
):
    async with (
        ClientSession(r1, w1) as file_session,
        ClientSession(r2, w2) as db_session,
        ClientSession(r3, w3) as api_session
    ):
        # Agent can now access all three servers
        await file_session.initialize()
        await db_session.initialize()
        await api_session.initialize()
```

## Building an MCP Server for Course Content

### Example: Course Content Server

```python
from mcp.server import Server
from mcp.types import Resource, Tool
import json

server = Server("course-content-server")

# Store course chapters
COURSE_CONTENT = {
    "ch-001": {
        "title": "Introduction to AI Agents",
        "content": open("chapters/ch-001/content.md").read()
    },
    "ch-002": {
        "title": "Claude Agent SDK",
        "content": open("chapters/ch-002/content.md").read()
    }
}

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri=f"course://chapter/{chapter_id}",
            name=chapter["title"],
            description=f"Chapter {chapter_id} content"
        )
        for chapter_id, chapter in COURSE_CONTENT.items()
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri.startswith("course://chapter/"):
        chapter_id = uri.replace("course://chapter/", "")
        if chapter_id in COURSE_CONTENT:
            return COURSE_CONTENT[chapter_id]["content"]
    raise ValueError(f"Resource not found: {uri}")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_chapter_metadata",
            description="Get metadata for a chapter",
            inputSchema={
                "type": "object",
                "properties": {
                    "chapter_id": {"type": "string"}
                },
                "required": ["chapter_id"]
            }
        ),
        Tool(
            name="search_content",
            description="Search course content for keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, args: dict):
    if name == "get_chapter_metadata":
        chapter_id = args["chapter_id"]
        if chapter_id in COURSE_CONTENT:
            return [{
                "type": "text",
                "text": json.dumps({
                    "id": chapter_id,
                    "title": COURSE_CONTENT[chapter_id]["title"]
                })
            }]
    
    elif name == "search_content":
        query = args["query"].lower()
        results = []
        for chapter_id, chapter in COURSE_CONTENT.items():
            if query in chapter["content"].lower():
                results.append(chapter_id)
        return [{
            "type": "text",
            "text": f"Found in chapters: {', '.join(results)}"
        }]
    
    raise ValueError(f"Unknown tool: {name}")
```

## Security Considerations

### Access Control

```python
# Validate user permissions before accessing resources
@server.read_resource()
async def read_resource(uri: str, context):
    user = context.get("user")
    
    if not user.has_permission("read", uri):
        raise PermissionError(f"Access denied to {uri}")
    
    return load_resource(uri)
```

### Input Validation

```python
@server.call_tool()
async def call_tool(name: str, args: dict):
    # Validate all inputs
    if not isinstance(args.get("query"), str):
        raise ValueError("Query must be a string")
    
    if len(args["query"]) > 1000:
        raise ValueError("Query too long")
    
    # Sanitize inputs
    sanitized_query = escape_html(args["query"])
    
    return execute_tool(sanitized_query)
```

### Rate Limiting

```python
from collections import defaultdict
import time

rate_limits = defaultdict(list)

@server.call_tool()
async def call_tool(name: str, args: dict):
    client_id = get_client_id()
    now = time.time()
    
    # Clean old requests
    rate_limits[client_id] = [
        t for t in rate_limits[client_id] if now - t < 60
    ]
    
    # Check rate limit (10 requests per minute)
    if len(rate_limits[client_id]) >= 10:
        raise RateLimitError("Too many requests")
    
    rate_limits[client_id].append(now)
    return execute_tool(name, args)
```

## Best Practices

### 1. Clear Resource Naming

```python
# ❌ Unclear URIs
Resource(uri="data://123", name="Stuff")

# ✅ Clear URIs
Resource(
    uri="course://chapter/ch-001/content",
    name="Introduction to AI Agents - Full Content"
)
```

### 2. Descriptive Tool Documentation

```python
# ❌ Poor documentation
Tool(name="calc", description="Does math")

# ✅ Good documentation
Tool(
    name="calculate_quiz_percentage",
    description="""
    Calculate quiz score as a percentage.
    
    Args:
        correct: Number of correct answers (0-100)
        total: Total number of questions (1-100)
    
    Returns:
        Percentage score rounded to 2 decimal places
    """,
    inputSchema={...}
)
```

### 3. Error Handling

```python
@server.call_tool()
async def call_tool(name: str, args: dict):
    try:
        result = execute_tool(name, args)
        return [{"type": "text", "text": str(result)}]
    except FileNotFoundError as e:
        return [{"type": "text", "text": f"Error: File not found - {e}"}]
    except PermissionError as e:
        return [{"type": "text", "text": f"Error: Access denied - {e}"}]
    except Exception as e:
        return [{"type": "text", "text": f"Error: {str(e)}"}]
```

## Summary

- **MCP** is an open standard for connecting AI agents to external systems
- **Resources** provide read-only access to data sources
- **Tools** enable agents to execute actions and modify state
- **Prompts** standardize common interaction patterns
- **Security** is built-in with access control and validation
- **Composability** allows mixing multiple servers

## Key Terms

- **MCP Server**: Provides resources and tools
- **MCP Client**: Connects to servers on behalf of agents
- **Resource**: Data source agents can read
- **Tool**: Action agents can execute
- **Prompt**: Pre-defined conversation template
- **URI**: Unique identifier for resources

## Next Steps

In Chapter 4, we'll learn how to build **Agent Skills** - reusable capabilities that make your agents more effective and consistent.
