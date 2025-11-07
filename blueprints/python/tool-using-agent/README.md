# A2A Tool-Using Agent Blueprint

A template for creating A2A agents that use tools and functions to perform specific tasks.

## What This Blueprint Provides

This blueprint demonstrates how to build an A2A agent with:

- ✅ **Tool/function definition** patterns
- ✅ **Tool registry** system for managing multiple tools
- ✅ **Multiple tool categories** (math, text, API calls, file operations)
- ✅ **LLM-based tool selection** examples (OpenAI function calling)
- ✅ **Keyword-based** fallback tool selection
- ✅ **Error handling** for tool execution
- ✅ **Organized code structure** with separate tool modules

## Use Cases

This blueprint is perfect for agents that need to:

- Perform calculations or data processing
- Call external APIs (weather, search, databases)
- Execute system operations
- Process files or documents
- Use specialized functions for specific tasks

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

# With LLM support (for advanced tool selection)
uv pip install -e ".[llm]"

# With API support (for web tools)
uv pip install -e ".[api]"
```

### Running the Agent

```bash
# Using uv
uv run python -m tool-using-agent-blueprint

# Or directly
python -m tool-using-agent-blueprint --port 9999
```

### Testing Your Agent

```python
from a2a import A2AClient

client = A2AClient("http://localhost:9999")

# Try different tools
responses = [
    await client.execute_task("Roll 2 dice"),
    await client.execute_task("Is 17 prime?"),
    await client.execute_task("Analyze this text: Hello world!"),
    await client.execute_task("Convert 100 celsius to fahrenheit"),
]
```

## Architecture

### Tool Structure

```
tool-using-agent/
├── __main__.py           # Server entry point
├── agent_executor.py     # Executor with tool selection logic
├── tools.py              # Tool definitions (separate module)
├── pyproject.toml        # Dependencies
└── README.md             # This file
```

### How It Works

1. **Tool Definition** - Tools are Python functions with clear signatures
2. **Tool Registry** - Central registry maps tool names to functions
3. **Tool Selection** - Agent determines which tool to use (keyword or LLM-based)
4. **Tool Execution** - Selected tool is called with parameters
5. **Result Formatting** - Tool results are formatted and returned

## Customization Guide

### 1. Define Your Tools

Add tool functions in `tools.py`:

```python
def my_custom_tool(param1: str, param2: int = 0) -> Dict[str, Any]:
    """
    Description of what your tool does.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (optional)

    Returns:
        Dictionary with results
    """
    # Implement your tool logic
    result = do_something(param1, param2)

    return {
        "result": result,
        "success": True,
    }
```

### 2. Register Your Tools

Add to `TOOLS` dictionary in `tools.py`:

```python
TOOLS = {
    "my_custom_tool": {
        "function": my_custom_tool,
        "description": "Does something useful",
        "category": "custom",
        "examples": ["Use my tool", "Run custom tool"],
    },
}
```

### 3. Update AgentCard Skills

Add corresponding skill in `__main__.py`:

```python
skills=[
    AgentSkill(
        id="my_custom_tool",
        name="My Custom Tool",
        description="Does something useful",
        examples=["Use my tool", "Run custom tool"],
    ),
]
```

### 4. Implement Tool Selection

Choose your approach in `agent_executor.py`:

**Option A: Keyword-Based (Simple)**

```python
if "my tool" in message_lower:
    result = my_custom_tool("param1", 42)
    return f"Result: {result}"
```

**Option B: LLM-Based (Advanced)**

```python
# Use OpenAI function calling, Claude tool use, or Gemini function calling
response = llm_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": user_message}],
    functions=[tool_to_function_schema(tool) for tool in tools],
    function_call="auto"
)
```

## Tool Patterns

### Simple Function Tool

```python
def simple_tool(input: str) -> str:
    """Simplest form - function with clear input/output."""
    return f"Processed: {input}"
```

### Structured Response Tool

```python
def structured_tool(input: str) -> Dict[str, Any]:
    """Returns structured data for complex results."""
    return {
        "status": "success",
        "data": process(input),
        "metadata": {"timestamp": datetime.now()},
    }
```

### API Call Tool

```python
import requests

def api_tool(query: str) -> Dict[str, Any]:
    """Calls external API."""
    response = requests.get(f"https://api.example.com/search?q={query}")
    return response.json()
```

### Error-Handling Tool

```python
def safe_tool(input: str) -> Dict[str, Any]:
    """Tool with proper error handling."""
    try:
        result = risky_operation(input)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Streaming Tool

```python
async def streaming_tool(input: str, event_queue: ExecutionEventQueue):
    """Tool that sends streaming updates."""
    for chunk in process_streaming(input):
        await event_queue.enqueue_event(
            AgentExecutionTextEvent(text=chunk, append=True)
        )
```

## Advanced Patterns

### LLM-Based Tool Selection

Use OpenAI function calling to let the LLM choose tools:

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define function schema
functions = [
    {
        "name": "roll_dice",
        "description": "Roll one or more dice",
        "parameters": {
            "type": "object",
            "properties": {
                "sides": {"type": "integer", "description": "Number of sides"},
                "count": {"type": "integer", "description": "Number of dice"},
            },
            "required": ["sides"],
        },
    }
]

# Let LLM choose and call function
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Roll 2 six-sided dice"}],
    functions=functions,
    function_call="auto"
)

if response.choices[0].message.function_call:
    function_name = response.choices[0].message.function_call.name
    function_args = json.loads(response.choices[0].message.function_call.arguments)

    # Execute the tool
    tool_func = tools_registry.get_tool(function_name)
    result = tool_func(**function_args)
```

### Tool Chaining

Execute multiple tools in sequence:

```python
async def execute_tool_chain(tools_sequence: List[Dict], event_queue):
    """Execute multiple tools in order, passing results between them."""
    context = {}

    for tool_spec in tools_sequence:
        tool_name = tool_spec["name"]
        tool_params = tool_spec.get("params", {})

        # Use results from previous tools
        if "from_previous" in tool_params:
            tool_params.update(context)

        # Execute tool
        tool_func = tools_registry.get_tool(tool_name)
        result = tool_func(**tool_params)

        # Store result for next tool
        context[f"{tool_name}_result"] = result

        # Update user
        await event_queue.enqueue_event(
            AgentExecutionTextEvent(text=f"Completed {tool_name}")
        )

    return context
```

### Conditional Tool Execution

Use LLM to decide if more tools are needed:

```python
async def execute_with_replanning(user_request: str, event_queue):
    """Execute tools and ask LLM if more tools are needed."""
    results = []
    max_iterations = 5

    for i in range(max_iterations):
        # Ask LLM what to do next
        response = llm_decide_next_action(user_request, results)

        if response["action"] == "complete":
            break
        elif response["action"] == "use_tool":
            tool_result = execute_tool(response["tool"], response["params"])
            results.append(tool_result)

    return synthesize_final_answer(results)
```

## Example Tools Included

### Math Tools
- `roll_dice` - Roll dice with specified sides and count
- `is_prime` - Check if a number is prime
- `calculate` - Evaluate mathematical expressions

### Time Tools
- `get_current_time` - Get current date and time

### Text Tools
- `analyze_text` - Get text statistics (word count, etc.)
- `reverse_text` - Reverse text by characters or words

### Conversion Tools
- `convert_units` - Convert between units (temperature, length, weight)

### API Tools
- `fetch_weather` - Get weather data (template)
- `search_web` - Search the web (template)

### File Tools
- `read_file` - Read file contents
- `write_file` - Write content to file

## Integration Examples

### OpenAI Function Calling

```python
from openai import OpenAI

def use_openai_function_calling(user_message: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        functions=[convert_tool_to_openai_function(tool) for tool in TOOLS.values()],
        function_call="auto"
    )

    return response
```

### Claude Tool Use

```python
from anthropic import Anthropic

def use_claude_tools(user_message: str):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": user_message}],
        tools=[convert_tool_to_claude_tool(tool) for tool in TOOLS.values()],
    )

    return response
```

### Gemini Function Calling

```python
import google.generativeai as genai

def use_gemini_functions(user_message: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    tools = [convert_tool_to_gemini_function(tool) for tool in TOOLS.values()]
    response = model.generate_content(
        user_message,
        tools=tools
    )

    return response
```

## Testing

### Unit Tests for Tools

```python
import pytest
from tools import roll_dice, is_prime, calculate

def test_roll_dice():
    result = roll_dice(sides=6, count=2)
    assert result["count"] == 2
    assert all(1 <= r <= 6 for r in result["rolls"])

def test_is_prime():
    assert is_prime(7)["is_prime"] == True
    assert is_prime(8)["is_prime"] == False

def test_calculate():
    result = calculate("2 + 2")
    assert result["result"] == 4
```

### Integration Tests

```bash
pytest tests/ -v
```

## Deployment

### Environment Variables

```bash
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Tool-specific keys
WEATHER_API_KEY=your_key_here
SEARCH_API_KEY=your_key_here

# Configuration
PORT=9999
LOG_LEVEL=INFO
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install --system -e ".[llm,api]"

EXPOSE 9999
CMD ["python", "-m", "tool-using-agent-blueprint"]
```

## Best Practices

1. **Clear Tool Signatures** - Use type hints and docstrings
2. **Error Handling** - Always handle tool failures gracefully
3. **Input Validation** - Validate tool parameters before execution
4. **Result Formatting** - Return consistent structured results
5. **Security** - Sanitize inputs, especially for file/system tools
6. **Testing** - Write unit tests for each tool
7. **Documentation** - Document tool parameters and examples

## Related Blueprints

- **Simple Agent**: Basic A2A agent without tools
- **Multi-Agent Orchestrator**: Coordinate multiple tool-using agents
- **Framework-Specific**: LangGraph, CrewAI patterns with tools

## Resources

- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Claude Tool Use Guide](https://docs.anthropic.com/claude/docs/tool-use)
- [Gemini Function Calling Guide](https://ai.google.dev/docs/function_calling)

## License

Apache 2.0
