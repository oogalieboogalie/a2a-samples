# A2A Agent Blueprints

Comprehensive templates and guides for building Agent-to-Agent (A2A) protocol agents.

## What Are Blueprints?

Blueprints are production-ready templates that help you quickly scaffold new A2A agents. Each blueprint provides:

- ✅ **Complete working code** - Copy and customize
- ✅ **Best practices** - Industry-standard patterns
- ✅ **Detailed documentation** - Step-by-step guides
- ✅ **Common patterns** - Proven architectures
- ✅ **Type safety** - Where applicable
- ✅ **Testing examples** - Unit and integration tests

## Available Blueprints

### Python Blueprints

#### 1. Simple Agent
**Location**: `blueprints/python/simple-agent/`

Basic A2A agent template with core functionality.

**Best for**:
- First-time A2A developers
- Simple request-response agents
- Learning the basics

**Features**:
- AgentCard configuration
- Event publishing
- Streaming support
- Error handling
- Cancellation support

**Quick start**:
```bash
cd blueprints/python/simple-agent
uv venv && source .venv/bin/activate
uv pip install -e .
python -m simple-agent-blueprint
```

---

#### 2. Tool-Using Agent
**Location**: `blueprints/python/tool-using-agent/`

Agent with tools/functions for specific tasks.

**Best for**:
- Agents that need to perform actions
- API integration
- Data processing
- Calculations and transformations

**Features**:
- Tool definition patterns
- Tool registry system
- LLM-based tool selection
- Multiple tool categories (math, text, API, file)
- Error handling for tools

**Included tools**:
- Math tools (dice rolling, prime checking, calculations)
- Time tools (current time)
- Text processing (analysis, reversal)
- Unit conversion
- API calls (weather, web search)
- File operations

**Quick start**:
```bash
cd blueprints/python/tool-using-agent
uv pip install -e ".[llm,api]"
python -m tool-using-agent-blueprint
```

---

#### 3. Multi-Agent Orchestrator
**Location**: `blueprints/python/multi-agent-orchestrator/`

Orchestrator agent that coordinates multiple specialized sub-agents.

**Best for**:
- Complex workflows
- Tasks requiring multiple types of expertise
- Multi-step processes
- Collaborative agent systems

**Features**:
- 4 orchestration patterns (sequential, parallel, conditional, iterative)
- Sub-agent management
- Result aggregation
- Event forwarding
- LLM-powered orchestration option

**Orchestration patterns**:
1. **Sequential**: Execute agents one after another
2. **Parallel**: Run multiple agents simultaneously
3. **Conditional**: Choose agents based on task
4. **Iterative**: Refine results through multiple passes

**Quick start**:
```bash
cd blueprints/python/multi-agent-orchestrator
uv pip install -e ".[llm]"

# Configure sub-agent URLs in .env
# AGENT_1_URL=http://localhost:10001
# AGENT_2_URL=http://localhost:10002

python -m multi-agent-orchestrator-blueprint
```

---

### JavaScript/TypeScript Blueprint

#### JavaScript Agent
**Location**: `blueprints/javascript/`

Modern TypeScript agent with Genkit integration.

**Best for**:
- Node.js developers
- Teams using TypeScript
- Firebase/Google Cloud users
- Need for prompt management

**Features**:
- TypeScript for type safety
- Firebase Genkit for AI/prompts
- Express.js server
- Tool/function calling
- Streaming responses
- Multi-model support (Gemini, GPT, Claude)
- Structured prompts with Zod schemas

**Quick start**:
```bash
cd blueprints/javascript
npm install
cp .env.example .env
# Add your API keys to .env
npm run dev
```

---

### Java Blueprint

#### Java/Quarkus Agent
**Location**: `blueprints/java/`

Enterprise Java agents with Quarkus and LangChain4j.

**Best for**:
- Java developers
- Enterprise environments
- Need for GraalVM native images
- Multi-transport support (HTTP + gRPC)

**Features**:
- Quarkus framework
- LangChain4j integration
- CDI dependency injection
- Fast startup times
- Native image compilation
- Multi-transport (HTTP/gRPC)

**Quick start**:
See Java README for detailed instructions and sample references.

---

## Choosing a Blueprint

### By Experience Level

**Beginner**:
1. Start with **Simple Agent** (Python or JavaScript)
2. Learn core concepts
3. Move to **Tool-Using Agent**

**Intermediate**:
1. Use **Tool-Using Agent** for practical agents
2. Explore **JavaScript Blueprint** for TypeScript
3. Try **Multi-Agent Orchestrator** for complex workflows

**Advanced**:
1. **Multi-Agent Orchestrator** with LLM orchestration
2. **Java Blueprint** for enterprise systems
3. Custom combinations of patterns

### By Use Case

**Simple Q&A Agent**:
→ Simple Agent blueprint

**Agent with Specific Functions** (weather, calculations, etc.):
→ Tool-Using Agent blueprint

**Complex Workflows** (research → plan → execute):
→ Multi-Agent Orchestrator blueprint

**Content Creation** (writer + editor):
→ Multi-Agent Orchestrator (iterative pattern)

**Data Processing**:
→ Tool-Using Agent blueprint

**Enterprise System**:
→ Java/Quarkus blueprint

**Modern Web Service**:
→ JavaScript/TypeScript blueprint

### By Language Preference

| Language | Blueprint | Best For |
|----------|-----------|----------|
| Python | Simple Agent | Beginners, quick prototypes |
| Python | Tool-Using Agent | Most use cases |
| Python | Multi-Agent Orchestrator | Complex systems |
| TypeScript | JavaScript Blueprint | Modern web services |
| Java | Java Blueprint | Enterprise systems |

## Quick Start Guide

### 1. Choose Your Blueprint

Pick based on your use case and language preference.

### 2. Copy the Blueprint

```bash
# Example: Copy Python tool-using agent
cp -r blueprints/python/tool-using-agent my-new-agent
cd my-new-agent
```

### 3. Customize

Follow the blueprint's README for customization steps:
- Update agent name and description
- Add your business logic
- Configure API keys
- Add custom tools/skills

### 4. Test

```bash
# Start your agent
python -m my-new-agent

# Test with A2A client
python test_client.py
```

### 5. Deploy

Follow deployment instructions in the blueprint's README.

## Common Patterns

### Pattern 1: Simple Request-Response

```
User → Agent → Response
```

**Use**: Simple Agent blueprint

---

### Pattern 2: Tool-Augmented Agent

```
User → Agent → Select Tool → Execute Tool → Response
```

**Use**: Tool-Using Agent blueprint

---

### Pattern 3: Sequential Multi-Agent

```
User → Orchestrator → Agent A → Agent B → Agent C → Response
```

**Use**: Multi-Agent Orchestrator (sequential pattern)

---

### Pattern 4: Parallel Multi-Agent

```
            ┌─ Agent A ─┐
User → Orch ├─ Agent B ─┤ → Combine → Response
            └─ Agent C ─┘
```

**Use**: Multi-Agent Orchestrator (parallel pattern)

---

### Pattern 5: Iterative Refinement

```
User → Orchestrator → (Writer → Editor)×N → Response
```

**Use**: Multi-Agent Orchestrator (iterative pattern)

---

## Architecture Components

All blueprints share common A2A components:

### AgentCard
Describes the agent's capabilities and skills.

```python
AgentCard(
    name="Agent Name",
    description="What it does",
    skills=[...],
    capabilities=AgentCapabilities(...)
)
```

### AgentExecutor
Handles execution logic.

```python
class MyExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        # Your logic here
        pass
```

### Event Publishing
Communicate with users/agents.

```python
# Text message
await event_queue.enqueue_event(
    AgentExecutionTextEvent(text="Hello!")
)

# Status update
await event_queue.enqueue_event(
    AgentExecutionStateEvent(state=ExecutionState.COMPLETED)
)
```

## Development Workflow

### 1. Local Development

```bash
# Start agent in dev mode
python -m my-agent --port 9999

# Or with hot reload
uv run --reload python -m my-agent
```

### 2. Testing

```bash
# Unit tests
pytest tests/

# Integration tests with test client
python test_client.py
```

### 3. Deployment

```bash
# Containerize
docker build -t my-agent .

# Deploy to cloud
# See blueprint README for platform-specific instructions
```

## Best Practices

### 1. Start Simple
Begin with Simple Agent blueprint, add complexity as needed.

### 2. Use Tools Appropriately
- Simple tasks: Direct implementation
- Complex tasks: Use tools
- Multiple tools: Consider LLM-based selection

### 3. Handle Errors Gracefully
All blueprints include error handling patterns - use them!

### 4. Test Thoroughly
- Unit test your business logic
- Integration test with A2A client
- Load test for production

### 5. Document Your Agent
- Clear skill descriptions
- Example queries
- Configuration requirements

### 6. Secure Your Agent
- Validate all inputs
- Use environment variables for secrets
- Consider authentication for sensitive operations

## Advanced Topics

### Custom Frameworks

Want to use a specific framework (LangGraph, CrewAI, etc.)?

**Approach**:
1. Start with Simple Agent or Tool-Using Agent
2. Replace the `execute()` logic with your framework
3. Keep A2A event publishing

See `samples/python/agents/` for framework-specific examples.

### Multi-Language Systems

**Orchestrator (Python)** → **Sub-Agent 1 (JavaScript)** → **Sub-Agent 2 (Java)**

Use the Multi-Agent Orchestrator to coordinate agents in different languages.

### Streaming and Real-Time Updates

All blueprints support streaming. Use `append=True` for incremental updates:

```python
await event_queue.enqueue_event(
    AgentExecutionTextEvent(text="chunk", append=True)
)
```

### Custom Protocols

Need gRPC or other protocols? See Java blueprint for multi-transport examples.

## Troubleshooting

### Agent not starting

```bash
# Check port availability
lsof -i :9999

# Check logs
tail -f agent.log
```

### Can't connect to agent

```bash
# Verify agent is running
curl http://localhost:9999/agent-card

# Check firewall/network
```

### Tool execution failing

- Check API keys in environment
- Verify tool parameters
- Review error messages in logs

### Orchestration issues

- Verify all sub-agents are running
- Check sub-agent URLs in configuration
- Review orchestration logs

## Contributing

Found an issue or have a suggestion?

1. Check existing issues: [GitHub Issues](https://github.com/a2aproject/a2a-samples/issues)
2. Submit a new issue or PR
3. Follow the contributing guidelines

## Resources

### Documentation
- [A2A Protocol Specification](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [A2A Java SDK](https://github.com/a2aproject/a2a-java-sdk)

### Sample Code
- Python samples: `samples/python/agents/`
- JavaScript samples: `samples/js/src/agents/`
- Java samples: `samples/java/agents/`

### Community
- GitHub Discussions
- Issue Tracker

## FAQ

### Q: Which blueprint should I start with?

**A**: If you're new to A2A, start with the **Simple Agent** blueprint in your preferred language. Once comfortable, move to **Tool-Using Agent** for practical applications.

### Q: Can I mix languages?

**A**: Yes! Use the **Multi-Agent Orchestrator** (in any language) to coordinate sub-agents written in different languages.

### Q: How do I add my own LLM?

**A**: Replace the LLM calls in the executor with your provider's API. All blueprints show examples.

### Q: Do I need to use Genkit/LangChain4j?

**A**: No. These are provided as convenient options, but you can use any LLM library or framework.

### Q: Can I deploy these to production?

**A**: Yes! All blueprints include deployment guidance. Add proper error handling, monitoring, and security measures.

### Q: How do I handle authentication?

**A**: See the Java blueprint and `magic_8_ball_security` sample for authentication patterns.

### Q: Can agents call other agents?

**A**: Yes! Use the **Multi-Agent Orchestrator** pattern or directly use A2A client in any agent.

## Next Steps

1. **Choose a blueprint** based on your needs
2. **Copy and customize** the template
3. **Run locally** and test
4. **Deploy** to your environment
5. **Iterate** and improve

Happy building! 🚀

## License

All blueprints are licensed under Apache 2.0.
