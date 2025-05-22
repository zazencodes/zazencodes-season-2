# main.py
import logging
import os

import discord
from dotenv import load_dotenv
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("DiscordBot")

load_dotenv()

QUESTION_SYSTEM_PROMPT = """
Generate an AI-engineering related trivia question that is different each time it is requested.

The question should be short. One sentence max and keep it short and to the point.

DO NOT output the answer to the question.

Vary the topic, difficulty, and format (e.g., multiple choice, true/false, open-ended).
Use randomness in selecting from AI history, famous researchers, key breakthroughs, ethical dilemmas, real-world applications, futuristic AI concepts,
software engineering practices in AI, MLOps, model deployment strategies, AI system architecture, performance optimization techniques, or AI infrastructure design.

The question should be mid-range difficulty. Something that people might have the answer to, but difficult enough that it's interesting.

Again, it's crucial that you only ask a question without revealing the answer.
""".strip()

REPLY_SYSTEM_PROMPT = """
<system>
Evaluate if the answer to the AI trivia question is correct. Respond with a friendly explanation of whether it's right or wrong, and provide the correct answer if it's wrong.

If it's partially correct or even completely right, still provide more information for additional context. If any reasoning was provided then make sure you speak to that when you provide an answer.

Keep your answer succinct and do not ask any follow-up question.
</system>

Below are some examples of how you should respond:

<correct_answer_example>
Yes, that's correct! The AI program that defeated Garry Kasparov in 1997 is indeed called Deep Blue.

Deep Blue was specifically designed to evaluate millions of chess positions per second, which allowed it to outmaneuver Kasparov, who was considered one of the greatest chess players of all time.
</correct_answer_example>

<incorrect_answer_example>
The answer you provided is not correct. The first computer program to defeat a reigning world champion in chess was actually Deep Blue, developed by IBM. This historic event took place in 1997 when Deep Blue defeated Garry Kasparov, who was the world champion at the time.

Stockfish is indeed a powerful chess engine, but it came after Deep Blue and has not played a match against a reigning world champion in the same way.
</incorrect_answer_example>
""".strip()


CHANNEL_NAME = "general-chat"
MODEL = "gpt-4o-mini"
PROMPTS = {
    "stage_1": [
        {
            "role": "system",
            "content": QUESTION_SYSTEM_PROMPT,
        },
        {"role": "user", "content": "Generate a single trivia question."},
    ],
    "stage_2": lambda question, user_answer: [
        {
            "role": "system",
            "content": REPLY_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {user_answer}",
        },
    ],
}


# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Store question context for verification
question_context = {}

# question_context[1338704307951767552] = {
#     "question": "What is the best ai model in terms of benchmarks in 2024?",
#     "user_id": 416455497789472768,
# }


async def generate_ai_question() -> str:
    logger.debug("Generating AI question...")
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=PROMPTS["stage_1"],
        )
        logger.debug(f"Generated question: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        return "Well, this is awkward. It seems that I'm broken right now. Maybe I used all my magic OpenAI API jelly beans. Hopefully Alex can get me online again soon!"


async def verify_answer(question, user_answer):
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=PROMPTS["stage_2"](question, user_answer),
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error verifying answer: {str(e)}")
        return "Thanks for your answer! Due to technical difficulties, I couldn't verify it right now. Go tell Alex to fix me."


@client.event
async def on_ready():
    logger.info(f"Bot logged in as {client.user}")
    logger.info(f"Bot is in {len(client.guilds)} guilds")
    for guild in client.guilds:
        logger.info(f"- {guild.name} (id: {guild.id})")
        # List all channels in each guild
        for channel in guild.channels:
            logger.info(f"  > {channel.name} (id: {channel.id})")


@client.event
async def on_member_join(member):
    logger.info(f"New member joined: {member.name} (id: {member.id})")

    # Try to find general-chat channel
    channel = discord.utils.get(member.guild.channels, name=CHANNEL_NAME)
    if not channel:
        logger.error(f"Could not find suitable channel in guild {member.guild.name}")
        return

    logger.info(f"Using channel: {channel.name} (id: {channel.id})")

    try:
        # Generate AI trivia question
        question = await generate_ai_question()

        # Store the question context
        question_context[channel.id] = {"question": question, "user_id": member.id}

        # Send welcome message with question
        logger.info(f"Sending welcome message to channel {channel.id}")
        logger.info(f"Setting question context {question_context}")
        await channel.send(
            f"Welcome {member.mention}! In honor of your arrival, I've come up with a question just for you. Post your best guess and feel free to talk through your reasoning. No cheating!\n\n{question}"
        )
        logger.info("Welcome message sent successfully")

    except Exception as e:
        logger.error(f"Error in on_member_join: {str(e)}", exc_info=True)


@client.event
async def on_message(message):
    logger.debug(f"Message received in channel {message.channel.id}")
    logger.debug(f"Current question contexts: {question_context}")

    if message.author == client.user:
        # Ignore messages from the bot itself
        return

    if message.channel.id in question_context:
        logger.info(f"Processing answer for question in channel {message.channel.id}")
        context = question_context[message.channel.id]

        try:
            # Verify the answer
            response = await verify_answer(context["question"], message.content)

            # Tag the original user in the response
            user = await message.guild.fetch_member(context["user_id"])
            await message.channel.send(f"{user.mention} {response}")
            logger.info("Answer response sent successfully")

            # Clear the question context
            del question_context[message.channel.id]

        except Exception as e:
            logger.error(f"Error processing answer: {str(e)}", exc_info=True)


if __name__ == "__main__":
    logger.info("Starting bot...")
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("No Discord bot token found in environment variables!")
        exit(1)
    client.run(token)
