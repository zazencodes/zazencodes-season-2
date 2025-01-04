#!/usr/bin/env python3


def read_file():
    try:
        filename = input("Enter the file name: ")
        with open(filename, "r") as file:
            for line in file:
                print(line.rstrip())
    except IOError as e:
        print(f"Error: Could not read file. {e}")  # Use f-string for formatting
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Use f-string for formatting


if __name__ == "__main__":
    read_file()
