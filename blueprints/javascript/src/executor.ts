/**
 * A2A JavaScript Agent Blueprint - Executor Implementation
 *
 * The AgentExecutor handles incoming requests and generates responses.
 */

import { z } from 'zod';
import {
  AgentExecutor,
  ExecutionContext,
  ExecutionEventQueue,
  AgentExecutionEvent,
} from '@a2a-protocol/core';
import { generate } from '@genkit-ai/ai';
import { gemini15Flash } from '@genkit-ai/googleai';
import { myPrompt } from './prompts.js';
import { myTool } from './tools.js';

/**
 * Main agent executor that processes user requests
 */
export class MyAgentExecutor implements AgentExecutor {
  /**
   * Execute the agent's task
   *
   * @param context - Execution context with user message and parameters
   * @param eventQueue - Queue for publishing events (messages, status updates)
   */
  async execute(
    context: ExecutionContext,
    eventQueue: ExecutionEventQueue
  ): Promise<void> {
    // Get user's message
    const userMessage = context.taskInstruction;

    try {
      // Update status to "thinking"
      await eventQueue.enqueue({
        type: 'state',
        state: 'thinking',
        description: 'Processing your request...',
      });

      // TODO: Implement your agent logic here
      // Options:
      // 1. Use Genkit prompts (see below)
      // 2. Call external APIs
      // 3. Use tools/functions
      // 4. Process data

      // Example: Using Genkit with prompt and tools
      const response = await this.generateResponse(userMessage);

      // Send response back to user
      await eventQueue.enqueue({
        type: 'text',
        text: response,
      });

      // Mark task as completed
      await eventQueue.enqueue({
        type: 'state',
        state: 'completed',
        description: 'Task completed successfully!',
      });
    } catch (error) {
      // Handle errors
      await eventQueue.enqueue({
        type: 'state',
        state: 'failed',
        description: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      });
    }
  }

  /**
   * Generate a response using Genkit
   *
   * TODO: Replace with your actual generation logic
   */
  private async generateResponse(userMessage: string): Promise<string> {
    // Example 1: Simple text generation
    // const result = await generate({
    //   model: gemini15Flash,
    //   prompt: userMessage,
    // });
    // return result.text();

    // Example 2: Using a defined prompt
    // const result = await myPrompt({
    //   input: userMessage,
    // });
    // return result.text();

    // Example 3: With tools
    // const result = await generate({
    //   model: gemini15Flash,
    //   prompt: userMessage,
    //   tools: [myTool],
    // });
    // return result.text();

    // Simple placeholder response
    return `You said: "${userMessage}". I'm a TypeScript agent template - customize me to do more!`;
  }

  /**
   * Handle task cancellation
   *
   * This method is called when a user/agent requests to cancel the current task.
   */
  async cancel(
    context: ExecutionContext,
    eventQueue: ExecutionEventQueue
  ): Promise<void> {
    await eventQueue.enqueue({
      type: 'state',
      state: 'cancelled',
      description: 'Task cancelled by user.',
    });
  }
}

/**
 * Advanced Pattern: Streaming Agent Executor
 *
 * Example of an agent that sends incremental updates
 */
export class StreamingAgentExecutor implements AgentExecutor {
  async execute(
    context: ExecutionContext,
    eventQueue: ExecutionEventQueue
  ): Promise<void> {
    const userMessage = context.taskInstruction;

    await eventQueue.enqueue({
      type: 'state',
      state: 'thinking',
      description: 'Starting to generate response...',
    });

    // Streaming with Genkit
    const { stream } = await generate({
      model: gemini15Flash,
      prompt: userMessage,
      streamingCallback: async (chunk) => {
        // Send each chunk as it arrives
        await eventQueue.enqueue({
          type: 'text',
          text: chunk.text(),
          append: true,  // Append to previous text
        });
      },
    });

    // Wait for completion
    await stream();

    await eventQueue.enqueue({
      type: 'state',
      state: 'completed',
      description: 'Streaming complete!',
    });
  }

  async cancel(
    context: ExecutionContext,
    eventQueue: ExecutionEventQueue
  ): Promise<void> {
    await eventQueue.enqueue({
      type: 'state',
      state: 'cancelled',
      description: 'Streaming cancelled.',
    });
  }
}

/**
 * Advanced Pattern: Tool-Using Agent Executor
 *
 * Example of an agent that uses tools/functions
 */
export class ToolUsingAgentExecutor implements AgentExecutor {
  async execute(
    context: ExecutionContext,
    eventQueue: ExecutionEventQueue
  ): Promise<void> {
    const userMessage = context.taskInstruction;

    await eventQueue.enqueue({
      type: 'state',
      state: 'thinking',
      description: 'Selecting appropriate tool...',
    });

    // Use Genkit with tools
    const result = await generate({
      model: gemini15Flash,
      prompt: userMessage,
      tools: [myTool],  // Add your tools here
      config: {
        temperature: 0.7,
      },
    });

    // Extract tool calls and results
    const toolCalls = result.toolCalls();
    if (toolCalls && toolCalls.length > 0) {
      for (const toolCall of toolCalls) {
        await eventQueue.enqueue({
          type: 'text',
          text: `\nCalled tool: ${toolCall.name}\nResult: ${JSON.stringify(toolCall.output, null, 2)}\n`,
        });
      }
    }

    // Send final response
    await eventQueue.enqueue({
      type: 'text',
      text: result.text(),
    });

    await eventQueue.enqueue({
      type: 'state',
      state: 'completed',
      description: 'Done!',
    });
  }

  async cancel(
    context: ExecutionContext,
    eventQueue: ExecutionEventQueue
  ): Promise<void> {
    await eventQueue.enqueue({
      type: 'state',
      state: 'cancelled',
      description: 'Cancelled.',
    });
  }
}
