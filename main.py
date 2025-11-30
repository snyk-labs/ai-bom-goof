from openai import OpenAI
import time


def main():
    client = OpenAI()

    print("OpenAI Chat App")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if not user_input:
            continue

        print("Assistant: ", end="", flush=True)
        
        stream = client.responses.create(
            model="gpt-4o-mini",
            instructions="Be concise and brief in your responses.",
            input=user_input,
            stream=True
        )

        for event in stream:
            if hasattr(event, 'delta') and event.delta:
                print(event.delta, end="", flush=True)
                time.sleep(0.15)
        
        print("\n")


if __name__ == "__main__":
    main()
