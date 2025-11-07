# A2A Java/Quarkus Agent Blueprint

A guide for creating A2A (Agent-to-Agent) protocol agents using Java with Quarkus and LangChain4j.

## Overview

Java A2A agents typically use:

- **Quarkus** - Modern Java framework with fast startup
- **LangChain4j** - Java library for LLM integration
- **CDI (Contexts and Dependency Injection)** - For configuration
- **Maven/Gradle** - Build tools

## Quick Start

The best way to get started with Java A2A agents is to use one of the existing sample agents as a template:

### Recommended Starting Points

1. **Dice Agent (Multi-Transport)**
   - Location: `samples/java/agents/dice_agent_multi_transport/`
   - Features: Tool usage, multi-protocol (gRPC, JSON-RPC), LangChain4j
   - Best for: Learning the basics

2. **Content Editor**
   - Location: `samples/java/agents/content_editor/`
   - Features: Text processing, LangChain4j integration
   - Best for: Content manipulation agents

3. **Magic 8 Ball (Security)**
   - Location: `samples/java/agents/magic_8_ball_security/`
   - Features: Keycloak authentication, bearer tokens
   - Best for: Secured agents

4. **Weather MCP**
   - Location: `samples/java/agents/weather_mcp/`
   - Features: MCP (Model Context Protocol) integration
   - Best for: MCP server patterns

## Architecture Pattern

### Project Structure

```
my-agent/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/example/a2a/
│       │       ├── AgentCardProducer.java      # AgentCard configuration
│       │       ├── Agent.java                  # LLM agent interface
│       │       ├── Tools.java                  # Tool definitions
│       │       ├── Executor.java               # Executor implementation
│       │       └── ExecutorProducer.java       # Executor factory
│       └── resources/
│           └── application.properties          # Quarkus configuration
├── pom.xml                                     # Maven dependencies
└── README.md
```

### Key Components

#### 1. AgentCard Producer

```java
@ApplicationScoped
public class MyAgentCardProducer {

    @Produces
    @ApplicationScoped
    public AgentCard agentCard() {
        return AgentCard.builder()
            .name("My Java Agent")
            .description("What this agent does")
            .url("http://localhost:11000/")
            .version("1.0.0")
            .addSkill(AgentSkill.builder()
                .id("my_skill")
                .name("My Skill")
                .description("What this skill does")
                .addExample("Example query")
                .build())
            .build();
    }
}
```

#### 2. LangChain4j Agent Interface

```java
@RegisterAiService
public interface MyAgent {

    @SystemMessage("You are a helpful AI assistant.")
    String chat(@UserMessage String userMessage);

    // With tools
    @SystemMessage("You are an assistant with tools.")
    String chatWithTools(@UserMessage String userMessage);
}
```

#### 3. Tools Definition

```java
@ApplicationScoped
public class MyTools {

    @Tool("Description of what this tool does")
    public String myTool(String param) {
        // Implement tool logic
        return "Result";
    }

    @Tool("Another tool")
    public int calculate(int a, int b) {
        return a + b;
    }
}
```

#### 4. Executor Implementation

```java
@ApplicationScoped
public class MyAgentExecutor implements AgentExecutor {

    @Inject
    MyAgent agent;

    @Override
    public void execute(
        ExecutionContext context,
        ExecutionEventQueue eventQueue
    ) throws Exception {

        // Get user message
        String userMessage = context.getTaskInstruction();

        // Update status
        eventQueue.enqueue(AgentExecutionStateEvent.builder()
            .state(ExecutionState.THINKING)
            .description("Processing...")
            .build());

        // Call agent
        String response = agent.chat(userMessage);

        // Send response
        eventQueue.enqueue(AgentExecutionTextEvent.builder()
            .text(response)
            .build());

        // Mark complete
        eventQueue.enqueue(AgentExecutionStateEvent.builder()
            .state(ExecutionState.COMPLETED)
            .build());
    }

    @Override
    public void cancel(
        ExecutionContext context,
        ExecutionEventQueue eventQueue
    ) {
        eventQueue.enqueue(AgentExecutionStateEvent.builder()
            .state(ExecutionState.CANCELLED)
            .build());
    }
}
```

#### 5. Executor Producer

```java
@ApplicationScoped
public class MyExecutorProducer {

    @Inject
    MyAgentExecutor executor;

    @Produces
    @ApplicationScoped
    public AgentExecutor agentExecutor() {
        return executor;
    }
}
```

## Configuration

### application.properties

```properties
# Server Configuration
quarkus.http.port=11000

# LangChain4j Configuration
quarkus.langchain4j.openai.api-key=${OPENAI_API_KEY}
quarkus.langchain4j.openai.chat-model.model-name=gpt-4
quarkus.langchain4j.openai.chat-model.temperature=0.7

# Or use other providers:
# Google Gemini
# quarkus.langchain4j.google-ai-gemini.api-key=${GOOGLE_API_KEY}

# Azure OpenAI
# quarkus.langchain4j.azure-openai.api-key=${AZURE_API_KEY}
# quarkus.langchain4j.azure-openai.endpoint=${AZURE_ENDPOINT}

# Logging
quarkus.log.level=INFO
```

### pom.xml

```xml
<dependencies>
    <!-- A2A SDK -->
    <dependency>
        <groupId>com.google.a2a</groupId>
        <artifactId>a2a-java-sdk</artifactId>
        <version>0.3.0.Final</version>
    </dependency>

    <!-- Quarkus -->
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-arc</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-resteasy-reactive</artifactId>
    </dependency>

    <!-- LangChain4j -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-open-ai</artifactId>
    </dependency>
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-quarkus</artifactId>
    </dependency>
</dependencies>
```

## Creating a New Java Agent

### Step 1: Copy a Sample

```bash
# Copy the dice agent as a starting point
cp -r samples/java/agents/dice_agent_multi_transport my-agent
cd my-agent
```

### Step 2: Update Package Names

```bash
# Update package declarations in all .java files
# From: com.samples.a2a.dice
# To: com.example.a2a.myagent
```

### Step 3: Customize Agent Logic

1. **Update AgentCardProducer** - Change name, description, skills
2. **Modify Agent Interface** - Update system messages and methods
3. **Update Tools** - Add your custom tools
4. **Customize Executor** - Implement your logic

### Step 4: Configure Dependencies

Update `pom.xml` with:
- Correct artifact name
- Required dependencies
- LLM provider (OpenAI, Google, Azure, etc.)

### Step 5: Build and Run

```bash
# Build
mvn clean package

# Run in dev mode
mvn quarkus:dev

# Or run the JAR
java -jar target/quarkus-app/quarkus-run.jar
```

## Advanced Features

### Multi-Transport Support

Support both HTTP and gRPC:

```java
// application.properties
quarkus.grpc.server.port=9000
quarkus.http.port=11000
```

Implement gRPC service alongside HTTP.

### Authentication with Keycloak

```properties
# application.properties
quarkus.oidc.auth-server-url=https://keycloak.example.com/realms/myrealm
quarkus.oidc.client-id=my-agent
```

See `magic_8_ball_security` sample for full implementation.

### Memory and Conversation History

```java
@ApplicationScoped
public class ChatMemoryStore {

    private final Map<String, ChatMemory> memoryMap = new ConcurrentHashMap<>();

    public ChatMemory get(String sessionId) {
        return memoryMap.computeIfAbsent(
            sessionId,
            id -> MessageWindowChatMemory.withMaxMessages(10)
        );
    }
}
```

### Tool Integration Patterns

```java
// Simple tool
@Tool("Get current time")
public String getCurrentTime() {
    return LocalDateTime.now().toString();
}

// Tool with parameters
@Tool("Search for information")
public String search(
    @P("search query") String query,
    @P("maximum results") int maxResults
) {
    // Implement search
    return results;
}

// Tool with structured output
@Tool("Analyze sentiment")
public SentimentResult analyzeSentiment(@P("text") String text) {
    // Return structured object
    return new SentimentResult(sentiment, confidence);
}
```

## Running Examples

### Dice Agent

```bash
cd samples/java/agents/dice_agent_multi_transport
mvn quarkus:dev
```

Test:

```bash
curl -X POST http://localhost:11000/execute \
  -H "Content-Type: application/json" \
  -d '{"taskInstruction": "Roll 2 dice"}'
```

### Content Editor

```bash
cd samples/java/agents/content_editor
mvn quarkus:dev
```

### Weather MCP

```bash
cd samples/java/agents/weather_mcp
mvn quarkus:dev
```

## Deployment

### Native Image

```bash
# Build native image (requires GraalVM)
mvn package -Pnative

# Run
./target/my-agent-1.0.0-SNAPSHOT-runner
```

### Docker

```bash
# Build container
mvn package -Dquarkus.container-image.build=true

# Run
docker run -i --rm -p 11000:11000 my-agent:1.0.0-SNAPSHOT
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-agent
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-agent
  template:
    metadata:
      labels:
        app: my-agent
    spec:
      containers:
      - name: my-agent
        image: my-agent:1.0.0
        ports:
        - containerPort: 11000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai
```

## Testing

### Unit Tests

```java
@QuarkusTest
public class MyAgentExecutorTest {

    @Inject
    MyAgentExecutor executor;

    @Test
    public void testExecute() throws Exception {
        ExecutionContext context = new ExecutionContext();
        context.setTaskInstruction("test message");

        TestEventQueue queue = new TestEventQueue();

        executor.execute(context, queue);

        assertTrue(queue.hasTextEvent());
        assertTrue(queue.hasCompletedState());
    }
}
```

### Integration Tests

```bash
mvn verify
```

## Best Practices

1. **Use CDI** - Leverage dependency injection for clean code
2. **Type Safety** - Use Java's strong typing for tools
3. **Error Handling** - Catch and handle exceptions properly
4. **Logging** - Use proper logging frameworks
5. **Configuration** - Externalize configuration
6. **Testing** - Write comprehensive tests
7. **Documentation** - Document tools and APIs

## Troubleshooting

### Port already in use

```properties
# Change port in application.properties
quarkus.http.port=11001
```

### LangChain4j model not responding

Check API keys and model names in `application.properties`.

### Build failures

```bash
# Clean and rebuild
mvn clean install
```

## Resources

### Official Documentation
- [A2A Java SDK](https://github.com/a2aproject/a2a-java-sdk)
- [Quarkus Documentation](https://quarkus.io/guides/)
- [LangChain4j Documentation](https://docs.langchain4j.dev/)

### Sample Code
- All Java samples: `samples/java/agents/`
- Koog framework examples: `samples/java/koog/`

### Related Blueprints
- **Python Simple Agent**: Python-based A2A agent
- **JavaScript Agent**: TypeScript/Node.js agent

## Next Steps

1. **Start with samples** - Copy and modify an existing sample
2. **Customize gradually** - Change one thing at a time
3. **Test thoroughly** - Write tests as you go
4. **Deploy** - Start with dev mode, then containerize

## License

Apache 2.0
