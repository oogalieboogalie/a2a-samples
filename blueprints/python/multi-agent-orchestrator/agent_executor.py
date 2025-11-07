"""
A2A Multi-Agent Orchestrator Blueprint - Orchestration Logic

This demonstrates how to build an orchestrator that coordinates multiple
specialized agents to accomplish complex tasks.
"""

from typing import Dict, List, Any, Optional
import asyncio
from a2a import (
    AgentExecutor,
    ExecutionContext,
    ExecutionEventQueue,
    AgentExecutionTextEvent,
    AgentExecutionStateEvent,
    ExecutionState,
    A2AClient,
)


class SubAgent:
    """
    Wrapper for a sub-agent with its metadata and client.
    """

    def __init__(self, name: str, url: str, description: str = ""):
        self.name = name
        self.url = url
        self.description = description
        self._client: Optional[A2AClient] = None
        self._card = None

    async def get_client(self) -> A2AClient:
        """Get or create A2A client for this sub-agent."""
        if self._client is None:
            self._client = A2AClient(self.url)
        return self._client

    async def get_card(self):
        """Fetch the sub-agent's AgentCard."""
        if self._card is None:
            client = await self.get_client()
            self._card = await client.get_agent_card()
        return self._card

    async def execute_task(self, instruction: str, event_queue: ExecutionEventQueue):
        """
        Execute a task on this sub-agent and forward events.

        Args:
            instruction: The task instruction to send
            event_queue: Queue to forward events to
        """
        client = await self.get_client()

        # Send task and stream events
        async for event in client.execute_task(instruction):
            # Forward events from sub-agent to orchestrator's event queue
            await event_queue.enqueue_event(event)

        return True


class OrchestratorExecutor(AgentExecutor):
    """
    Orchestrator executor that coordinates multiple sub-agents.

    This executor:
    1. Receives a complex task from the user
    2. Breaks it down into sub-tasks
    3. Delegates sub-tasks to appropriate sub-agents
    4. Aggregates results and returns final answer
    """

    def __init__(self, sub_agent_urls: Dict[str, str]):
        """
        Initialize the orchestrator with sub-agent URLs.

        Args:
            sub_agent_urls: Dictionary mapping agent names to their URLs
        """
        # TODO: Configure your sub-agents here
        self.sub_agents = {
            name: SubAgent(name=name, url=url)
            for name, url in sub_agent_urls.items()
        }

    async def execute(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """
        Execute orchestration of sub-agents.

        This is where you implement your orchestration strategy:
        - Sequential execution (one agent after another)
        - Parallel execution (multiple agents at once)
        - Conditional execution (based on results)
        - Iterative refinement (loop until complete)
        """
        user_message = context.task_instruction

        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.THINKING,
                description="Analyzing task and planning agent coordination...",
            )
        )

        try:
            # TODO: Implement your orchestration strategy
            # Choose from patterns below or implement your own
            result = await self._orchestrate_task(user_message, event_queue)

            # Send final result
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(text=result)
            )

            await event_queue.enqueue_event(
                AgentExecutionStateEvent(
                    state=ExecutionState.COMPLETED,
                    description="All sub-agents completed successfully!",
                )
            )

        except Exception as e:
            await event_queue.enqueue_event(
                AgentExecutionStateEvent(
                    state=ExecutionState.FAILED,
                    description=f"Orchestration failed: {str(e)}",
                )
            )

    async def _orchestrate_task(
        self,
        user_message: str,
        event_queue: ExecutionEventQueue,
    ) -> str:
        """
        Main orchestration logic - choose your pattern here.

        TODO: Replace with your orchestration strategy
        """
        # Example: Sequential execution
        return await self._sequential_orchestration(user_message, event_queue)

        # Alternative patterns (uncomment to use):
        # return await self._parallel_orchestration(user_message, event_queue)
        # return await self._conditional_orchestration(user_message, event_queue)
        # return await self._iterative_orchestration(user_message, event_queue)

    # ===== ORCHESTRATION PATTERN 1: Sequential Execution =====

    async def _sequential_orchestration(
        self,
        user_message: str,
        event_queue: ExecutionEventQueue,
    ) -> str:
        """
        Execute sub-agents sequentially, passing results between them.

        Use this when:
        - Agent B needs results from Agent A
        - Tasks must be done in specific order
        - Each step builds on previous steps
        """
        results = {}

        # Execute agents in sequence
        for agent_name, agent in self.sub_agents.items():
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(
                    text=f"\n--- Delegating to {agent.name} ---\n"
                )
            )

            # Build instruction using previous results
            instruction = self._build_instruction_for_agent(
                agent_name, user_message, results
            )

            # Execute agent
            await agent.execute_task(instruction, event_queue)

            # Store result for next agent
            results[agent_name] = "completed"  # TODO: Store actual result

        # Synthesize final answer
        final_answer = self._synthesize_results(results)
        return final_answer

    # ===== ORCHESTRATION PATTERN 2: Parallel Execution =====

    async def _parallel_orchestration(
        self,
        user_message: str,
        event_queue: ExecutionEventQueue,
    ) -> str:
        """
        Execute multiple sub-agents in parallel.

        Use this when:
        - Agents don't depend on each other
        - You want faster execution
        - Tasks are independent
        """
        await event_queue.enqueue_event(
            AgentExecutionTextEvent(
                text="Executing multiple agents in parallel...\n"
            )
        )

        # Create tasks for parallel execution
        tasks = []
        for agent_name, agent in self.sub_agents.items():
            instruction = f"{user_message} (handled by {agent_name})"
            task = agent.execute_task(instruction, event_queue)
            tasks.append(task)

        # Wait for all agents to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check for errors
        errors = [r for r in results if isinstance(r, Exception)]
        if errors:
            raise Exception(f"Some agents failed: {errors}")

        return "All agents completed successfully in parallel!"

    # ===== ORCHESTRATION PATTERN 3: Conditional Execution =====

    async def _conditional_orchestration(
        self,
        user_message: str,
        event_queue: ExecutionEventQueue,
    ) -> str:
        """
        Execute agents conditionally based on logic or previous results.

        Use this when:
        - Different agents for different task types
        - Need to branch based on conditions
        - Dynamic agent selection
        """
        # Determine which agent(s) to use
        selected_agents = self._select_agents_for_task(user_message)

        results = []
        for agent_name in selected_agents:
            if agent_name not in self.sub_agents:
                continue

            agent = self.sub_agents[agent_name]

            await event_queue.enqueue_event(
                AgentExecutionTextEvent(
                    text=f"\n--- Selected {agent.name} for this task ---\n"
                )
            )

            await agent.execute_task(user_message, event_queue)
            results.append(agent_name)

            # Conditional: Stop if first agent succeeds
            if self._should_stop_execution(results):
                break

        return f"Executed agents: {', '.join(results)}"

    # ===== ORCHESTRATION PATTERN 4: Iterative Refinement =====

    async def _iterative_orchestration(
        self,
        user_message: str,
        event_queue: ExecutionEventQueue,
    ) -> str:
        """
        Execute agents iteratively, refining results in multiple passes.

        Use this when:
        - Need iterative improvement
        - Agent A generates, Agent B critiques, Agent A revises
        - Multi-round workflows
        """
        max_iterations = 3
        current_result = user_message

        for iteration in range(max_iterations):
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(
                    text=f"\n--- Iteration {iteration + 1} ---\n"
                )
            )

            # Generator agent
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(text="Generating...\n")
            )
            # TODO: Execute generator agent

            # Critic agent
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(text="Reviewing...\n")
            )
            # TODO: Execute critic agent

            # Check if result is good enough
            if self._is_result_satisfactory(current_result):
                break

        return f"Completed after {iteration + 1} iterations"

    # ===== HELPER METHODS =====

    def _build_instruction_for_agent(
        self,
        agent_name: str,
        original_message: str,
        previous_results: Dict[str, Any],
    ) -> str:
        """
        Build custom instruction for a specific agent.

        TODO: Customize this based on your agents and workflow.
        """
        # Simple example: just pass original message
        return original_message

        # Advanced example: Include previous results
        # if previous_results:
        #     context = "\n".join([
        #         f"- {name}: {result}"
        #         for name, result in previous_results.items()
        #     ])
        #     return f"{original_message}\n\nPrevious results:\n{context}"

    def _select_agents_for_task(self, user_message: str) -> List[str]:
        """
        Select which agents to use based on the task.

        TODO: Implement your agent selection logic.
        Examples:
        - Keyword matching
        - LLM-based selection
        - Rule-based routing
        """
        # Simple example: use all agents
        return list(self.sub_agents.keys())

        # Example: Keyword-based selection
        # if "weather" in user_message.lower():
        #     return ["weather_agent"]
        # elif "booking" in user_message.lower():
        #     return ["booking_agent"]
        # else:
        #     return ["general_agent"]

    def _should_stop_execution(self, results: List[Any]) -> bool:
        """
        Determine if execution should stop early.

        TODO: Implement your stopping logic.
        """
        # Example: Stop after first success
        return len(results) >= 1

    def _is_result_satisfactory(self, result: str) -> bool:
        """
        Check if iterative result is good enough.

        TODO: Implement your quality check.
        """
        # Example: Always iterate max times
        return False

    def _synthesize_results(self, results: Dict[str, Any]) -> str:
        """
        Combine results from multiple agents into final answer.

        TODO: Implement your result synthesis logic.
        """
        # Simple example
        return f"Orchestration completed. Agents executed: {', '.join(results.keys())}"

        # Advanced example: Use LLM to synthesize
        # synthesis_prompt = f"Combine these agent results:\n{json.dumps(results)}"
        # return call_llm(synthesis_prompt)

    async def cancel(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """
        Handle cancellation - should cancel all running sub-agents.

        TODO: Implement proper cancellation of sub-agents.
        """
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.CANCELLED,
                description="Orchestration cancelled.",
            )
        )


# ===== ADVANCED: LLM-Powered Orchestrator =====

class LLMOrchestratorExecutor(AgentExecutor):
    """
    Advanced orchestrator that uses an LLM to decide which agents to call
    and how to combine their results.

    This is more flexible than hard-coded orchestration logic.
    """

    def __init__(self, sub_agent_urls: Dict[str, str], llm_api_key: str = None):
        self.sub_agents = {
            name: SubAgent(name=name, url=url)
            for name, url in sub_agent_urls.items()
        }
        self.llm_api_key = llm_api_key
        # TODO: Initialize LLM client

    async def execute(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        """
        Use LLM to orchestrate agents dynamically.

        The LLM decides:
        1. Which agents to call
        2. In what order
        3. What instructions to give each agent
        4. How to combine results
        """
        user_message = context.task_instruction

        # TODO: Implement LLM-based orchestration
        # 1. Fetch all agent cards
        agent_descriptions = await self._get_agent_descriptions()

        # 2. Ask LLM to create execution plan
        # plan = await self._create_execution_plan(user_message, agent_descriptions)

        # 3. Execute plan
        # results = await self._execute_plan(plan, event_queue)

        # 4. Ask LLM to synthesize final answer
        # final_answer = await self._synthesize_with_llm(results)

        await event_queue.enqueue_event(
            AgentExecutionTextEvent(
                text="LLM-based orchestration not yet implemented. See code for examples."
            )
        )

        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.COMPLETED,
                description="Done!",
            )
        )

    async def _get_agent_descriptions(self) -> Dict[str, str]:
        """Fetch descriptions of all available agents."""
        descriptions = {}
        for name, agent in self.sub_agents.items():
            card = await agent.get_card()
            descriptions[name] = card.description
        return descriptions

    async def cancel(
        self,
        context: ExecutionContext,
        event_queue: ExecutionEventQueue,
    ) -> None:
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.CANCELLED,
                description="Orchestration cancelled.",
            )
        )
