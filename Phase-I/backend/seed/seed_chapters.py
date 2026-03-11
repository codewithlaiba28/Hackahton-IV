#!/usr/bin/env python3
"""
Seed script for course chapters.
Creates 5 chapters for the AI Agent Development course.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.models.chapter import Chapter
from app.database import Base

settings = get_settings()

# Chapter data for AI Agent Development course
CHAPTERS = [
    {
        "id": "ch-001",
        "title": "Introduction to AI Agents",
        "difficulty": "beginner",
        "estimated_read_min": 15,
        "is_free": True,
        "sequence_order": 1,
        "prev_chapter_id": None,
        "next_chapter_id": "ch-002",
        "content": """# Introduction to AI Agents

## What is an AI Agent?

An AI Agent is an autonomous software system that can perceive its environment, make decisions, and take actions to achieve specific goals. Unlike traditional programs that follow fixed instructions, AI agents can adapt their behavior based on changing conditions.

## Key Components of AI Agents

### 1. Perception
Agents gather information from their environment through:
- **Sensors**: Input mechanisms (APIs, cameras, microphones, data feeds)
- **Data Processing**: Converting raw inputs into meaningful information

### 2. Decision Making
Agents process information and choose actions using:
- **Rules**: Predefined if-then logic
- **Machine Learning**: Patterns learned from data
- **LLM Reasoning**: Natural language understanding and generation

### 3. Action
Agents execute decisions through:
- **Actuators**: Output mechanisms (APIs, displays, speakers)
- **Communication**: Sending messages to other systems

## Types of AI Agents

### Simple Reflex Agents
Respond directly to current percepts without considering history.
```python
if temperature > 30:
    turn_on_ac()
```

### Model-Based Agents
Maintain internal state to track aspects of the world.
```python
class ThermostatAgent:
    def __init__(self):
        self.temperature_history = []

    def decide(self, current_temp):
        self.temperature_history.append(current_temp)
        trend = self.calculate_trend()
        return self.make_decision(trend)
```

### Goal-Based Agents
Choose actions to achieve specific objectives.
```python
class NavigationAgent:
    def __init__(self, goal_location):
        self.goal = goal_location

    def decide(self, current_location):
        return self.find_path(current_location, self.goal)
```

### Utility-Based Agents
Maximize a utility function for optimal decisions.
```python
class TradingAgent:
    def decide(self, market_data):
        best_action = None
        best_utility = -float('inf')

        for action in self.possible_actions:
            utility = self.calculate_utility(action, market_data)
            if utility > best_utility:
                best_utility = utility
                best_action = action

        return best_action
```

## Real-World Applications

1. **Personal Assistants**: Siri, Alexa, Google Assistant
2. **Autonomous Vehicles**: Self-driving cars and drones
3. **Recommendation Systems**: Netflix, Spotify, Amazon
4. **Trading Systems**: Algorithmic stock trading
5. **Customer Service**: Chatbots and support agents

## The Future of AI Agents

AI agents are evolving rapidly with advances in:
- **Large Language Models**: Better natural language understanding
- **Multi-Agent Systems**: Collaborative agent networks
- **Embodied AI**: Agents with physical presence (robots)
- **Agentic Workflows**: Autonomous task completion

## Summary

AI agents represent a paradigm shift from traditional programming. Instead of writing explicit instructions, we design agents that can:
- Perceive their environment
- Make autonomous decisions
- Learn and adapt
- Take purposeful actions

This course will teach you how to build practical AI agents using modern tools and frameworks.

---

**Next Chapter**: Claude Agent SDK
"""
    },
    {
        "id": "ch-002",
        "title": "Claude Agent SDK",
        "difficulty": "intermediate",
        "estimated_read_min": 20,
        "is_free": True,
        "sequence_order": 2,
        "prev_chapter_id": "ch-001",
        "next_chapter_id": "ch-003",
        "content": """# Claude Agent SDK

## Overview

The Claude Agent SDK provides a powerful framework for building AI agents powered by Anthropic's Claude models. This chapter covers the fundamentals of creating, configuring, and deploying Claude-based agents.

## Installation

```bash
pip install claude-agent-sdk
```

## Basic Agent Setup

### Creating Your First Agent

```python
from claude_agent import Agent, Tool

# Define a simple agent
agent = Agent(
    name="ResearchAssistant",
    model="claude-sonnet-4-20250514",
    system_prompt="You are a helpful research assistant.",
    tools=[]
)

# Run the agent
response = agent.run("What is quantum computing?")
print(response)
```

### Understanding Agent Components

#### 1. System Prompt
The system prompt defines the agent's behavior and role:
```python
system_prompt = """You are a coding assistant specialized in Python.
- Provide clear, concise explanations
- Include working code examples
- Explain trade-offs when relevant
- Ask clarifying questions when requirements are unclear"""
```

#### 2. Model Selection
Choose the appropriate Claude model:
- **claude-sonnet-4**: Best for most tasks, balanced performance
- **claude-opus-4**: Maximum capability for complex reasoning
- **claude-haiku-4**: Fast and cost-effective for simple tasks

#### 3. Tools
Tools extend agent capabilities:
```python
from claude_agent import Tool

@Tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return perform_search(query)

@Tool
def calculate(expression: str) -> float:
    """Perform mathematical calculations."""
    return eval(expression)

agent = Agent(
    name="MathTutor",
    tools=[search_web, calculate]
)
```

## Advanced Configuration

### Memory Management

```python
from claude_agent import Memory

# Short-term memory (conversation history)
memory = Memory(max_messages=50)

# Long-term memory (persistent storage)
from claude_agent import VectorStore
vector_store = VectorStore(embedding_model="text-embedding-3-small")
long_term_memory = VectorMemory(store=vector_store)

agent = Agent(
    name="PersonalAssistant",
    memory=memory,
    long_term_memory=long_term_memory
)
```

### Custom Handlers

```python
from claude_agent import EventHandler

class LoggingHandler(EventHandler):
    def on_tool_call(self, tool_name: str, args: dict):
        print(f"Calling tool: {tool_name} with args: {args}")

    def on_response(self, response: str):
        print(f"Agent response: {response}")

agent.add_handler(LoggingHandler())
```

## Error Handling

```python
from claude_agent import AgentError, TimeoutError

try:
    response = agent.run("Complex task...", timeout=30)
except TimeoutError:
    print("Agent took too long, retrying...")
except AgentError as e:
    print(f"Agent error: {e}")
    # Implement fallback logic
```

## Best Practices

1. **Clear System Prompts**: Be specific about the agent's role
2. **Tool Design**: Keep tools focused and well-documented
3. **Error Handling**: Always handle potential failures
4. **Testing**: Test agents with diverse inputs
5. **Monitoring**: Log agent behavior for debugging

## Summary

The Claude Agent SDK provides a robust foundation for building AI agents. Key takeaways:
- Agents combine LLM reasoning with tool execution
- System prompts define agent behavior
- Tools extend capabilities
- Memory enables context retention

---

**Next Chapter**: MCP Basics
"""
    },
    {
        "id": "ch-003",
        "title": "MCP Basics",
        "difficulty": "intermediate",
        "estimated_read_min": 18,
        "is_free": True,
        "sequence_order": 3,
        "prev_chapter_id": "ch-002",
        "next_chapter_id": "ch-004",
        "content": """# MCP Basics

## What is Model Context Protocol (MCP)?

Model Context Protocol (MCP) is an open standard that enables AI agents to interact with external tools, data sources, and services through a unified interface. It provides a standardized way for agents to discover and use capabilities.

## Why MCP Matters

### Before MCP
- Each tool required custom integration
- Agents were tightly coupled to specific services
- Adding new capabilities meant code changes

### After MCP
- Standardized tool interface
- Plug-and-play capabilities
- Agents can discover new tools dynamically

## MCP Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Agent     │────▶│   MCP Host  │────▶│ MCP Server  │
│  (Claude)   │◀────│  (Bridge)   │◀────│  (Tools)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Components

1. **Agent**: The AI making requests (e.g., Claude)
2. **MCP Host**: The application managing the agent
3. **MCP Server**: Provides tools and resources

## Setting Up MCP

### Installing MCP

```bash
pip install mcp
```

### Creating an MCP Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server
server = Server("example-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="calculator",
            description="Perform mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculator":
        result = eval(arguments["expression"])
        return [TextContent(type="text", text=str(result))]

# Run server
async with stdio_server() as streams:
    await server.run(
        streams[0],
        streams[1],
        server.create_initialization_options()
    )
```

### Connecting to MCP from Agent

```python
from claude_agent import Agent, MCPConnection

# Connect to MCP server
mcp = MCPConnection(
    command="python",
    args=["mcp_server.py"]
)

agent = Agent(
    name="MCPAgent",
    mcp_connections=[mcp]
)

# Agent can now use MCP tools
response = agent.run("Calculate 2 + 2")
```

## MCP Resources

Resources provide data to agents:

```python
from mcp.types import Resource

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file:///documents/report.pdf",
            name="Monthly Report",
            mimeType="application/pdf"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    # Return resource content
    return [TextContent(type="text", text="Resource content...")]
```

## MCP Prompts

Pre-defined prompt templates:

```python
from mcp.types import Prompt, PromptArgument

@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="code_review",
            description="Review code for best practices",
            arguments=[
                PromptArgument(
                    name="code",
                    description="Code to review",
                    required=True
                )
            ]
        )
    ]
```

## Best Practices

1. **Clear Descriptions**: Document tools thoroughly
2. **Input Validation**: Validate all inputs
3. **Error Messages**: Provide helpful error messages
4. **Security**: Limit tool permissions
5. **Testing**: Test MCP servers independently

## Summary

MCP provides a standardized way for AI agents to interact with tools and data:
- Decouples agents from specific implementations
- Enables dynamic tool discovery
- Simplifies adding new capabilities
- Promotes reusability

---

**Next Chapter**: Agent Skills
"""
    },
    {
        "id": "ch-004",
        "title": "Agent Skills",
        "difficulty": "advanced",
        "estimated_read_min": 25,
        "is_free": False,
        "sequence_order": 4,
        "prev_chapter_id": "ch-003",
        "next_chapter_id": "ch-005",
        "content": """# Agent Skills

## What are Agent Skills?

Agent Skills are predefined capabilities that teach AI agents how to perform specific tasks consistently. Unlike tools (which execute code), skills are behavioral patterns encoded in the agent's system prompt and workflow.

## Skill Architecture

```
┌─────────────────────────────────────────────┐
│                 Agent Skill                  │
├─────────────────────────────────────────────┤
│  • Trigger Keywords                          │
│  • Purpose Statement                         │
│  • Step-by-Step Workflow                     │
│  • Response Templates                        │
│  • Key Principles & Guardrails               │
└─────────────────────────────────────────────┘
```

## Creating a Skill

### Example: Code Review Skill

```markdown
---
name: code-reviewer
description: Reviews code for best practices, bugs, and style
triggers: ["review", "check code", "analyze this"]
---

# Code Reviewer Skill

## Purpose
Provide thorough, constructive code reviews.

## Workflow
1. Read the code carefully
2. Identify strengths
3. Find potential issues
4. Suggest improvements
5. Provide corrected code

## Response Template
**Strengths:**
- [List positive aspects]

**Issues Found:**
- [List problems]

**Suggestions:**
- [List improvements]

**Corrected Code:**
```language
[fixed code]
```
```

## Built-in Skills

### 1. Concept Explainer

```python
from claude_agent.skills import Skill

concept_explainer = Skill(
    name="concept-explainer",
    triggers=["explain", "what is", "how does"],
    workflow=[
        "Identify the concept",
        "Assess user's level",
        "Retrieve relevant content",
        "Construct level-appropriate explanation",
        "Check for understanding"
    ]
)
```

### 2. Quiz Master

```python
quiz_master = Skill(
    name="quiz-master",
    triggers=["quiz", "test me", "practice"],
    workflow=[
        "Determine topic",
        "Fetch questions",
        "Present one question at a time",
        "Provide feedback",
        "Track score",
        "Celebrate progress"
    ]
)
```

### 3. Socratic Tutor

```python
socratic_tutor = Skill(
    name="socratic-tutor",
    triggers=["help me think", "I'm stuck"],
    workflow=[
        "Understand the problem",
        "Ask guiding questions",
        "Never give direct answers",
        "Encourage reasoning",
        "Validate conclusions"
    ]
)
```

## Skill Best Practices

### 1. Clear Triggers
```python
# Good
triggers=["explain", "what is", "how does", "tell me about"]

# Bad - too vague
triggers=["help", "do it"]
```

### 2. Structured Workflow
```python
# Good - specific steps
workflow=[
    "Gather requirements",
    "Validate inputs",
    "Process request",
    "Format output",
    "Confirm satisfaction"
]

# Bad - unclear
workflow=["Do the thing", "Return result"]
```

### 3. Response Templates
```python
# Good - consistent format
template = """
**Summary:** [Brief overview]

**Details:**
- Point 1
- Point 2

**Next Steps:** [Action items]
"""
```

## Implementing Skills in Your Agent

```python
from claude_agent import Agent, Skill

# Load skills
skills = [
    Skill.from_file("skills/concept-explainer.md"),
    Skill.from_file("skills/quiz-master.md"),
    Skill.from_file("skills/socratic-tutor.md"),
]

# Create agent with skills
agent = Agent(
    name="CourseCompanion",
    system_prompt="You are a helpful course companion.",
    skills=skills
)

# Agent automatically uses skills based on triggers
response = agent.run("Explain quantum computing")
# Uses concept-explainer skill
```

## Skill Composition

Combine multiple skills for complex tasks:

```python
from claude_agent import SkillChain

learning_chain = SkillChain([
    concept_explainer,  # First explain
    quiz_master,        # Then test understanding
    socratic_tutor      # Finally, guide deeper thinking
])

agent = Agent(
    name="TutorAgent",
    skill_chain=learning_chain
)
```

## Summary

Agent Skills provide:
- Consistent behavior across interactions
- Reusable behavioral patterns
- Clear trigger-based activation
- Structured workflows
- Quality through templates

---

**Next Chapter**: Agent Factory Architecture
"""
    },
    {
        "id": "ch-005",
        "title": "Agent Factory Architecture",
        "difficulty": "advanced",
        "estimated_read_min": 22,
        "is_free": False,
        "sequence_order": 5,
        "prev_chapter_id": "ch-004",
        "next_chapter_id": None,
        "content": """# Agent Factory Architecture

## Overview

The Agent Factory Architecture is a systematic approach to building AI agents at scale. It separates the concerns of agent specification, manufacturing, and operation.

## Core Principles

### 1. Spec-Driven Development
- Define agent behavior in specifications
- Use natural language for requirements
- Generate code from specs

### 2. Separation of Concerns
- **Spec**: What the agent should do
- **Factory**: How to build the agent
- **Runtime**: Where the agent operates

### 3. Reusability
- Shared skills across agents
- Common infrastructure patterns
- Composable components

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│ L7: A2A Protocol (Multi-Agent Collaboration)        │
├─────────────────────────────────────────────────────┤
│ L6: Runtime Skills + MCP (Domain Knowledge)         │
├─────────────────────────────────────────────────────┤
│ L5: Claude Agent SDK (Agentic Execution)            │
├─────────────────────────────────────────────────────┤
│ L4: OpenAI Agents SDK (High-Level Orchestration)    │
├─────────────────────────────────────────────────────┤
│ L3: FastAPI (HTTP Interface + A2A)                  │
├─────────────────────────────────────────────────────┤
│ L2: Dapr + Workflows (Infrastructure + Durability)  │
├─────────────────────────────────────────────────────┤
│ L1: Apache Kafka (Event Backbone)                   │
├─────────────────────────────────────────────────────┤
│ L0: Agent Sandbox (gVisor) (Secure Execution)       │
└─────────────────────────────────────────────────────┘
```

## Layer Details

### L0: Agent Sandbox
Secure execution environment:
```yaml
runtime: gVisor
isolation: process-level
resources:
  cpu: 2 cores
  memory: 4GB
  network: restricted
```

### L1: Apache Kafka
Event streaming backbone:
```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Agent events
producer.send('agent-events', {
    'agent_id': 'agent-001',
    'event': 'task_started',
    'timestamp': time.time()
})
```

### L2: Dapr + Workflows
Infrastructure abstraction:
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # State management
    client.save_state(
        store_name='agent-state',
        key='agent-001',
        value=json.dumps({'status': 'running'})
    )

    # Workflow orchestration
    client.start_workflow(
        workflow_name='agent-task',
        input={'task_id': '123'}
    )
```

### L3: FastAPI
HTTP interface:
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/agents/{agent_id}/run")
async def run_agent(agent_id: str, task: Task):
    result = await execute_agent(agent_id, task)
    return {"result": result}
```

### L4-L5: Agent SDKs
High-level orchestration:
```python
from openai.agents import Agent
from claude_agent import Agent as ClaudeAgent

# OpenAI agent
oa_agent = Agent(
    name="ResearchAgent",
    instructions="Research and summarize topics"
)

# Claude agent
cl_agent = ClaudeAgent(
    name="CodeAgent",
    system_prompt="Write clean, efficient code"
)
```

### L6: Skills + MCP
Domain knowledge:
```python
skills = [
    Skill(name="code-review", file="skills/code-review.md"),
    Skill(name="testing", file="skills/testing.md"),
]

mcp_servers = [
    MCPServer(command="github-mcp", args=[]),
    MCPServer(command="filesystem-mcp", args=["/workspace"]),
]
```

### L7: A2A Protocol
Multi-agent collaboration:
```python
from a2a import AgentNetwork

network = AgentNetwork([
    ResearchAgent(),
    WriterAgent(),
    ReviewerAgent()
])

# Collaborative task
result = await network.collaborate(
    task="Write a technical article",
    coordination_strategy="sequential"
)
```

## Building an Agent Factory

### Step 1: Define Specification

```yaml
agent:
  name: CourseCompanion
  version: 1.0
  purpose: Educational tutoring

capabilities:
  - content-delivery
  - quiz-management
  - progress-tracking

skills:
  - concept-explainer
  - quiz-master
  - socratic-tutor

deployment:
  environment: production
  replicas: 3
  resources:
    cpu: 2
    memory: 4Gi
```

### Step 2: Generate Agent

```python
from agent_factory import Factory

factory = Factory()

# Generate agent from spec
agent = factory.build_agent("specs/course-companion.yaml")

# Deploy agent
factory.deploy(agent, environment="production")
```

### Step 3: Monitor and Iterate

```python
from agent_factory import Monitor

monitor = Monitor()

# Track agent performance
metrics = monitor.get_metrics("course-companion")

# Update based on feedback
if metrics.error_rate > 0.01:
    factory.update_agent("course-companion", fix="error-handling")
```

## Summary

The Agent Factory Architecture enables:
- Systematic agent development
- Reusable components and patterns
- Scalable deployment
- Continuous improvement

This architecture powers the Course Companion FTE and can be applied to build any AI agent.

---

**End of Course**
"""
    },
]


async def seed_chapters():
    """Seed chapters into the database and local filesystem."""
    # Create engine and session
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Setup local content directory
    content_dir = Path(settings.LOCAL_CONTENT_PATH) / "chapters"
    content_dir.mkdir(parents=True, exist_ok=True)

    async with async_session() as session:
        for chapter_data in CHAPTERS:
            # Check if chapter already exists
            result = await session.execute(
                select(Chapter).where(Chapter.id == chapter_data["id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Chapter {chapter_data['id']} already exists, skipping...")
                continue

            # Save content to local filesystem
            chapter_content_dir = content_dir / chapter_data["id"]
            chapter_content_dir.mkdir(parents=True, exist_ok=True)
            content_file = chapter_content_dir / "content.md"
            content_file.write_text(chapter_data["content"], encoding='utf-8')
            print(f"Saved content for chapter: {chapter_data['id']}")

            # Remove content from dict before creating DB model (content stored in file)
            db_data = {k: v for k, v in chapter_data.items() if k != 'content'}

            # Create chapter in database
            chapter = Chapter(**db_data)
            session.add(chapter)
            print(f"Added chapter to DB: {chapter_data['title']}")

        # Commit all changes
        await session.commit()
        print(f"\nSuccessfully seeded {len(CHAPTERS)} chapters!")
        print(f"Content stored in: {content_dir.absolute()}")


if __name__ == "__main__":
    print("Seeding chapters...")
    asyncio.run(seed_chapters())
