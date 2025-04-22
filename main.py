import importlib
import os

CHALLENGES_DIR = "challenges"
PROGRESS_FILE = "progress.txt"

def list_challenges():
    return sorted(
        [d for d in os.listdir(CHALLENGES_DIR)
         if os.path.isdir(os.path.join(CHALLENGES_DIR, d))
         and not d.startswith("__")]
    )

def update_progress(challenge_name):
    with open(PROGRESS_FILE, "a") as f:
        f.write(f"{challenge_name.capitalize()} Challenge: Cleared ✅\n")

def main():
    print("=== Signal3001 :: Challenge Launcher ===\n")
    challenges = list_challenges()
    
    if not challenges:
        print("[!] No challenges found.")
        return

    print("Available challenges:")
    for idx, ch in enumerate(challenges, 1):
        print(f"{idx}. {ch}")

    choice = input("\nEnter challenge name to run: ").strip().lower()

    if choice not in challenges:
        print("[x] Invalid challenge name.")
        return

    try:
        mod = importlib.import_module(f"{CHALLENGES_DIR}.{choice}.generate_{choice}")
        result = mod.run() if hasattr(mod, "run") else None

        if result is True:
            print("[✓] Flag correct.")
            update_progress(choice)
        elif result is False:
            print("[x] Flag incorrect.")
        else:
            print("[!] Challenge did not return a result.")

    except Exception as e:
        print(f"[!] Error loading challenge: {e}")

if __name__ == "__main__":
    main()
