# MCP Basics

# Tool Use and Function Calling

One of the most powerful capabilities of modern AI agents is their ability to interact with the external world through **Tool Use** (also known as **Function Calling**). This transforms an LLM from a simple text generator into an active problem solver.

## What is Tool Use?

Tool use is the mechanism by which an LLM can request the execution of a specific function or API call. Instead of just answering a question, the agent can say: *"To answer this, I need to fetch the current weather/search a database/calculate a mortgage rate. Here is the tool I want to use and the parameters I'm providing."*

---

## How it Works: The Protocol

The workflow for tool use typically follows these steps:

1.  **System Definition:** You provide the LLM with a list of available tools, including their names, descriptions, and required input parameters (schema).
2.  **User Request:** The user asks a question that requires external data or action.
3.  **Tool Selection:** The LLM decides which tool is appropriate and generates a "tool call" (structured JSON).
4.  **Execution:** Your backend (not the LLM) executes the requested function using the provided parameters.
5.  **Observation:** The result of the function (output) is sent back to the LLM.
6.  **Final Response:** The LLM integrates the tool output into its internal reasoning to provide a final, grounded answer to the user.

---

## Real-World Use Cases

- **Real-Time Data Retrieval:** Fetching stock prices, weather, or news—things the LLM wasn't trained on.
- **Database Interaction:** Querying a customer's order history or updating a user's subscription tier.
- **Action Execution:** Sending an email, creating a calendar event, or triggering a CI/CD pipeline.
- **Computation:** Performing complex math or data analysis that the LLM might hallucinate on if done natively.

---

## Constitutional Best Practices

When designing tools for your Course Companion FTE, follow these guardrails:
- **Describe Tools Clearly:** The LLM relies on the description to know *when* and *how* to use the tool.
- **Handle Errors Gracefully:** What happens if an API call fails? The agent should know how to interpret the error and inform the user.
- **Security First:** Never give an agent unlimited access. Use "human-in-the-loop" for destructive actions (like deleting data).

In the next chapters, we will explore how to manage the **Memory** that stores the results of these tool interactions.