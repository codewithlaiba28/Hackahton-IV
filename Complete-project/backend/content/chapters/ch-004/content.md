# Agent Skills

## Memory and State Management

For an AI agent to feel truly "intelligent" and maintain a coherent conversation over time, it must have a way to remember past interactions. This is known as **Memory** and **State Management**.

## Types of Agent Memory

Just like humans, AI agents utilize different types of memory to perform tasks:

### 1. Short-Term Memory (Context)
This refers to information the agent keeps in its "mind" during a single session.
- **Implementation:** Passing the last 5-10 messages back and forth with the LLM.
- **Limitation:** Limited by the "Context Window" of the model (e.g., 200k tokens for Claude).

### 2. Long-Term Memory (Retrieval)
This allows the agent to remember facts, user preferences, or past outcomes across days, weeks, or months.
- **Implementation:** Using **Vector Databases** (like Pinecone, Weaviate, or Chroma) and **RAG (Retrieval-Augmented Generation)**.
- **Process:** The agent "searches" its long-term memory for relevant information before responding.

### 3. State Management (Workflow)
This is about tracking where the agent is in a multi-step process.
- **Implementation:** Storing variables in a database (e.g., `is_authenticated`, `current_step`, `user_goal`).
- **Example:** A tutor agent needs to know which chapters you've finished and which quiz you're currently taking.

---

## Why is Memory Hard?

Managing memory isn't just about storing everything. It requires:
- **Summarization:** Condensing long conversations into key bullet points to save tokens.
- **Relevance:** Only retrieving the *most important* memories for the current context.
- **Forgetting:** Safely deleting sensitive or outdated information.

---

## The Role of the Backend

In a Digital FTE architecture, the **Backend** acts as the agent's external memory. While the LLM "thinks" about the current message, the backend:
1.  **Fetches** the user's profile and progress.
2.  **Retrieves** relevant course content based on the query.
3.  **Saves** the outcome of the interaction for future use.

Without robust state management, an agent is just a stateless text box. With it, it becomes a personalized, persistent companion.