"""
A2A Tool-Using Agent Blueprint - Server Entry Point

This template shows how to create an agent that can use tools/functions
to perform specific tasks (like rolling dice, checking primes, calling APIs, etc.)
"""

import argparse
import os
from a2a import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    A2AStarletteApplication,
    A2AServerOptions,
)
from agent_executor import ToolUsingAgentExecutor


def create_agent_card(port: int) -> AgentCard:
    """
    Create and configure the AgentCard with tool-based skills.

    Each skill represents a specific tool or capability your agent can use.
    """
    return AgentCard(
        # Basic identification
        name="Tool-Using Agent",  # TODO: Customize your agent name
        description="An A2A agent that uses tools to perform specific tasks.",  # TODO: Customize
        url=f"http://localhost:{port}/",
        version="1.0.0",

        # Communication modes
        default_input_modes=["text"],
        default_output_modes=["text"],

        # Agent capabilities
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False,
            stateTransitionHistory=False,
        ),

        # Define skills for each tool
        skills=[
            AgentSkill(
                id="tool_1",  # TODO: Rename to match your tool
                name="Tool 1",  # TODO: Customize tool name
                description="Description of what Tool 1 does",  # TODO: Customize
                tags=["tool", "example"],
                examples=[
                    "Use tool 1 to do something",
                    "Can you run tool 1?",
                ],
            ),
            AgentSkill(
                id="tool_2",  # TODO: Rename to match your tool
                name="Tool 2",  # TODO: Customize tool name
                description="Description of what Tool 2 does",  # TODO: Customize
                tags=["tool", "example"],
                examples=[
                    "Use tool 2 for something",
                    "Run tool 2 with parameters",
                ],
            ),
            # TODO: Add more skills/tools as needed
        ],
    )


def main():
    """Start the A2A tool-using agent server."""
    parser = argparse.ArgumentParser(description="Tool-Using A2A Agent")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "9999")),
        help="Port to run the agent server on (default: 9999)",
    )
    args = parser.parse_args()

    # Create agent card and executor
    agent_card = create_agent_card(args.port)
    agent_executor = ToolUsingAgentExecutor()

    # Create A2A application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        agent_executor=agent_executor,
        server_options=A2AServerOptions(
            port=args.port,
            log_level="INFO",
        ),
    )

    # Start the server
    print(f"Starting {agent_card.name} on port {args.port}...")
    print(f"Available tools: {', '.join([s.name for s in agent_card.skills])}")
    app.run()


if __name__ == "__main__":
    main()
