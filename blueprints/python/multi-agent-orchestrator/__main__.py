"""
A2A Multi-Agent Orchestrator Blueprint - Server Entry Point

This template shows how to create a host/orchestrator agent that coordinates
multiple specialized sub-agents to accomplish complex tasks.
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
from agent_executor import OrchestratorExecutor


def create_agent_card(port: int) -> AgentCard:
    """
    Create and configure the orchestrator AgentCard.

    The orchestrator agent doesn't perform tasks itself - it delegates
    to specialized sub-agents and coordinates their efforts.
    """
    return AgentCard(
        # Basic identification
        name="Multi-Agent Orchestrator",  # TODO: Customize orchestrator name
        description=(
            "An orchestrator agent that coordinates multiple specialized agents "
            "to accomplish complex tasks."
        ),  # TODO: Customize description
        url=f"http://localhost:{port}/",
        version="1.0.0",

        # Communication modes
        default_input_modes=["text"],
        default_output_modes=["text"],

        # Orchestrator capabilities
        capabilities=AgentCapabilities(
            streaming=True,  # Forward streaming from sub-agents
            push_notifications=False,
            stateTransitionHistory=False,
        ),

        # High-level skills (delegated to sub-agents)
        skills=[
            AgentSkill(
                id="orchestrated_task_1",  # TODO: Customize skill
                name="Orchestrated Task 1",
                description=(
                    "Handles complex task 1 by coordinating multiple specialized agents."
                ),  # TODO: Customize
                tags=["orchestration", "multi-agent"],
                examples=[
                    "Perform complex task 1",
                    "Execute workflow 1",
                ],  # TODO: Add examples
            ),
            AgentSkill(
                id="orchestrated_task_2",  # TODO: Customize skill
                name="Orchestrated Task 2",
                description=(
                    "Handles complex task 2 by coordinating multiple specialized agents."
                ),  # TODO: Customize
                tags=["orchestration", "multi-agent"],
                examples=[
                    "Perform complex task 2",
                    "Execute workflow 2",
                ],  # TODO: Add examples
            ),
            # TODO: Add more high-level skills
        ],
    )


def main():
    """Start the orchestrator agent server."""
    parser = argparse.ArgumentParser(description="Multi-Agent Orchestrator")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "10000")),
        help="Port to run the orchestrator on (default: 10000)",
    )
    args = parser.parse_args()

    # Create agent card and executor
    agent_card = create_agent_card(args.port)

    # Configure sub-agent URLs
    # TODO: Update with your sub-agent URLs
    sub_agent_urls = {
        "agent_1": os.environ.get("AGENT_1_URL", "http://localhost:10001"),
        "agent_2": os.environ.get("AGENT_2_URL", "http://localhost:10002"),
        "agent_3": os.environ.get("AGENT_3_URL", "http://localhost:10003"),
    }

    agent_executor = OrchestratorExecutor(sub_agent_urls=sub_agent_urls)

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
    print("Configured sub-agents:")
    for name, url in sub_agent_urls.items():
        print(f"  - {name}: {url}")
    app.run()


if __name__ == "__main__":
    main()
