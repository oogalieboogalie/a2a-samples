# A2A Multi-Agent Orchestrator Blueprint

A template for creating A2A agents that orchestrate and coordinate multiple specialized sub-agents to accomplish complex tasks.

## What This Blueprint Provides

This blueprint demonstrates how to build an orchestrator agent with:

- ✅ **Sub-agent coordination** - Manage multiple specialized agents
- ✅ **Multiple orchestration patterns** - Sequential, parallel, conditional, iterative
- ✅ **Result aggregation** - Combine outputs from multiple agents
- ✅ **Event forwarding** - Stream updates from sub-agents to users
- ✅ **Error handling** - Graceful failure recovery
- ✅ **Flexible architecture** - Easy to extend and customize

## Use Cases

This blueprint is perfect for:

- Complex workflows requiring multiple specialized agents
- Tasks that need different types of expertise
- Planning and execution systems
- Multi-step processes (research → plan → execute)
- Collaborative agent systems

## Architecture

```
User
  ↓
Orchestrator Agent (this blueprint)
  ↓
  ├─→ Sub-Agent 1 (specialized task A)
  ├─→ Sub-Agent 2 (specialized task B)
  └─→ Sub-Agent 3 (specialized task C)
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Multiple sub-agents running (or mock agents for testing)

### Installation

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# With LLM support (for intelligent orchestration)
uv pip install -e ".[llm]"
```

### Configuration

Set up your sub-agent URLs in `.env`:

```bash
# Orchestrator configuration
PORT=10000

# Sub-agent URLs
AGENT_1_URL=http://localhost:10001
AGENT_2_URL=http://localhost:10002
AGENT_3_URL=http://localhost:10003
```

### Running the Orchestrator

```bash
# Start orchestrator
uv run python -m multi-agent-orchestrator-blueprint

# Custom port
python -m multi-agent-orchestrator-blueprint --port 10000
```

### Testing

```python
from a2a import A2AClient

client = A2AClient("http://localhost:10000")

# Send complex task to orchestrator
async for event in client.execute_task("Plan a trip and book accommodations"):
    if hasattr(event, 'text'):
        print(event.text)
```

## Orchestration Patterns

### Pattern 1: Sequential Execution

Execute agents one after another, passing results between them.

```python
async def _sequential_orchestration(self, user_message, event_queue):
    """
    Agent A → Agent B → Agent C
    Each agent uses results from previous agents
    """
    results = {}

    for agent_name, agent in self.sub_agents.items():
        instruction = self._build_instruction(agent_name, user_message, results)
        await agent.execute_task(instruction, event_queue)
        results[agent_name] = "result"

    return self._synthesize_results(results)
```

**When to use:**
- Agent B needs output from Agent A
- Tasks must be done in order
- Each step builds on previous

**Example:**
```
Research Agent → Planning Agent → Booking Agent
```

### Pattern 2: Parallel Execution

Execute multiple agents simultaneously for faster results.

```python
async def _parallel_orchestration(self, user_message, event_queue):
    """
    Agent A ┐
    Agent B ├─→ Combine Results
    Agent C ┘
    """
    tasks = [
        agent.execute_task(user_message, event_queue)
        for agent in self.sub_agents.values()
    ]

    results = await asyncio.gather(*tasks)
    return self._synthesize_results(results)
```

**When to use:**
- Independent tasks
- Need speed
- No dependencies between agents

**Example:**
```
Weather Agent ┐
News Agent    ├─→ Daily Brief
Stock Agent   ┘
```

### Pattern 3: Conditional Execution

Choose which agents to run based on the task or results.

```python
async def _conditional_orchestration(self, user_message, event_queue):
    """
    Select agents based on:
    - Task type
    - Keywords
    - Previous results
    - LLM decision
    """
    selected_agents = self._select_agents_for_task(user_message)

    for agent_name in selected_agents:
        agent = self.sub_agents[agent_name]
        await agent.execute_task(user_message, event_queue)

        if self._should_stop():
            break
```

**When to use:**
- Different agents for different tasks
- Dynamic routing
- Fallback options

**Example:**
```
If "weather" → Weather Agent
If "booking" → Booking Agent
If "general" → General Agent
```

### Pattern 4: Iterative Refinement

Loop multiple times to improve results.

```python
async def _iterative_orchestration(self, user_message, event_queue):
    """
    Iteration 1: Generator → Critic → Refine
    Iteration 2: Generator → Critic → Refine
    ...until satisfactory
    """
    for iteration in range(max_iterations):
        # Generate
        result = await self.generator_agent.execute_task(...)

        # Critique
        feedback = await self.critic_agent.execute_task(...)

        # Check if done
        if self._is_satisfactory(result):
            break
```

**When to use:**
- Need quality improvement
- Writer-editor workflows
- Iterative planning

**Example:**
```
Writer Agent → Editor Agent → Writer Agent → Editor Agent
```

## Customization Guide

### 1. Configure Your Sub-Agents

Edit `__main__.py`:

```python
sub_agent_urls = {
    "weather_agent": "http://localhost:10001",
    "booking_agent": "http://localhost:10002",
    "planning_agent": "http://localhost:10003",
}
```

Or use environment variables:

```bash
WEATHER_AGENT_URL=http://localhost:10001
BOOKING_AGENT_URL=http://localhost:10002
PLANNING_AGENT_URL=http://localhost:10003
```

### 2. Choose Orchestration Pattern

Edit `agent_executor.py` in the `_orchestrate_task` method:

```python
async def _orchestrate_task(self, user_message, event_queue):
    # Choose your pattern:

    # Sequential (one after another)
    return await self._sequential_orchestration(user_message, event_queue)

    # Parallel (all at once)
    # return await self._parallel_orchestration(user_message, event_queue)

    # Conditional (smart routing)
    # return await self._conditional_orchestration(user_message, event_queue)

    # Iterative (refinement loop)
    # return await self._iterative_orchestration(user_message, event_queue)
```

### 3. Implement Agent Selection Logic

For conditional orchestration:

```python
def _select_agents_for_task(self, user_message: str) -> List[str]:
    """Choose which agents to use."""

    # Keyword-based
    if "weather" in user_message.lower():
        return ["weather_agent"]

    # Intent-based
    intent = self._classify_intent(user_message)
    return self.intent_to_agents[intent]

    # LLM-based
    return self._llm_select_agents(user_message)
```

### 4. Customize Result Synthesis

Combine sub-agent results:

```python
def _synthesize_results(self, results: Dict[str, Any]) -> str:
    """Combine agent outputs into final answer."""

    # Simple concatenation
    return "\n\n".join(str(r) for r in results.values())

    # Template-based
    return f"Weather: {results['weather']}\nBooking: {results['booking']}"

    # LLM-based synthesis
    prompt = f"Combine these results:\n{json.dumps(results)}"
    return call_llm(prompt)
```

## Advanced Features

### LLM-Powered Orchestration

Use an LLM to dynamically decide which agents to call:

```python
from openai import OpenAI

class LLMOrchestratorExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        # Get agent descriptions
        agent_info = await self._get_agent_descriptions()

        # Ask LLM to create plan
        plan = await self._create_execution_plan(
            user_message=context.task_instruction,
            available_agents=agent_info
        )

        # Execute plan
        for step in plan["steps"]:
            agent = self.sub_agents[step["agent"]]
            await agent.execute_task(step["instruction"], event_queue)

        # Synthesize with LLM
        return await self._synthesize_with_llm(results)

    async def _create_execution_plan(self, user_message, available_agents):
        """Ask LLM to create execution plan."""
        prompt = f"""
        User request: {user_message}

        Available agents:
        {json.dumps(available_agents, indent=2)}

        Create a step-by-step execution plan specifying which agents
        to call, in what order, and what instructions to give them.
        """

        response = llm_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

### Error Handling and Retries

Handle sub-agent failures gracefully:

```python
async def execute_with_retry(self, agent, instruction, event_queue, max_retries=3):
    """Execute with automatic retry on failure."""
    for attempt in range(max_retries):
        try:
            await agent.execute_task(instruction, event_queue)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await event_queue.enqueue_event(
                AgentExecutionTextEvent(
                    text=f"Agent {agent.name} failed (attempt {attempt+1}), retrying..."
                )
            )
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Streaming from Sub-Agents

Forward streaming updates from sub-agents:

```python
async def execute_with_streaming(self, agent, instruction, event_queue):
    """Stream events from sub-agent to user."""
    await event_queue.enqueue_event(
        AgentExecutionTextEvent(text=f"\n--- {agent.name} ---\n")
    )

    client = await agent.get_client()

    async for event in client.execute_task(instruction):
        # Forward all events from sub-agent
        await event_queue.enqueue_event(event)
```

### Dynamic Agent Discovery

Discover agents at runtime:

```python
async def discover_agents(self, registry_url: str):
    """Discover available agents from a registry."""
    response = requests.get(f"{registry_url}/agents")
    agent_list = response.json()

    for agent_info in agent_list:
        self.sub_agents[agent_info["name"]] = SubAgent(
            name=agent_info["name"],
            url=agent_info["url"],
            description=agent_info["description"]
        )
```

## Example Workflows

### Example 1: Travel Planning

```python
# Sequential workflow
1. Weather Agent → Get weather forecast
2. Planning Agent → Suggest activities based on weather
3. Booking Agent → Book recommended activities
```

### Example 2: Content Creation

```python
# Iterative workflow
Iteration 1:
  - Writer Agent → Generate draft
  - Editor Agent → Provide feedback

Iteration 2:
  - Writer Agent → Revise based on feedback
  - Editor Agent → Final review
```

### Example 3: Research Assistant

```python
# Parallel + Sequential workflow
Step 1 (Parallel):
  - Web Search Agent → Find articles
  - Database Agent → Query internal data
  - News Agent → Get recent news

Step 2 (Sequential):
  - Analysis Agent → Analyze combined data
  - Summary Agent → Create final report
```

### Example 4: Adversarial Testing

```python
# Adversarial pattern
Loop:
  - Attacker Agent → Try to break system
  - Defender Agent → Fix vulnerabilities
  - Judge Agent → Evaluate if attack succeeded
Until system is secure
```

## Deployment

### Environment Variables

```bash
# Orchestrator
PORT=10000
LOG_LEVEL=INFO

# Sub-agent URLs
AGENT_1_URL=http://localhost:10001
AGENT_2_URL=http://localhost:10002
AGENT_3_URL=http://localhost:10003

# Optional: LLM for orchestration
OPENAI_API_KEY=your_key_here
```

### Docker Compose

Run orchestrator + sub-agents together:

```yaml
version: '3.8'

services:
  orchestrator:
    build: .
    ports:
      - "10000:10000"
    environment:
      - AGENT_1_URL=http://agent1:10001
      - AGENT_2_URL=http://agent2:10002
    depends_on:
      - agent1
      - agent2

  agent1:
    build: ../agent1
    ports:
      - "10001:10001"

  agent2:
    build: ../agent2
    ports:
      - "10002:10002"
```

Run:

```bash
docker-compose up
```

## Testing

### Unit Tests

Test orchestration logic:

```python
import pytest
from agent_executor import OrchestratorExecutor

@pytest.mark.asyncio
async def test_sequential_orchestration():
    orchestrator = OrchestratorExecutor(
        sub_agent_urls={"agent1": "http://localhost:10001"}
    )

    # Mock sub-agents
    # Test orchestration logic
    # Assert correct order and results
```

### Integration Tests

Test with real sub-agents:

```bash
# Start sub-agents in background
python -m agent1 --port 10001 &
python -m agent2 --port 10002 &

# Start orchestrator
python -m orchestrator --port 10000 &

# Run tests
pytest tests/integration/
```

## Best Practices

1. **Clear Agent Responsibilities** - Each sub-agent should have a specific purpose
2. **Error Handling** - Always handle sub-agent failures gracefully
3. **Timeouts** - Set timeouts for sub-agent calls
4. **Logging** - Log all orchestration decisions and agent interactions
5. **Result Validation** - Validate sub-agent outputs before using them
6. **Monitoring** - Track agent performance and success rates
7. **Fallbacks** - Have backup agents or strategies if primary agents fail

## Troubleshooting

### Sub-agent not responding

```python
# Add timeout and retry logic
try:
    await asyncio.wait_for(
        agent.execute_task(instruction, event_queue),
        timeout=30.0
    )
except asyncio.TimeoutError:
    # Use fallback or return error
```

### Results not synthesizing correctly

```python
# Debug result structure
print(f"Results from agents: {json.dumps(results, indent=2)}")
```

### Agents executing in wrong order

```python
# For sequential: ensure await before next agent
await agent1.execute_task(...)  # Wait for completion
await agent2.execute_task(...)  # Then start next
```

## Related Blueprints

- **Simple Agent**: Single-purpose agent template
- **Tool-Using Agent**: Agent with tools/functions
- **Framework-Specific**: LangGraph, CrewAI orchestration patterns

## Resources

- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [Multi-Agent Systems Guide](https://example.com/multi-agent-guide)

## License

Apache 2.0
