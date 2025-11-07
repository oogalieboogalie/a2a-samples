# A2A Simple Agent Blueprint

A template for creating basic A2A (Agent-to-Agent) protocol agents in Python.

## What This Blueprint Provides

This blueprint gives you a complete starting point for building an A2A agent with:

- ✅ **Server setup** with proper A2A protocol handling
- ✅ **AgentCard configuration** (agent metadata and capabilities)
- ✅ **AgentExecutor pattern** for handling requests
- ✅ **Event publishing** for messages and status updates
- ✅ **Streaming support** example
- ✅ **Error handling** patterns
- ✅ **Cancellation** support

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Installation

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Or using pip
pip install -e .
```

### Running the Agent

```bash
# Using uv
uv run python -m simple-agent-blueprint

# Or directly
python -m simple-agent-blueprint

# Custom port
python -m simple-agent-blueprint --port 10000
```

The agent will start on `http://localhost:9999` by default.

### Testing Your Agent

Create a test client or use the A2A CLI:

```python
from a2a import A2AClient

# Create client
client = A2AClient("http://localhost:9999")

# Get agent card
card = await client.get_agent_card()
print(f"Agent: {card.name}")
print(f"Skills: {[s.name for s in card.skills]}")

# Send a message
async for event in client.execute_task("Hello, agent!"):
    if hasattr(event, 'text'):
        print(event.text)
```

## Customization Guide

### 1. Update Agent Metadata

Edit `__main__.py` in the `create_agent_card()` function:

```python
AgentCard(
    name="Your Agent Name",  # Change this
    description="What your agent does",  # Change this
    skills=[
        AgentSkill(
            id="your_skill_id",  # Use snake_case
            name="Your Skill Name",
            description="What this skill does",
            examples=["Example query 1", "Example query 2"],
        )
    ],
)
```

### 2. Implement Your Agent Logic

Edit `agent_executor.py` in the `_generate_response()` method:

```python
def _generate_response(self, user_message: str) -> str:
    # TODO: Replace with your logic
    # Examples:

    # Use an LLM
    # response = call_openai_api(user_message)

    # Call external APIs
    # data = requests.get("https://api.example.com/data")

    # Apply business logic
    # result = process_data(user_message)

    return "Your response here"
```

### 3. Add Dependencies

Edit `pyproject.toml`:

```toml
dependencies = [
    "a2a[server]>=0.2.3",
    "openai>=1.0.0",  # Add your dependencies
]
```

Then reinstall:

```bash
uv pip install -e .
```

### 4. Add Environment Variables

Create `.env` file:

```bash
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Configuration
PORT=9999
LOG_LEVEL=INFO
```

Load in your code:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

## Advanced Features

### Streaming Responses

Use `append=True` to send incremental updates:

```python
for chunk in generate_streaming_response():
    await event_queue.enqueue_event(
        AgentExecutionTextEvent(
            text=chunk,
            append=True,  # Append to previous text
        )
    )
```

### State Updates

Keep users informed of progress:

```python
# Thinking
await event_queue.enqueue_event(
    AgentExecutionStateEvent(
        state=ExecutionState.THINKING,
        description="Analyzing your request...",
    )
)

# Completed
await event_queue.enqueue_event(
    AgentExecutionStateEvent(
        state=ExecutionState.COMPLETED,
        description="Done!",
    )
)
```

### Publishing Artifacts

Send files, images, or structured data:

```python
from a2a import AgentExecutionArtifactEvent, Artifact

await event_queue.enqueue_event(
    AgentExecutionArtifactEvent(
        artifact=Artifact(
            content=file_bytes,
            content_type="image/png",
            name="result.png",
        )
    )
)
```

### Multi-Turn Conversations

Request additional input from the user:

```python
await event_queue.enqueue_event(
    AgentExecutionStateEvent(
        state=ExecutionState.INPUT_REQUIRED,
        description="I need more information. What is your preference?",
    )
)
```

## Project Structure

```
simple-agent-blueprint/
├── __main__.py           # Server entry point and AgentCard configuration
├── agent_executor.py     # Core agent logic and execution
├── pyproject.toml        # Dependencies and project metadata
├── README.md             # This file
├── .env.example          # Environment variable template
└── .python-version       # Python version specification
```

## Deployment

### Docker/Container

Create a `Containerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install --system -e .

EXPOSE 9999
CMD ["python", "-m", "simple-agent-blueprint"]
```

Build and run:

```bash
docker build -t my-agent .
docker run -p 9999:9999 my-agent
```

### Cloud Deployment

- **Google Cloud Run**: Set `PORT` environment variable
- **AWS Lambda**: Use A2A with AWS Lambda adapter
- **Azure Container Apps**: Deploy container with exposed port

## Common Patterns

### Using LLMs

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _generate_response(self, user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content
```

### Error Handling

```python
async def execute(self, context, event_queue):
    try:
        # Your logic here
        result = process_request(context.task_instruction)
        await event_queue.enqueue_event(
            AgentExecutionTextEvent(text=result)
        )
    except Exception as e:
        await event_queue.enqueue_event(
            AgentExecutionStateEvent(
                state=ExecutionState.FAILED,
                description=f"Error: {str(e)}",
            )
        )
```

### Accessing Context

```python
async def execute(self, context, event_queue):
    # User's message
    user_message = context.task_instruction

    # Session ID (for maintaining state across calls)
    session_id = context.session_id

    # Additional parameters
    params = context.execution_params
```

## Next Steps

1. **Customize the agent** - Update name, description, and skills
2. **Implement logic** - Add your agent's core functionality
3. **Add tools** - See `tool-using-agent` blueprint for tool patterns
4. **Test thoroughly** - Create test cases for your agent
5. **Deploy** - Choose your deployment platform

## Related Blueprints

- **Tool-Using Agent**: Agent that can call external tools/APIs
- **Multi-Agent Orchestrator**: Agent that coordinates multiple sub-agents
- **Framework-Specific**: Templates for LangGraph, CrewAI, etc.

## Resources

- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [Sample Agents](../../samples/)

## License

Apache 2.0
