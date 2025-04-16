/**
 * OpenAI Image Generation Configuration
 * 
 * This file contains the configuration for OpenAI image generation settings.
 * The API key is securely stored in the Supabase Edge Function environment variables.
 */

const OPENAI_CONFIG = {
    // Default image generation settings
    imageSettings: {
        quality: 'hd',
        style: 'natural'
    }
};
