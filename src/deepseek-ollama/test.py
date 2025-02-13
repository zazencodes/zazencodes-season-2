import json
import random
import sys


# Add colored text capabilities using ANSI escape codes
def print_colored(text, color):
    if color == "red":
        print(f"\033[1;31m{text}\033[0m")
    elif color == "blue":
        print(f"\033[1;34m{text}\033[0m")
    elif color == "green":
        print(f"\033[1;32m{text}\033[0m")
    elif color == "yellow":
        print(f"\033[1;33m{text}\033[0m")


# Define emoji categories
categories = {
    "animals": ["🐱", "🐭", "🐹", "🦊", "🐶"],
    "food": ["🍕", "🍔", "🍟", "🍩", "🍪"],
    "nature": ["🌿", "🌼", "🌳", "🌈", "⭐"],
    "objects": ["🎮", "🎲", "🎧", "📚", "🎨"],
}

# Load or create the favorites file
favorites_file = "favorites.json"
try:
    with open(favorites_file, "r") as f:
        favorites = json.load(f)
except FileNotFoundError:
    favorites = {"animals": [], "food": [], "nature": [], "objects": []}
    with open(favorites_file, "w") as f:
        json.dump(favorites, f)

# Add color to the welcome message
print_colored("🎉 Funny Emoji Generator 🎉", "blue")
print("-" * 50)
print_colored("Welcome to the Funny Emoji Generator! 😄", "green")

while True:
    print(
        "\nAvailable categories:\n1. Animals\n2. Food\n3. Nature\n4. Objects\n5. Random Combination\n6. Favorites\n7. Help\n8. Exit"
    )

    user_input = input("\nEnter your choice: ").strip().lower()

    if user_input == "help":
        print(
            "Here are the commands you can use:\n1. animals - Show animal emojis\n2. food - Show food emojis\n3. nature - Show nature emojis\n4. objects - Show object emojis\n5. random - Generate a random combination\n6. favorites - View your favorites\n7. add - Add an emoji to favorites\n8. exit - Close the generator"
        )
        continue

    if user_input == "exit":
        print("Goodbye! 😊")
        sys.exit(0)

    elif user_input in ["animals", "food", "nature", "objects"]:
        category = user_input
        print_colored("\nCurrent Category: " + category.capitalize() + "\n", "yellow")
        for emoji in categories[category]:
            print_colored(emoji, "red")
        continue

    elif user_input == "random":
        # Generate a random combination from all categories
        all_emojis = []
        for category in categories:
            all_emojis.extend(categories[category])

        random_combination = random.sample(all_emojis, k=min(5, len(all_emojis)))
        print_colored("\nRandom Combination:\n", "blue")
        for emoji in random_combination:
            print_colored(emoji, "green")
        input("Press Enter to continue...")
        continue

    elif user_input == "favorites":
        if not favorites["animals"]:
            print("No favorites in this category yet.")
        else:
            print_colored("\nYour Favorites:\n", "blue")
            for emoji in favorites["animals"]:
                print_colored(emoji, "green")
            for emoji in favorites["food"]:
                print_colored(emoji, "red")
            for emoji in favorites["nature"]:
                print_colored(emoji, "green")
            for emoji in favorites["objects"]:
                print_colored(emoji, "blue")
        continue

    elif user_input == "add":
        print("Enter an emoji to add to your favorites:")
        emoji = input().strip()
        if emoji in categories.values():
            print(f"{emoji} is already a valid emoji.")
        else:
            # Add to the first category (animals by default)
            favorites["animals"].append(emoji)
            with open(favorites_file, "w") as f:
                json.dump(favorites, f)
            print("Added to your favorites!")
        continue

    elif user_input == "delete":
        print("Enter an emoji to delete from favorites:")
        emoji = input().strip()
        if emoji in favorites.values():
            favorites_list = list(favorites.items())
            for category in favorites_list:
                if emoji in favorites[category]:
                    del favorites[category][favorites[category].index(emoji)]
                    with open(favorites_file, "w") as f:
                        json.dump(favorites, f)
                    print("Emoji deleted from favorites!")
        else:
            print("This emoji is not in your favorites.")
        continue

    elif user_input == "clear":
        favorites = {"animals": [], "food": [], "nature": [], "objects": []}
        with open(favorites_file, "w") as f:
            json.dump(favorites, f)
        print("Favorites cleared!")
        continue
