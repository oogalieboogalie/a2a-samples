"""
A2A Simple Agent Blueprint - Server Entry Point

This is a template for creating a basic A2A agent that responds to user messages.
Customize the AgentCard configuration and agent logic to fit your use case.
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
from agent_executor import SimpleAgentExecutor


def create_agent_card(port: int) -> AgentCard:
    """
    Create and configure the AgentCard that describes this agent.

    The AgentCard is the agent's "business card" - it tells other agents:
    - What the agent can do (skills)
    - How to communicate with it (URL, input/output modes)
    - What features it supports (streaming, notifications, etc.)
    """
    return AgentCard(
        # Basic identification
        name="Simple Agent",  # TODO: Customize your agent name
        description="A simple A2A agent that demonstrates basic message handling patterns.",  # TODO: Customize description
        url=f"http://localhost:{port}/",
        version="1.0.0",

        # Communication modes
        default_input_modes=["text"],  # Accepts text messages
        default_output_modes=["text"],  # Returns text messages
        # Note: Can also include "image" and "artifact" modes

        # Agent capabilities
        capabilities=AgentCapabilities(
            streaming=True,  # Supports real-time streaming updates
            push_notifications=False,  # No webhook support
            stateTransitionHistory=False,  # No state history tracking
        ),

        # Skills this agent can perform
        skills=[
            AgentSkill(
                id="simple_response",  # TODO: Customize skill ID (snake_case)
                name="Simple Response",  # TODO: Customize skill name
                description="Responds to user messages with helpful information.",  # TODO: Customize skill description
                tags=["response", "simple"],  # TODO: Add relevant tags
                examples=[
                    "Hello, how can you help me?",
                    "What can you do?",
                    "Tell me something interesting",
                ],  # TODO: Add example queries
            ),
            # TODO: Add more skills as needed
        ],

        # Advanced: Support role-based extended cards
        supports_authenticated_extended_card=False,  # Set to True for authenticated features
    )


def main():
    """Start the A2A agent server."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Simple A2A Agent")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "9999")),
        help="Port to run the agent server on (default: 9999)",
    )
    args = parser.parse_args()

    # Create agent card and executor
    agent_card = create_agent_card(args.port)
    agent_executor = SimpleAgentExecutor()

    # Create A2A application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        agent_executor=agent_executor,
        server_options=A2AServerOptions(
            port=args.port,
            log_level="INFO",  # Can be: DEBUG, INFO, WARNING, ERROR
        ),
    )

    # Start the server
    print(f"Starting {agent_card.name} on port {args.port}...")
    print(f"Agent URL: {agent_card.url}")
    app.run()


if __name__ == "__main__":
    main()
