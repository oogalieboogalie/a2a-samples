"""
A2A Tool-Using Agent Blueprint - Executor with Tools

This demonstrates how to create an agent that can use tools to perform tasks.
Tools can be simple functions, API calls, or complex operations.
"""

import json
from typing import Any, Dict, List, Callable
from a2a import (
    AgentExecutor,
    ExecutionContext,
    ExecutionEventQueue,
    AgentExecutionTextEvent,
    AgentExecutionStateEvent,
    ExecutionState,
)


# ===== DEFINE YOUR TOOLS =====

def tool_example_1(param1: str, param2: int = 1) -> str:
    """
    Example tool 1 - Replace with your actual tool.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 1)

    Returns:
        The result of the tool execution
    """
    # TODO: Implement your tool logic here
    return f"Tool 1 executed with param1='{param1}' and param2={param2}"


def tool_example_2(data: str) -> Dict[str, Any]:
    """
    Example tool 2 - Returns structured data.

    Args:
        data: Input data to process

    Returns:
        Dictionary with results
    """
    # TODO: Implement your tool logic here
    return {
        "status": "success",
        "data": data,
        "processed": True,
    }


def tool_api_call(endpoint: str, method: str = "GET") -> str:
    """
    Example API call tool.

    Args:
        endpoint: The API endpoint to call
        method: HTTP method (GET, POST, etc.)

    Returns:
        API response
    """
    # TODO: Implement actual API call
    # import requests
    # response = requests.request(method, endpoint)
    # return response.json()

    return f"Would call {method} {endpoint}"


# ===== TOOL REGISTRY =====

class ToolRegistry:
    """
    Central registry for all available tools.
    Maps tool names to their functions and metadata.
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {
            # TODO: Register your tools here
            "tool_example_1": {
                "function": tool_example_1,
                "description": "Example tool that does something",
                "parameters": {
                    "param1": {"type": "string", "required": True, "description": "First parameter"},
                    "param2": {"type": "integer", "required": False, "description": "Second parameter", "default": 1},
                },
            },
            "tool_example_2": {
                "function": tool_example_2,
                "description": "Example tool that returns structured data",
                "parameters": {
                    "data": {"type": "string", "required": True, "description": "Input data"},
                },
            },
            "api_call": {
                "function": tool_api_call,
                "description": "Make an API call",
                "parameters": {
                    "endpoint": {"type": "string", "required": True, "description": "API endpoint URL"},
                    "method": {"type": "string", "required": False, "description": "HTTP method", "default": "GET"},
                },
            },
        }

    def get_tool(self, tool_name: str) -> Callable:
        """Get a tool function by name."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        return self.tools[tool_name]["function"]

    def list_tools(self) -> List[str]:
        """List all available tool names."""
        return list(self.tools.keys())

    def get_tool_description(self, tool_name: str) -> str:
        """Get a tool's description."""
        return self.tools[tool_name]["description"]


# ===== AGENT EXECUTOR =====

class ToolUsingAgentExecutor(AgentExecutor):
    """
    Agent executor that can use tools to accomplish tasks.

    This agent:
    1. Receives a user request
    2. Determines which tool(s) to use
    3. Executes the tool(s)
    4. Returns the results
    """

    def __init__(self):
        self.tools = ToolRegistry()

    async def execute(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """
        Execute the agent's task using available tools.

        The agent determines which tool to use based on the user's message
        and then executes that tool.
        """
        user_message = context.task_instruction

        # Update status
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.THINKING,
                description="Analyzing your request and selecting appropriate tool...",
            )
        )

        try:
            # TODO: Replace this simple pattern matching with:
            # - LLM-based tool selection (using function calling)
            # - Structured command parsing
            # - Intent classification
            result = await self._process_with_tools(user_message)

            # Send result
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(text=result, append=False)
            )

            # Mark as completed
            await event_queue.enqueue_event(
                AgentExecutionStateEvent(
                    state=ExecutionState.COMPLETED,
                    description="Task completed!",
                )
            )

        except Exception as e:
            # Handle errors
            await event_queue.enqueue_event(
                AgentExecutionStateEvent(
                    state=ExecutionState.FAILED,
                    description=f"Error: {str(e)}",
                )
            )

    async def _process_with_tools(self, user_message: str) -> str:
        """
        Process the user message and execute appropriate tools.

        TODO: Replace this simple keyword matching with proper tool selection:
        - Use an LLM with function calling (OpenAI, Claude, Gemini)
        - Parse structured commands
        - Use intent classification
        """
        message_lower = user_message.lower()

        # Simple keyword-based tool selection (replace with LLM-based selection)
        if "tool 1" in message_lower or "example 1" in message_lower:
            result = tool_example_1("example input", 5)
            return f"Executed Tool 1:\n{result}"

        elif "tool 2" in message_lower or "example 2" in message_lower:
            result = tool_example_2("sample data")
            return f"Executed Tool 2:\n{json.dumps(result, indent=2)}"

        elif "api" in message_lower or "call" in message_lower:
            result = tool_api_call("https://api.example.com/data")
            return f"API Call Result:\n{result}"

        elif "list tools" in message_lower or "what can you do" in message_lower:
            tools = self.tools.list_tools()
            descriptions = [
                f"- {name}: {self.tools.get_tool_description(name)}"
                for name in tools
            ]
            return "Available tools:\n" + "\n".join(descriptions)

        else:
            return (
                f"I didn't understand which tool to use for: '{user_message}'\n\n"
                f"Available tools: {', '.join(self.tools.list_tools())}\n"
                f"Try saying 'list tools' to see what I can do!"
            )

    async def cancel(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """Handle task cancellation."""
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.CANCELLED,
                description="Task cancelled.",
            )
        )


# ===== ADVANCED PATTERN: LLM-Based Tool Selection =====

class LLMToolUsingAgentExecutor(AgentExecutor):
    """
    Advanced agent that uses an LLM to determine which tools to call.

    This pattern is more flexible and can handle natural language requests
    without explicit keyword matching.
    """

    def __init__(self, llm_api_key: str = None):
        self.tools = ToolRegistry()
        self.llm_api_key = llm_api_key
        # TODO: Initialize your LLM client here
        # self.llm_client = OpenAI(api_key=llm_api_key)

    async def execute(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        user_message = context.task_instruction

        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.THINKING,
                description="Using LLM to determine appropriate action...",
            )
        )

        try:
            # TODO: Implement LLM-based tool selection
            # Example using OpenAI function calling:
            #
            # response = self.llm_client.chat.completions.create(
            #     model="gpt-4",
            #     messages=[{"role": "user", "content": user_message}],
            #     functions=[self._tool_to_function_schema(tool_name)
            #                for tool_name in self.tools.list_tools()],
            #     function_call="auto"
            # )
            #
            # if response.choices[0].message.function_call:
            #     function_name = response.choices[0].message.function_call.name
            #     function_args = json.loads(response.choices[0].message.function_call.arguments)
            #     tool_func = self.tools.get_tool(function_name)
            #     result = tool_func(**function_args)
            #     ...

            result = "LLM-based tool selection not yet implemented. See code comments for examples."

            await event_queue.enqueue_event(
                AgentExecutionTextEvent(text=result)
            )

            await event_queue.enqueue_event(
                AgentExecutionStateEvent(
                    state=ExecutionState.COMPLETED,
                    description="Completed!",
                )
            )

        except Exception as e:
            await event_queue.enqueue_event(
                AgentExecutionStateEvent(
                    state=ExecutionState.FAILED,
                    description=f"Error: {str(e)}",
                )
            )

    def _tool_to_function_schema(self, tool_name: str) -> Dict:
        """
        Convert tool metadata to OpenAI function calling schema.

        TODO: Implement this to enable LLM function calling.
        """
        tool_info = self.tools.tools[tool_name]
        return {
            "name": tool_name,
            "description": tool_info["description"],
            "parameters": {
                "type": "object",
                "properties": tool_info["parameters"],
                "required": [
                    name for name, info in tool_info["parameters"].items()
                    if info.get("required", False)
                ],
            },
        }

    async def cancel(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.CANCELLED,
                description="Task cancelled.",
            )
        )
