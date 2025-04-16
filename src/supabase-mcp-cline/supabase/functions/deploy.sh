#!/bin/bash

# Supabase Edge Function Deployment Script

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "Supabase CLI is not installed. Please install it first:"
    echo "npm install -g supabase"
    exit 1
fi

# Check if user is logged in
if ! supabase projects list &> /dev/null; then
    echo "You are not logged in to Supabase CLI. Please login first:"
    echo "supabase login"
    exit 1
fi

# Get project reference
PROJECT_REF="mtrdeegsedalhmrmqdwl"
echo "Using project reference: $PROJECT_REF"

# Link project
echo "Linking project..."
supabase link --project-ref $PROJECT_REF

# Deploy the generate-image function
echo "Deploying generate-image function..."
supabase functions deploy generate-image --no-verify-jwt

# Prompt for OpenAI API key
echo ""
echo "Please enter your OpenAI API key:"
read -s OPENAI_API_KEY

# Set the OpenAI API key as a secret
if [ -n "$OPENAI_API_KEY" ]; then
    echo "Setting OpenAI API key as a secret..."
    supabase secrets set OPENAI_API_KEY=$OPENAI_API_KEY
    echo "Deployment completed successfully!"
else
    echo "No API key provided. Please set it manually:"
    echo "supabase secrets set OPENAI_API_KEY=your_api_key"
fi

echo ""
echo "Your Edge Function is now deployed and ready to use!"
