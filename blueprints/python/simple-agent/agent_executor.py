"""
A2A Simple Agent Blueprint - Executor Implementation

The AgentExecutor is the core business logic of your agent.
It handles incoming messages and generates responses.
"""

from a2a import (
    AgentExecutor,
    ExecutionContext,
    ExecutionEventQueue,
    AgentExecutionTextEvent,
    AgentExecutionStateEvent,
    ExecutionState,
)


class SimpleAgentExecutor(AgentExecutor):
    """
    Simple agent executor that demonstrates basic message handling.

    This executor receives messages from users/agents and responds with text.
    Customize the execute() method to implement your agent's logic.
    """

    async def execute(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """
        Execute the agent's task.

        Args:
            context: Contains the execution context including:
                - context.task_instruction: The user's request/message
                - context.execution_params: Additional parameters
                - context.session_id: Unique session identifier
            event_queue: Queue for publishing events (messages, status updates, etc.)
        """
        # Get the user's message
        user_message = context.task_instruction

        # Update status to "thinking"
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.THINKING,
                description="Processing your request...",
            )
        )

        # TODO: Implement your agent logic here
        # This is where you would:
        # - Process the user's input
        # - Call external APIs
        # - Use LLMs for generation
        # - Perform computations
        # - Access databases

        # Example: Simple response logic
        response = self._generate_response(user_message)

        # Send the response back to the user
        await event_queue.enqueue_event(
            AgentExecutionTextEvent(
                text=response,
                append=False,  # Set True for streaming/incremental updates
            )
        )

        # Mark task as completed
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.COMPLETED,
                description="Task completed successfully!",
            )
        )

    def _generate_response(self, user_message: str) -> str:
        """
        Generate a response to the user's message.

        TODO: Replace this with your actual agent logic.
        Examples:
        - Call an LLM API (OpenAI, Anthropic, Google Gemini)
        - Use a local model
        - Apply business logic
        - Query databases or APIs

        Args:
            user_message: The user's input message

        Returns:
            The agent's response
        """
        # Simple example response
        if "hello" in user_message.lower():
            return "Hello! I'm a simple A2A agent. How can I help you today?"
        elif "help" in user_message.lower():
            return "I'm a simple agent that can respond to your messages. Ask me anything!"
        else:
            return f"You said: '{user_message}'. I'm a simple agent template - customize me to do more!"

    async def cancel(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """
        Handle task cancellation.

        This method is called when a user/agent requests to cancel the current task.
        Implement cleanup logic if needed.
        """
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.CANCELLED,
                description="Task cancelled by user.",
            )
        )


# Advanced Pattern: Streaming Updates
class StreamingAgentExecutor(AgentExecutor):
    """
    Example of an agent that sends streaming/incremental updates.
    Useful for long-running tasks or real-time generation.
    """

    async def execute(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        user_message = context.task_instruction

        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.THINKING,
                description="Starting to generate response...",
            )
        )

        # Simulate streaming response word by word
        response_words = ["This", "is", "a", "streaming", "response", "example."]

        for word in response_words:
            # Send each word incrementally with append=True
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(
                    text=word + " ",
                    append=True,  # Append to previous text
                )
            )
            # In real implementation, this would be your LLM streaming chunks

        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.COMPLETED,
                description="Streaming complete!",
            )
        )

    async def cancel(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.CANCELLED,
                description="Streaming cancelled.",
            )
        )
