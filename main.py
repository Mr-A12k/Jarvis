from core.brain import Brain

jarvis = Brain()

print("JARVIS v0.1 Initialized")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = jarvis.think(user_input)

    print("\nIntent:", result["intent"])
    print("Confidence:", result["confidence"])
    print("Requires Action:", result["requires_action"])
    print("Response:", result["response"])
    print("-" * 50)