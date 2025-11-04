from transformers import pipeline

# Load summarizer once (this will download the model the first time)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_sentences: int = 2) -> str:
    """
    Summarize text locally using BART.
    """
    if not text or len(text.split()) < 30:
        return text  # skip if too short

    # Rough length control (each sentence ~20 words)
    max_len = max_sentences * 25
    min_len = max_sentences * 10

    summary = summarizer(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )

    return summary[0]['summary_text']

if __name__ == "__main__":
    sample = (
        "Apple announced a new AI partnership with OpenAI to enhance Siri and iPhone features. "
        "This collaboration will integrate GPT technology into iOS, focusing on better natural language understanding "
        "and smarter suggestions for users."
    )
    print("🔍 Summary:", summarize_text(sample))

