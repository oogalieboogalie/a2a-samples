# A2A JavaScript/TypeScript Agent Blueprint

A template for creating A2A (Agent-to-Agent) protocol agents using TypeScript, Express.js, and Firebase Genkit.

## What This Blueprint Provides

This blueprint gives you a complete starting point for building an A2A agent with:

- ✅ **TypeScript** for type safety and better DX
- ✅ **Express.js** for HTTP server
- ✅ **Firebase Genkit** for AI/prompt management
- ✅ **Tool/function calling** support
- ✅ **Streaming** responses
- ✅ **Multi-model support** (Gemini, GPT, Claude)
- ✅ **Structured prompts** with Zod schemas

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- API keys for AI providers (Google AI, OpenAI, etc.)

### Installation

```bash
# Install dependencies
npm install

# or
yarn install
```

### Configuration

Create `.env` file:

```bash
# Server
PORT=41000

# AI Provider (choose one or more)
GOOGLE_API_KEY=your_google_api_key_here
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional
LOG_LEVEL=info
NODE_ENV=development
```

### Running

```bash
# Development (with hot reload)
npm run dev

# Build
npm run build

# Production
npm start
```

The agent will start on `http://localhost:41000` by default.

### Testing

```typescript
import { A2AClient } from '@a2a-protocol/client';

const client = new A2AClient('http://localhost:41000');

// Get agent card
const card = await client.getAgentCard();
console.log(`Agent: ${card.name}`);

// Send a message
for await (const event of client.executeTask('Hello, agent!')) {
  if (event.type === 'text') {
    console.log(event.text);
  }
}
```

## Project Structure

```
javascript-agent/
├── src/
│   ├── index.ts          # Server entry point
│   ├── executor.ts       # Agent execution logic
│   ├── genkit.ts         # Genkit configuration
│   ├── prompts.ts        # Prompt definitions
│   └── tools.ts          # Tool definitions
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── .env                  # Environment variables
└── README.md             # This file
```

## Customization Guide

### 1. Update Agent Metadata

Edit `src/index.ts`:

```typescript
function createAgentCard(): AgentCard {
  return {
    name: 'Your Agent Name',  // Change this
    description: 'What your agent does',  // Change this
    skills: [
      {
        id: 'your_skill',
        name: 'Your Skill',
        description: 'What this skill does',
        examples: ['Example 1', 'Example 2'],
      },
    ],
  };
}
```

### 2. Implement Agent Logic

Edit `src/executor.ts`:

```typescript
async generateResponse(userMessage: string): Promise<string> {
  // Option 1: Simple generation
  const result = await generate({
    model: gemini15Flash,
    prompt: userMessage,
  });
  return result.text();

  // Option 2: Use custom prompt
  const result = await myPrompt({ input: userMessage });
  return result.text();

  // Option 3: With tools
  const result = await generate({
    model: gemini15Flash,
    prompt: userMessage,
    tools: [myTool, otherTool],
  });
  return result.text();
}
```

### 3. Add Custom Prompts

Edit `src/prompts.ts`:

```typescript
export const myCustomPrompt = definePrompt(
  {
    name: 'myCustomPrompt',
    description: 'What this prompt does',

    input: z.object({
      query: z.string(),
      context: z.string().optional(),
    }),

    output: z.object({
      answer: z.string(),
      confidence: z.number(),
    }),

    model: gemini15Flash,
    config: {
      temperature: 0.7,
    },
  },
  async (input) => ({
    messages: [
      {
        role: 'system',
        content: 'You are a specialized assistant.',
      },
      {
        role: 'user',
        content: `${input.query}\n\nContext: ${input.context || 'None'}`,
      },
    ],
  })
);
```

### 4. Add Custom Tools

Edit `src/tools.ts`:

```typescript
export const myCustomTool = defineTool(
  {
    name: 'myCustomTool',
    description: 'What this tool does',

    inputSchema: z.object({
      param1: z.string().describe('Description of param1'),
      param2: z.number().optional(),
    }),

    outputSchema: z.object({
      result: z.any(),
      success: z.boolean(),
    }),
  },
  async (input) => {
    // Implement your tool logic
    const result = doSomething(input.param1, input.param2);

    return {
      result,
      success: true,
    };
  }
);
```

## Advanced Patterns

### Streaming Responses

```typescript
const { stream } = await generate({
  model: gemini15Flash,
  prompt: userMessage,
  streamingCallback: async (chunk) => {
    await eventQueue.enqueue({
      type: 'text',
      text: chunk.text(),
      append: true,  // Append to previous text
    });
  },
});

await stream();
```

### Multi-Model Support

```typescript
import { gemini15Flash } from '@genkit-ai/googleai';
import { gpt4 } from '@genkit-ai/openai';
import { claude3Sonnet } from '@genkit-ai/anthropic';

// Use different models for different tasks
const result = await generate({
  model: gemini15Flash,  // or gpt4, claude3Sonnet
  prompt: userMessage,
});
```

### Structured Output

```typescript
export const structuredPrompt = definePrompt(
  {
    name: 'structuredPrompt',

    output: z.object({
      category: z.string(),
      sentiment: z.enum(['positive', 'negative', 'neutral']),
      keywords: z.array(z.string()),
      confidence: z.number().min(0).max(1),
    }),

    model: gemini15Flash,
  },
  async (input) => ({
    messages: [
      {
        role: 'system',
        content: 'Analyze and categorize the input.',
      },
      {
        role: 'user',
        content: input.text,
      },
    ],
  })
);

// Use it
const result = await structuredPrompt({ text: 'Your text here' });
// result is typed and validated!
```

### Multi-Turn Conversations

```typescript
// Store conversation history
const history: Array<{ role: string; content: string }> = [];

// Add to history
history.push({ role: 'user', content: userMessage });

// Generate response with history
const result = await generate({
  model: gemini15Flash,
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    ...history,
  ],
});

// Add response to history
history.push({ role: 'assistant', content: result.text() });
```

### Error Handling

```typescript
async execute(context, eventQueue) {
  try {
    const result = await this.generateResponse(context.taskInstruction);

    await eventQueue.enqueue({
      type: 'text',
      text: result,
    });

    await eventQueue.enqueue({
      type: 'state',
      state: 'completed',
    });
  } catch (error) {
    console.error('Agent error:', error);

    await eventQueue.enqueue({
      type: 'state',
      state: 'failed',
      description: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}
```

### Publishing Artifacts

```typescript
// Send images, files, or structured data
await eventQueue.enqueue({
  type: 'artifact',
  artifact: {
    content: Buffer.from(imageData),
    contentType: 'image/png',
    name: 'result.png',
  },
});
```

## Genkit Features

### Testing Prompts

```bash
# Start Genkit developer UI
npm run genkit:dev

# Test prompts and tools in the UI
# Navigate to http://localhost:4000
```

### Tracing and Debugging

```typescript
// Enable tracing in development
configureGenkit({
  enableTracingAndMetrics: true,
  telemetry: {
    instrumentation: 'googleCloud',
    logger: 'winston',
  },
});
```

### Custom Models

```typescript
import { defineModel } from '@genkit-ai/ai';

export const myCustomModel = defineModel({
  name: 'my-custom-model',
  async generate(request) {
    // Call your custom model API
    const response = await fetch('https://api.example.com/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });

    return await response.json();
  },
});
```

## Deployment

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 41000

CMD ["npm", "start"]
```

Build and run:

```bash
docker build -t my-agent .
docker run -p 41000:41000 --env-file .env my-agent
```

### Cloud Deployment

#### Google Cloud Run

```bash
# Build
gcloud builds submit --tag gcr.io/PROJECT_ID/my-agent

# Deploy
gcloud run deploy my-agent \
  --image gcr.io/PROJECT_ID/my-agent \
  --platform managed \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

#### AWS Lambda (with adapter)

```bash
npm install @vendia/serverless-express

# Update index.ts to export handler
export const handler = serverlessExpress({ app });
```

## Testing

### Unit Tests

```typescript
import { MyAgentExecutor } from './executor';

describe('MyAgentExecutor', () => {
  it('should generate response', async () => {
    const executor = new MyAgentExecutor();
    const mockQueue = createMockEventQueue();

    await executor.execute(
      { taskInstruction: 'test' },
      mockQueue
    );

    expect(mockQueue.events).toContainEqual(
      expect.objectContaining({ type: 'text' })
    );
  });
});
```

### Integration Tests

```bash
npm test
```

## Best Practices

1. **Type Safety** - Use TypeScript and Zod schemas
2. **Error Handling** - Always catch and handle errors
3. **Logging** - Use structured logging
4. **Validation** - Validate all inputs with Zod
5. **Testing** - Write tests for prompts and tools
6. **Security** - Sanitize inputs, use environment variables
7. **Performance** - Use streaming for long responses

## Related Blueprints

- **Python Simple Agent**: Python-based A2A agent
- **Python Tool-Using Agent**: Advanced tool patterns
- **Java Quarkus Agent**: Java-based A2A agent

## Resources

- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)
- [Genkit Documentation](https://firebase.google.com/docs/genkit)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## License

Apache 2.0
