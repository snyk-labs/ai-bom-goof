from openai import OpenAI


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

        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_input
        )

        print(f"Assistant: {response.output_text}\n")


if __name__ == "__main__":
    main()
