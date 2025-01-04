import os
from typing import Optional

import openai


def sanitize_and_validate(prompt: str) -> str:
    """
    Sanitize and validate the input prompt before sending to the language model.

    Args:
        prompt (str): The input prompt to be validated

    Returns:
        str: The sanitized prompt

    Raises:
        ValueError: If prompt is empty, too long, or contains invalid content
    """
    if not isinstance(prompt, str):
        raise ValueError("Prompt must be a string")

    # Remove leading/trailing whitespace
    prompt = prompt.strip()

    # Check length constraints
    if len(prompt) < 1:
        raise ValueError("Prompt cannot be empty")
    if len(prompt) > 2000:
        raise ValueError("Prompt must be less than 2000 characters")

    # Basic HTML/script tag removal
    import re

    prompt = re.sub(r"<[^>]*>", "", prompt)

    # Remove any null bytes
    prompt = prompt.replace("\0", "")

    # Remove any control characters
    prompt = "".join(char for char in prompt if ord(char) >= 32 or char == "\n")

    # Filter out swear words
    swear_words = {
        "damn",
        "hell",
    }
    words = prompt.split()
    filtered_words = [
        "*" * len(word) if word.lower() in swear_words else word for word in words
    ]
    prompt = " ".join(filtered_words)

    return prompt


def chat_with_gpt(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> Optional[str]:
    """
    Send a prompt to ChatGPT and get a response.

    Args:
        prompt (str): The input prompt to send to ChatGPT
        model (str): The GPT model to use (default: "gpt-3.5-turbo")
        max_tokens (int): Maximum number of tokens in the response
        temperature (float): Controls randomness (0.0-1.0)

    Returns:
        Optional[str]: The model's response or None if there's an error
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Set up the OpenAI client
        openai.api_key = api_key

        # Make the API call
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Extract and return the response text
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error calling ChatGPT API: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Make sure to set your API key in environment variables first:
    # export OPENAI_API_KEY='your-api-key-here'

    prompt = input("Enter your question: ")
    validated_prompt = sanitize_and_validate(prompt)
    response = chat_with_gpt(validated_prompt)

    if response:
        print(f"ChatGPT: {response}")
    else:
        print("Failed to get response from ChatGPT")
