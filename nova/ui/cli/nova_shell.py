"""
NOVA Intelligent CLI Shell.
Interactive shell with fuzzy command suggestions and context awareness.
"""

import sys
from nova.agents.core.nova_mind import NovaMind
from nova.voice.voice_interface import VoiceInterface

COMMANDS = ["help", "todo add", "todo list", "todo toggle", "todo delete", "profile", "exit", "quit"]

def fuzzy_match(input_cmd: str) -> list:
    return [cmd for cmd in COMMANDS if input_cmd.lower() in cmd]

def run_shell():
    mind = NovaMind()
    voice = VoiceInterface()

    print("==========================================")
    print("      Welcome to NOVA 2.0 Shell           ")
    print("==========================================")
    print("Type 'help' for available commands or 'exit' to quit.\n")

    while True:
        try:
            user_input = input("NOVA> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting NOVA Shell.")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if user_input.lower() == "help":
            print("Available commands:", ", ".join(COMMANDS))
            continue

        if user_input.lower() == "profile":
            print("User Profile:", mind.user_profile.to_dict())
            continue

        matches = fuzzy_match(user_input)
        if matches and user_input not in COMMANDS:
            print(f"Did you mean: {', '.join(matches)}?")

        res = mind.process_query(user_input)
        print(f"\n[NOVA Response]: {res['response']}\n")
        voice.speak(res['response'])

if __name__ == "__main__":
    run_shell()
