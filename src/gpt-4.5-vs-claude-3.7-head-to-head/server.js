const express = require('express');
const cors = require('cors');
const axios = require('axios');
const { OpenAI } = require('openai');
const Anthropic = require('@anthropic-ai/sdk');
const app = express();
const port = 3000;

// Get API keys from environment variables
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

// Initialize clients
const openai = new OpenAI({
  apiKey: OPENAI_API_KEY,
});

const anthropic = new Anthropic({
  apiKey: ANTHROPIC_API_KEY,
});

// Enable CORS for all routes
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Proxy endpoint for OpenAI with streaming
app.all('/api/openai', async (req, res) => {
  try {
    // Handle both GET (EventSource) and POST (fetch) requests
    const prompt = req.method === 'GET' ? req.query.prompt : req.body.prompt;
    const model = req.method === 'GET' ? req.query.model : req.body.model;

    if (!prompt || !model) {
      return res.status(400).json({ error: "Missing prompt or model parameter" });
    }

    if (!OPENAI_API_KEY) {
      return res.status(400).json({ error: "OpenAI API key not found in environment variables" });
    }

    // Set up proper headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');

    // For EventSource preflight OPTIONS request
    if (req.method === 'OPTIONS') {
      res.status(200).end();
      return;
    }

    const stream = await openai.chat.completions.create({
      model: model,
      messages: [{ role: 'user', content: prompt }],
      stream: true,
    });

    // Stream the response chunks to the client
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) {
        res.write(`data: ${JSON.stringify({ content })}\n\n`);
      }
    }

    // End the stream
    res.write('data: [DONE]\n\n');

    console.log(JSON.stringify(stream));

    res.end();
  } catch (error) {
    console.error('OpenAI API error:', error);
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  }
});

// Proxy endpoint for Anthropic with streaming
app.all('/api/anthropic', async (req, res) => {
  try {
    // Handle both GET (EventSource) and POST (fetch) requests
    const prompt = req.method === 'GET' ? req.query.prompt : req.body.prompt;
    const model = req.method === 'GET' ? req.query.model : req.body.model;

    if (!prompt || !model) {
      return res.status(400).json({ error: "Missing prompt or model parameter" });
    }

    if (!ANTHROPIC_API_KEY) {
      return res.status(400).json({ error: "Anthropic API key not found in environment variables" });
    }

    // Set up proper headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');

    // For EventSource preflight OPTIONS request
    if (req.method === 'OPTIONS') {
      res.status(200).end();
      return;
    }

    // Use the stream method with event handlers
    const stream = await anthropic.messages.stream({
      model: model,
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000,
    });

    // Handle text chunks
    stream.on('text', (text) => {
      res.write(`data: ${JSON.stringify({ content: text })}\n\n`);
    });

    // Handle errors during streaming
    stream.on('error', (error) => {
      console.error('Anthropic streaming error:', error);
      res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
      res.end();
    });

    // Handle stream completion
    stream.on('end', () => {
      res.write('data: [DONE]\n\n');
      console.log(JSON.stringify(stream));
      res.end();
    });

    // Start the stream
    await stream.done();
  } catch (error) {
    console.error('Anthropic API error:', error);
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
