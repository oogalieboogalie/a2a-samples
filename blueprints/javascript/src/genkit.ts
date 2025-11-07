/**
 * Firebase Genkit Configuration
 *
 * Genkit provides:
 * - Prompt management
 * - Tool/function calling
 * - Multi-model support
 * - Streaming
 */

import { configureGenkit } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';

/**
 * Initialize Genkit with your preferred model provider
 */
export async function initializeGenkit() {
  configureGenkit({
    // Configure model plugins
    plugins: [
      // Google AI (Gemini)
      googleAI({
        apiKey: process.env.GOOGLE_API_KEY,
      }),

      // TODO: Add other providers as needed:
      // OpenAI:
      // openAI({ apiKey: process.env.OPENAI_API_KEY }),
      //
      // Anthropic (Claude):
      // anthropic({ apiKey: process.env.ANTHROPIC_API_KEY }),
      //
      // Vertex AI:
      // vertexAI({ projectId: process.env.GOOGLE_CLOUD_PROJECT }),
    ],

    // Logging configuration
    logLevel: process.env.LOG_LEVEL || 'info',

    // Enable tracing for debugging
    enableTracingAndMetrics: process.env.NODE_ENV === 'development',
  });

  console.log('✓ Genkit initialized');
}
