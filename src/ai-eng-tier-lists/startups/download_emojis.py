import os
import time

import requests


def emoji_to_codepoint(emoji):
    codepoint = [f"{ord(char):x}" for char in emoji][0]
    return codepoint


emojis = [
    "🏋️‍♂️",
    "🗓️",
    "🛒",
    "⚙️",
    "🌐",
    "💰",
    "🛠️",
    "🚀",
    "📋",
    "🎧",
    "🛍️",
    "📊",
    "🤖",
    "📜",
    "✍️",
    "🎥",
    "📑",
    "🏗️",
    "🏡",
]

# Create directory for downloaded emojis
os.makedirs("emojis", exist_ok=True)

# Download each emoji as PNG from the Noto Emoji GitHub repository
base_url = "https://github.com/googlefonts/noto-emoji/blob/main/png/128/"

for emoji in emojis:
    codepoint = emoji_to_codepoint(emoji)
    url = f"{base_url}emoji_u{codepoint}.png?raw=true"
    response = requests.get(url)
    time.sleep(0.5)

    if response.status_code == 200:
        with open(f"emojis/{codepoint}.png", "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {emoji} -> {codepoint}.png")
    else:
        print(f"Failed to download: {emoji} ({codepoint})")
