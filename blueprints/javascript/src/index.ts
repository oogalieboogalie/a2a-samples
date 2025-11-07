/**
 * A2A JavaScript/TypeScript Agent Blueprint - Main Entry Point
 *
 * This template shows how to create an A2A agent using TypeScript,
 * Express.js, and Firebase Genkit for prompt management.
 */

import express from 'express';
import dotenv from 'dotenv';
import { AgentCard, AgentExecutor, createA2AServer } from '@a2a-protocol/core';
import { MyAgentExecutor } from './executor.js';
import { initializeGenkit } from './genkit.js';

// Load environment variables
dotenv.config();

const PORT = parseInt(process.env.PORT || '41000', 10);

/**
 * Create and configure the AgentCard
 */
function createAgentCard(): AgentCard {
  return {
    // Basic identification
    name: 'JavaScript Agent',  // TODO: Customize your agent name
    description: 'A TypeScript/JavaScript A2A agent with Genkit integration',  // TODO: Customize
    url: `http://localhost:${PORT}/`,
    version: '1.0.0',

    // Communication modes
    defaultInputModes: ['text'],
    defaultOutputModes: ['text'],
    // Can also include: 'image', 'artifact'

    // Agent capabilities
    capabilities: {
      streaming: true,
      pushNotifications: false,
      stateTransitionHistory: false,
    },

    // Skills this agent can perform
    skills: [
      {
        id: 'example_skill',  // TODO: Customize skill ID (snake_case)
        name: 'Example Skill',  // TODO: Customize skill name
        description: 'Demonstrates a basic skill',  // TODO: Customize
        tags: ['example', 'demo'],
        examples: [
          'Show me an example',
          'Demonstrate the skill',
        ],  // TODO: Add example queries
      },
      // TODO: Add more skills as needed
    ],

    // Advanced: Support role-based extended cards
    supportsAuthenticatedExtendedCard: false,
  };
}

/**
 * Start the A2A agent server
 */
async function main() {
  console.log('Starting JavaScript A2A Agent...');

  // Initialize Genkit (for AI/prompts)
  await initializeGenkit();

  // Create Express app
  const app = express();

  // Create agent card and executor
  const agentCard = createAgentCard();
  const agentExecutor: AgentExecutor = new MyAgentExecutor();

  // Create A2A server middleware
  const a2aRouter = createA2AServer({
    agentCard,
    agentExecutor,
  });

  // Mount A2A routes
  app.use('/', a2aRouter);

  // Health check endpoint
  app.get('/health', (req, res) => {
    res.json({ status: 'healthy', agent: agentCard.name });
  });

  // Start server
  app.listen(PORT, () => {
    console.log(`✓ ${agentCard.name} running on port ${PORT}`);
    console.log(`  URL: ${agentCard.url}`);
    console.log(`  Skills: ${agentCard.skills?.map(s => s.name).join(', ')}`);
  });
}

// Error handling
process.on('unhandledRejection', (error) => {
  console.error('Unhandled rejection:', error);
  process.exit(1);
});

// Start the server
main().catch((error) => {
  console.error('Failed to start server:', error);
  process.exit(1);
});
