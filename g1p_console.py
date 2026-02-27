from model_gateway import call_model

def main():
    prompt = input("What do you want to build today? ")

    print("\n=== GPT-4o-mini (G1P) ===")
    print(call_model(prompt, "gpt-4o-mini", user_id="console_user"))

    print("\n=== Claude 3.5 Sonnet (G1P) ===")
    print(call_model(prompt, "claude-3-5-sonnet-20241022", user_id="console_user"))

if __name__ == "__main__":
    main()
