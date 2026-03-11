# Claude Agent SDK

Welcome to the **Claude Agent SDK** chapter. In this section, we will explore how to build autonomous agents using Anthropic's powerful SDK.

## What is an Agent?

An agent is more than just a chatbot. It is a system that can:
1. **Reason** about a task.
2. **Use Tools** to interact with the world.
3. **Execute Loops** until a goal is reached.

## Key Concepts

### 1. Thinking Process
Claude uses a deliberate thinking process to plan its actions. This is often visible in the `thinking` block of the API response.

### 2. Tool Use (Function Calling)
You can provide Claude with a list of tools (functions). Claude will decide which tool to call and with what arguments.

```python
# Example: Defining a tool
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
]
```

## Phase 1 Verification
Remember, in **Phase 1**, all this content is served **verbatim** from our backend. No AI is processing this text on the fly!

### Next Steps
Once you've read this, try navigating back to the chapters list.