/**
 * Genkit Prompts
 *
 * Prompts are reusable, testable templates for LLM interactions.
 */

import { definePrompt } from '@genkit-ai/ai';
import { gemini15Flash } from '@genkit-ai/googleai';
import { z } from 'zod';

/**
 * Example prompt definition
 *
 * TODO: Replace with your actual prompts
 */
export const myPrompt = definePrompt(
  {
    name: 'myPrompt',
    description: 'A simple example prompt',

    // Input schema
    input: z.object({
      input: z.string().describe('The user input'),
    }),

    // Output schema (optional, for structured output)
    output: z.object({
      response: z.string(),
    }),

    // Model configuration
    model: gemini15Flash,
    config: {
      temperature: 0.7,
    },
  },
  // Prompt template
  async (input) => ({
    messages: [
      {
        role: 'system',
        content: 'You are a helpful AI assistant.',
      },
      {
        role: 'user',
        content: input.input,
      },
    ],
  })
);

/**
 * Example: Structured output prompt
 */
export const structuredPrompt = definePrompt(
  {
    name: 'structuredPrompt',
    description: 'Returns structured JSON output',

    input: z.object({
      text: z.string(),
    }),

    output: z.object({
      sentiment: z.enum(['positive', 'negative', 'neutral']),
      confidence: z.number(),
      keywords: z.array(z.string()),
    }),

    model: gemini15Flash,
  },
  async (input) => ({
    messages: [
      {
        role: 'system',
        content: 'Analyze the sentiment and extract keywords from the text.',
      },
      {
        role: 'user',
        content: input.text,
      },
    ],
  })
);

/**
 * Example: Multi-turn conversation prompt
 */
export const conversationPrompt = definePrompt(
  {
    name: 'conversationPrompt',
    description: 'Handles multi-turn conversations',

    input: z.object({
      history: z.array(
        z.object({
          role: z.enum(['user', 'assistant']),
          content: z.string(),
        })
      ),
      currentMessage: z.string(),
    }),

    model: gemini15Flash,
  },
  async (input) => ({
    messages: [
      {
        role: 'system',
        content: 'You are a helpful assistant engaged in a conversation.',
      },
      ...input.history,
      {
        role: 'user',
        content: input.currentMessage,
      },
    ],
  })
);
