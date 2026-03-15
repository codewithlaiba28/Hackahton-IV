# Claude Agent SDK

## Agent Architecture Patterns

Building an effective AI agent requires more than just an LLM and a prompt. It requires a structured **architecture** that determines how the agent processes information and interacts with its environment.

## The Taxonomy of Agents

In classical AI, agents are often categorized by their internal reasoning structure. Modern AI agents (LLM-powered) can be mapped to these same categories:

### 1. Simple Reflex Agents
These agents respond directly to perceptions based on a set of condition-action rules.
- **Classic:** If sensor detects heat, turn on cooling.
- **Modern LLM:** A chatbot that uses basic keyword matching to trigger specific pre-written responses.
- **Pros:** Fast, low latency.
- **Cons:** No memory, cannot handle complex reasoning.

### 2. Model-Based Reflex Agents
These agents maintain an internal state (a "model") of the world. They keep track of things that aren't currently visible.
- **Concept:** They remember what happened before and use that context for current decisions.
- **Modern LLM:** Agents that use **short-term memory** (last few turns of conversation) to inform their next response.

### 3. Goal-Based Agents
Instead of just responding to rules, these agents have a specific **goal** they are trying to achieve.
- **Concept:** They consider "Will this action lead me closer to my goal?"
- **Modern LLM:** Task-oriented agents that use **Chain-of-Thought (CoT)** reasoning to plan multiple steps to solve a user's request.

### 4. Utility-Based Agents
These are the most sophisticated. They don't just have a goal; they have a "utility function" that measures *how well* they are achieving it.
- **Concept:** If multiple paths lead to a goal, they choose the most efficient, cheapest, or safest one.
- **Modern LLM:** Agents that use **Self-Reflection** or **Tree-of-Thoughts** to evaluate multiple possible plans and select the optimal one.

---

## The Modern LLM-Agent Stack

In the context of this hackathon, our agents utilize a hybrid approach:
1.  **Orchestrator:** The LLM that plans and reasons.
2.  **Perception Layer:** Tools that fetch data (R2 storage, Search APIs).
3.  **Action Layer:** Tools that execute tasks (writing to DB, sending emails).
4.  **Memory Layer:** Persistent state across sessions.

Understanding these patterns is crucial for designing Digital FTEs that are reliable, efficient, and capable of handling complex, real-world workflows.