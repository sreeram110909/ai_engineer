import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

while True:
    
    # Ask the user if they want to use a system prompt
    system_prompt = input(
        "Enter a system prompt (press Enter to skip): "
    ).strip()
    
    
    # Get user input for the prompt
    prompt = input("Enter your prompt (or type 'exit' to quit): ")
    
    if(prompt.lower() == 'exit'):
        print("Exiting the program.")
        break;
    
    # Get user input for the maximum number of tokens
    try:
        max_tokens = int(input("Enter the maximum number of tokens: "))
        if(max_tokens <= 0):
            print("Please enter a positive integer for max tokens.")
            continue
    except ValueError:
        print("Invalid input. Please enter a valid integer for max tokens.")
        continue
    
    # Get user input for the temperature
    try:
        temperature = float(input("Enter the temperature (0.0 to 2.0): "))
        if(temperature < 0.0 or temperature > 2.0):
            print("Please enter a temperature between 0.0 and 2.0.")
            continue
        
    except ValueError:
        print("Invalid input. Please enter a valid float for temperature.")
        continue
    
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })
    
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temperature)
    
    usage = response.usage
    
    
    print("\nResponse:\n")
    print("\nTOKEN ANALYSIS\n")
    print(f"Model              : {model}")
    print(f"Prompt Tokens      : {usage.prompt_tokens}")
    print(f"Completion Tokens  : {usage.completion_tokens}")
    print(f"Total Tokens       : {usage.total_tokens}")
    print(f"Finish Reason      : {response.choices[0].finish_reason}")
    print(f"Temperature        : {temperature}")
    print(f"Max Tokens         : {max_tokens}")
    print("\n MODEL RESPONSE \n")
    print(response.choices[0].message.content)
    
    again = input(
        "\nEnter 'exit' to quit (press Enter to analyze another prompt): "
    ).strip().lower()

    if again == "exit":
        print("Thank you for using the Token Analyzer!")
        break