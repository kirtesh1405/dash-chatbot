from utils.llm_interface import send_prompt_to_llm

def generate_summary(messages, backend="openai"):
    """
    Generate a one-liner summary of the conversation using the specified backend.
    """
    if not messages:
        return "Empty conversation"

    conversation_text = "\n".join([
        f"{m['role']}: {m['content']}" for m in messages[-10:]  # Use last 10 messages
    ])

    summary_prompt = f"Summarize this conversation in one sentence:\n\n{conversation_text}"
    return send_prompt_to_llm(summary_prompt, persona="You are a helpful summarizer.", backend=backend)
