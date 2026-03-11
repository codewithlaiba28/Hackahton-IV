# Chapter 2: Claude Agent SDK

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the purpose and architecture of the Claude Agent SDK
- Set up the Claude Agent SDK in your development environment
- Create your first AI agent using the SDK
- Configure agent behaviors and capabilities
- Implement basic agent workflows

## Introduction to Claude Agent SDK

The **Claude Agent SDK** is a comprehensive framework for building AI agents powered by Anthropic's Claude models. It provides:

1. **Agent Orchestration** - Manage agent lifecycles and state
2. **Tool Integration** - Connect agents to external APIs and services
3. **Memory Management** - Handle short-term and long-term memory
4. **Streaming Support** - Real-time token streaming for responsive UX
5. **Error Handling** - Robust retry and fallback mechanisms

## Why Use the Claude Agent SDK?

### Benefits Over Direct API Calls

| Direct API | Claude Agent SDK |
|------------|------------------|
| Manual state management | Built-in state tracking |
| Custom retry logic | Production-ready error handling |
| No tool abstraction | Unified tool interface |
| Manual token counting | Automatic context management |
| Single-turn focused | Multi-turn conversation support |

## Core Concepts

### 1. Agent

An Agent is the primary abstraction - an autonomous entity that:
- Maintains conversation history
- Has access to tools and resources
- Makes decisions based on instructions
- Executes multi-step workflows

### 2. Tools

Tools are functions that agents can invoke:
- **Built-in Tools**: File operations, web search, code execution
- **Custom Tools**: Your own Python functions
- **MCP Tools**: Model Context Protocol integrations

### 3. Sessions

Sessions represent individual agent conversations:
- Maintain context across turns
- Store conversation history
- Track tool usage and results

### 4. Instructions

Instructions define agent behavior:
- System-level directives
- Task-specific guidance
- Constraint enforcement rules

## Installation and Setup

### Prerequisites

- Python 3.12 or higher
- Anthropic API key
- Virtual environment (recommended)

### Installation Steps

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the SDK
pip install claude-agent-sdk

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Creating Your First Agent

### Basic Agent Setup

```python
from claude_agent import Agent, Session

# Create an agent with basic configuration
agent = Agent(
    name="Course Companion",
    model="claude-sonnet-4-5-20250929",
    instructions="""You are a helpful educational tutor.
    - Explain concepts clearly and patiently
    - Adapt to the student's level
    - Use examples and analogies
    - Encourage questions and curiosity"""
)

# Start a new session
session = Session(agent=agent)

# Interact with the agent
response = session.send("What is an AI agent?")
print(response.content)
```

### Adding Tools to Your Agent

```python
from claude_agent import Agent, Tool

# Define a custom tool
@Tool
def calculate_percentage(correct: int, total: int) -> float:
    """Calculate quiz score percentage."""
    return (correct / total) * 100 if total > 0 else 0

# Create agent with tools
agent = Agent(
    name="Quiz Master",
    tools=[calculate_percentage],
    instructions="You are a quiz master. Use the calculate_percentage tool to grade quizzes."
)
```

## Agent Configuration Options

### Model Selection

```python
# Different Claude models for different use cases
agent = Agent(
    name="Flexible Agent",
    model="claude-sonnet-4-5-20250929",  # Balanced performance
    # model="claude-opus-4-0-20250514",  # Maximum capability
    # model="claude-haiku-3-5-20250101", # Fast and cost-effective
)
```

### Context Window Management

```python
agent = Agent(
    name="Memory-Aware Agent",
    max_tokens=4096,  # Maximum response length
    context_limit=100000,  # Maximum context window
    truncate_strategy="drop_oldest"  # How to handle overflow
)
```

### Temperature and Sampling

```python
agent = Agent(
    name="Creative Tutor",
    temperature=0.7,  # Higher = more creative
    top_p=0.9,  # Nucleus sampling
    top_k=40,  # Sample from top k tokens
)
```

## Multi-Turn Conversations

### Maintaining Context

```python
session = Session(agent=agent)

# First turn
response1 = session.send("I want to learn about AI agents")
print(response1.content)

# Second turn - agent remembers context
response2 = session.send("Can you explain the perception module?")
print(response2.content)

# Third turn - builds on previous explanations
response3 = session.send("How does that relate to reasoning?")
print(response3.content)
```

### Handling Long Conversations

```python
# Automatic context management
session = Session(
    agent=agent,
    max_history_turns=50,  # Keep last 50 turns
    summary_enabled=True,  # Summarize older turns
)
```

## Error Handling and Retries

### Built-in Retry Logic

```python
from claude_agent import Agent, RetryConfig

agent = Agent(
    name="Reliable Agent",
    retry_config=RetryConfig(
        max_retries=3,
        backoff_factor=2,
        retry_on_timeout=True,
        retry_on_rate_limit=True
    )
)
```

### Custom Error Handlers

```python
from claude_agent import Agent, ErrorHandler

@ErrorHandler
def handle_rate_limit(error):
    """Handle API rate limit errors."""
    print("Rate limited. Waiting before retry...")
    time.sleep(60)
    return True  # Indicates retry should happen

agent = Agent(
    name="Resilient Agent",
    error_handlers=[handle_rate_limit]
)
```

## Streaming Responses

### Real-time Token Streaming

```python
from claude_agent import Agent, Session

agent = Agent(name="Streaming Agent")
session = Session(agent=agent)

# Stream the response token by token
for chunk in session.stream("Explain quantum computing"):
    print(chunk.content, end="", flush=True)
```

### Progress Indicators

```python
for chunk in session.stream("Write a long essay"):
    if chunk.type == "progress":
        print(f"\rProgress: {chunk.tokens_generated} tokens", end="")
    elif chunk.type == "content":
        print(chunk.content, end="")
```

## Best Practices

### 1. Clear Instructions

```python
# ❌ Vague instructions
instructions = "Be helpful"

# ✅ Specific instructions
instructions = """
You are an educational tutor for AI agent development.
- Always explain concepts using concrete examples
- Check for understanding after each explanation
- Adapt complexity to the student's demonstrated level
- Never provide code without explaining how it works
"""
```

### 2. Tool Documentation

```python
# ❌ Poor tool documentation
@Tool
def calc(a, b):
    return a + b

# ✅ Well-documented tool
@Tool
def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number to add
        b: Second number to add
    
    Returns:
        The sum of a and b
    
    Example:
        add_numbers(5, 3) -> 8
    """
    return a + b
```

### 3. Context Management

```python
# ❌ Letting context grow unbounded
session = Session(agent)

# ✅ Managing context size
session = Session(
    agent=agent,
    max_history_turns=20,
    auto_summarize=True,
    summary_interval=10  # Summarize every 10 turns
)
```

## Common Use Cases

### Educational Tutor

```python
tutor = Agent(
    name="Course Companion",
    model="claude-sonnet-4-5-20250929",
    instructions="""You are a patient educational tutor.
    - Break down complex topics into manageable pieces
    - Use analogies relevant to the student's background
    - Ask questions to check understanding
    - Provide encouragement and positive feedback""",
    tools=[search_knowledge_base, calculate_score, track_progress]
)
```

### Code Reviewer

```python
reviewer = Agent(
    name="Code Review Assistant",
    instructions="""You are an expert code reviewer.
    - Identify bugs and security issues
    - Suggest performance improvements
    - Explain the reasoning behind each suggestion
    - Provide corrected code examples""",
    tools=[read_file, write_file, run_tests, check_syntax]
)
```

### Research Assistant

```python
researcher = Agent(
    name="Research Helper",
    instructions="""You are a research assistant.
    - Search for relevant academic papers
    - Summarize key findings
    - Track citations and references
    - Identify research gaps""",
    tools=[search_papers, extract_citations, summarize_pdf]
)
```

## Debugging Agents

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = Agent(
    name="Debug Agent",
    enable_logging=True,
    log_level="DEBUG"
)
```

### Inspect Agent State

```python
session = Session(agent=agent)
session.send("Hello")

# Inspect conversation history
print(session.history)

# View tool calls
print(session.tool_calls)

# Check token usage
print(session.token_usage)
```

## Summary

- The **Claude Agent SDK** provides a production-ready framework for building AI agents
- **Agents** maintain state, use tools, and follow instructions
- **Sessions** manage multi-turn conversations with automatic context handling
- **Tools** extend agent capabilities with custom functions and external APIs
- **Streaming** enables responsive real-time user experiences
- **Error handling** and **retry logic** are built-in for reliability

## Key Terms

- **Agent**: Autonomous entity powered by Claude
- **Session**: Individual conversation with context tracking
- **Tool**: Function that agents can invoke
- **Instructions**: Directives that define agent behavior
- **Streaming**: Real-time token-by-token response delivery

## Next Steps

In Chapter 3, we'll explore the **Model Context Protocol (MCP)** and learn how to connect your agents to external data sources and tools.
