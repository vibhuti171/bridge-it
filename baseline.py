from llm import generate_response

def baseline_response(user_message: str):
    prompt = f"""
You are an AI assistant for an education SaaS platform.
User says: {user_message}

Respond helpfully.
"""
    return generate_response(prompt)
