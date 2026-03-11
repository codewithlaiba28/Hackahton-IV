#!/usr/bin/env python3
"""
Simple seed script for quiz questions.
Creates quiz questions for all 5 chapters.
"""

import asyncio
import sys
import uuid
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.models import QuizQuestion  # Import from models package
from app.database import Base

settings = get_settings()

# Quiz data for all chapters
QUIZZES = [
    # Chapter 1: Introduction to AI Agents
    {
        "chapter_id": "ch-001",
        "questions": [
            {
                "question_text": "What are the three key components of an AI agent?",
                "question_type": "mcq",
                "options": [
                    "Input, Process, Output",
                    "Perception, Decision Making, Action",
                    "Sensors, CPU, Actuators",
                    "Data, Algorithm, Result"
                ],
                "correct_answer": "Perception, Decision Making, Action",
                "explanation": "AI agents perceive their environment, make decisions based on that perception, and take actions to achieve goals."
            },
            {
                "question_text": "A simple reflex agent responds directly to current percepts without considering history.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Simple reflex agents use condition-action rules based only on current percepts, not historical data."
            },
            {
                "question_text": "Which type of agent maintains internal state to track aspects of the world?",
                "question_type": "mcq",
                "options": [
                    "Simple Reflex Agent",
                    "Model-Based Agent",
                    "Goal-Based Agent",
                    "Utility-Based Agent"
                ],
                "correct_answer": "Model-Based Agent",
                "explanation": "Model-based agents maintain internal state (a model of the world) to handle partially observable environments."
            },
            {
                "question_text": "What is the primary difference between goal-based and utility-based agents?",
                "question_type": "mcq",
                "options": [
                    "Goal-based agents are faster",
                    "Utility-based agents maximize a satisfaction measure",
                    "Goal-based agents use machine learning",
                    "There is no difference"
                ],
                "correct_answer": "Utility-based agents maximize a satisfaction measure",
                "explanation": "Goal-based agents work towards a binary goal (achieved/not achieved), while utility-based agents maximize a utility function for optimal decisions."
            },
            {
                "question_text": "AI agents can only be implemented using machine learning algorithms.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "AI agents can be implemented using various approaches including simple rules, search algorithms, and machine learning. ML is not required."
            }
        ]
    },
    # Chapter 2: Claude Agent SDK
    {
        "chapter_id": "ch-002",
        "questions": [
            {
                "question_text": "Which Claude model is best for most tasks with balanced performance?",
                "question_type": "mcq",
                "options": [
                    "claude-opus-4",
                    "claude-sonnet-4",
                    "claude-haiku-4",
                    "claude-instant-4"
                ],
                "correct_answer": "claude-sonnet-4",
                "explanation": "Claude Sonnet 4 provides the best balance of performance and cost for most use cases."
            },
            {
                "question_text": "What is the purpose of a system prompt in Claude Agent SDK?",
                "question_type": "mcq",
                "options": [
                    "To authenticate the API",
                    "To define the agent's behavior and role",
                    "To configure network settings",
                    "To set rate limits"
                ],
                "correct_answer": "To define the agent's behavior and role",
                "explanation": "The system prompt establishes the agent's persona, capabilities, and behavioral guidelines."
            },
            {
                "question_text": "Tools in Claude Agent SDK are used to:",
                "question_type": "mcq",
                "options": [
                    "Debug the agent",
                    "Extend agent capabilities with external functions",
                    "Monitor performance",
                    "Manage memory"
                ],
                "correct_answer": "Extend agent capabilities with external functions",
                "explanation": "Tools allow agents to perform actions beyond text generation, such as API calls, calculations, or data retrieval."
            },
            {
                "question_text": "Memory management in Claude Agent SDK only supports short-term conversation history.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "The SDK supports both short-term memory (conversation history) and long-term memory (persistent vector storage)."
            },
            {
                "question_text": "What should you always implement when working with Claude agents?",
                "question_type": "mcq",
                "options": [
                    "Custom UI",
                    "Error handling",
                    "Database connections",
                    "Caching layer"
                ],
                "correct_answer": "Error handling",
                "explanation": "Error handling is essential for robust agent implementations to handle timeouts, API failures, and unexpected responses."
            }
        ]
    },
    # Chapter 3: MCP Basics
    {
        "chapter_id": "ch-003",
        "questions": [
            {
                "question_text": "What does MCP stand for?",
                "question_type": "mcq",
                "options": [
                    "Machine Communication Protocol",
                    "Model Context Protocol",
                    "Multi-Channel Processing",
                    "Modular Component Platform"
                ],
                "correct_answer": "Model Context Protocol",
                "explanation": "MCP (Model Context Protocol) is an open standard for AI agents to interact with external tools and data sources."
            },
            {
                "question_text": "Which component provides tools and resources in MCP architecture?",
                "question_type": "mcq",
                "options": [
                    "MCP Client",
                    "MCP Host",
                    "MCP Server",
                    "MCP Bridge"
                ],
                "correct_answer": "MCP Server",
                "explanation": "MCP Servers provide tools, resources, and prompts that agents can discover and use."
            },
            {
                "question_text": "MCP Resources are used to:",
                "question_type": "mcq",
                "options": [
                    "Execute code",
                    "Provide data to agents",
                    "Manage connections",
                    "Handle authentication"
                ],
                "correct_answer": "Provide data to agents",
                "explanation": "Resources in MCP provide data (files, documents, databases) that agents can read and reference."
            },
            {
                "question_text": "Before MCP, each tool required custom integration with agents.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Before MCP, agents were tightly coupled to specific services, requiring custom code for each integration."
            },
            {
                "question_text": "MCP Prompts allow you to:",
                "question_type": "mcq",
                "options": [
                    "Send messages to other agents",
                    "Define pre-configured prompt templates",
                    "Schedule tasks",
                    "Monitor agent performance"
                ],
                "correct_answer": "Define pre-configured prompt templates",
                "explanation": "MCP Prompts provide reusable prompt templates with defined arguments for consistent interactions."
            }
        ]
    },
    # Chapter 4: Agent Skills
    {
        "chapter_id": "ch-004",
        "questions": [
            {
                "question_text": "What is the main difference between Skills and Tools?",
                "question_type": "mcq",
                "options": [
                    "Skills are faster",
                    "Skills are behavioral patterns, Tools execute code",
                    "Tools are optional",
                    "There is no difference"
                ],
                "correct_answer": "Skills are behavioral patterns, Tools execute code",
                "explanation": "Skills define how an agent behaves (encoded in prompts/workflows), while Tools are executable functions."
            },
            {
                "question_text": "Trigger keywords in skills are used to:",
                "question_type": "mcq",
                "options": [
                    "Authenticate users",
                    "Activate the appropriate skill based on user input",
                    "Log interactions",
                    "Rate limit requests"
                ],
                "correct_answer": "Activate the appropriate skill based on user input",
                "explanation": "Trigger keywords help the agent recognize which skill to apply based on the user's request."
            },
            {
                "question_text": "The Socratic Tutor skill should never give direct answers.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "The Socratic method guides learning through questions, helping users discover answers themselves."
            },
            {
                "question_text": "Which of the following is NOT a component of a skill?",
                "question_type": "mcq",
                "options": [
                    "Trigger Keywords",
                    "Workflow Steps",
                    "Database Schema",
                    "Response Templates"
                ],
                "correct_answer": "Database Schema",
                "explanation": "Skills consist of triggers, purpose, workflow, templates, and principles - not database schemas."
            },
            {
                "question_text": "Skill Composition allows you to:",
                "question_type": "mcq",
                "options": [
                    "Delete unused skills",
                    "Combine multiple skills for complex tasks",
                    "Export skills to files",
                    "Encrypt skill definitions"
                ],
                "correct_answer": "Combine multiple skills for complex tasks",
                "explanation": "Skill chains allow multiple skills to work together in sequence for complex multi-step tasks."
            }
        ]
    },
    # Chapter 5: Agent Factory Architecture
    {
        "chapter_id": "ch-005",
        "questions": [
            {
                "question_text": "What is the lowest layer (L0) in the Agent Factory Architecture?",
                "question_type": "mcq",
                "options": [
                    "Apache Kafka",
                    "FastAPI",
                    "Agent Sandbox (gVisor)",
                    "Dapr + Workflows"
                ],
                "correct_answer": "Agent Sandbox (gVisor)",
                "explanation": "L0 is the Agent Sandbox layer using gVisor for secure execution isolation."
            },
            {
                "question_text": "Which layer handles event streaming in the architecture?",
                "question_type": "mcq",
                "options": [
                    "L1: Apache Kafka",
                    "L2: Dapr",
                    "L3: FastAPI",
                    "L4: OpenAI Agents SDK"
                ],
                "correct_answer": "L1: Apache Kafka",
                "explanation": "Apache Kafka at L1 serves as the event backbone for the entire architecture."
            },
            {
                "question_text": "Spec-Driven Development means writing code first, then specifications.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Spec-Driven Development means defining agent behavior in specifications first, then generating code from specs."
            },
            {
                "question_text": "What does A2A stand for in L7?",
                "question_type": "mcq",
                "options": [
                    "Application to Application",
                    "Agent to Agent",
                    "API to API",
                    "Algorithm to Algorithm"
                ],
                "correct_answer": "Agent to Agent",
                "explanation": "A2A Protocol enables multi-agent collaboration and communication."
            },
            {
                "question_text": "Which layer provides the HTTP interface?",
                "question_type": "mcq",
                "options": [
                    "L2: Dapr",
                    "L3: FastAPI",
                    "L4: OpenAI Agents SDK",
                    "L5: Claude Agent SDK"
                ],
                "correct_answer": "L3: FastAPI",
                "explanation": "FastAPI at L3 provides the HTTP interface and A2A communication endpoints."
            }
        ]
    },
]


async def seed_quizzes():
    """Seed quiz questions into the database."""
    # Create engine and session
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        total_questions = 0

        for quiz_data in QUIZZES:
            chapter_id = quiz_data["chapter_id"]

            for i, question_data in enumerate(quiz_data["questions"]):
                # Check if question already exists
                result = await session.execute(
                    select(QuizQuestion).where(
                        QuizQuestion.chapter_id == chapter_id,
                        QuizQuestion.question_text == question_data["question_text"]
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    print(f"Question '{question_data['question_text'][:50]}...' already exists, skipping...")
                    continue

                # Create quiz question
                question = QuizQuestion(
                    id=uuid.uuid4(),
                    chapter_id=chapter_id,
                    question_text=question_data["question_text"],
                    question_type=question_data["question_type"],
                    options=question_data["options"],
                    correct_answer=question_data["correct_answer"],
                    explanation=question_data["explanation"],
                    sequence_order=i + 1
                )
                session.add(question)
                total_questions += 1
                print(f"Added question to {chapter_id}: {question_data['question_text'][:50]}...")

        # Commit all changes
        await session.commit()
        print(f"\nSuccessfully seeded {total_questions} quiz questions!")


if __name__ == "__main__":
    print("Seeding quiz questions...")
    asyncio.run(seed_quizzes())
