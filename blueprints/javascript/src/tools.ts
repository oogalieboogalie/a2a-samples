/**
 * Genkit Tools (Functions)
 *
 * Tools allow your agent to perform specific actions.
 */

import { defineTool } from '@genkit-ai/ai';
import { z } from 'zod';

/**
 * Example tool: Get current time
 */
export const getCurrentTime = defineTool(
  {
    name: 'getCurrentTime',
    description: 'Get the current date and time',

    // Input schema
    inputSchema: z.object({
      timezone: z.string().optional().describe('Timezone (e.g., "UTC", "America/New_York")'),
    }),

    // Output schema
    outputSchema: z.object({
      timestamp: z.string(),
      formatted: z.string(),
      timezone: z.string(),
    }),
  },
  async (input) => {
    const now = new Date();

    return {
      timestamp: now.toISOString(),
      formatted: now.toLocaleString('en-US', {
        timeZone: input.timezone || 'UTC',
      }),
      timezone: input.timezone || 'UTC',
    };
  }
);

/**
 * Example tool: Calculate something
 */
export const calculateTool = defineTool(
  {
    name: 'calculate',
    description: 'Perform a mathematical calculation',

    inputSchema: z.object({
      expression: z.string().describe('Mathematical expression to evaluate (e.g., "2 + 2")'),
    }),

    outputSchema: z.object({
      result: z.number(),
      expression: z.string(),
    }),
  },
  async (input) => {
    try {
      // WARNING: eval is dangerous! Use a proper math parser in production
      // Consider libraries like: mathjs, expr-eval
      const result = eval(input.expression);

      if (typeof result !== 'number') {
        throw new Error('Result is not a number');
      }

      return {
        result,
        expression: input.expression,
      };
    } catch (error) {
      throw new Error(`Failed to evaluate expression: ${error.message}`);
    }
  }
);

/**
 * Example tool: Make an API call
 */
export const apiCallTool = defineTool(
  {
    name: 'apiCall',
    description: 'Make an HTTP API call',

    inputSchema: z.object({
      url: z.string().url().describe('API endpoint URL'),
      method: z.enum(['GET', 'POST', 'PUT', 'DELETE']).optional().describe('HTTP method'),
    }),

    outputSchema: z.object({
      status: z.number(),
      data: z.any(),
    }),
  },
  async (input) => {
    const response = await fetch(input.url, {
      method: input.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    return {
      status: response.status,
      data,
    };
  }
);

/**
 * Example tool: Text processing
 */
export const textProcessingTool = defineTool(
  {
    name: 'processText',
    description: 'Analyze and process text',

    inputSchema: z.object({
      text: z.string().describe('Text to process'),
      operation: z
        .enum(['wordCount', 'reverse', 'uppercase', 'lowercase'])
        .describe('Operation to perform'),
    }),

    outputSchema: z.object({
      result: z.string(),
      operation: z.string(),
    }),
  },
  async (input) => {
    let result: string;

    switch (input.operation) {
      case 'wordCount':
        result = `Word count: ${input.text.split(/\s+/).length}`;
        break;
      case 'reverse':
        result = input.text.split('').reverse().join('');
        break;
      case 'uppercase':
        result = input.text.toUpperCase();
        break;
      case 'lowercase':
        result = input.text.toLowerCase();
        break;
      default:
        throw new Error(`Unknown operation: ${input.operation}`);
    }

    return {
      result,
      operation: input.operation,
    };
  }
);

/**
 * Export all tools for easy import
 */
export const myTool = getCurrentTime;  // TODO: Replace with your primary tool

export const allTools = [
  getCurrentTime,
  calculateTool,
  apiCallTool,
  textProcessingTool,
];
