import gradio as gr

def letter_counter(word: str, letter: str) -> int:
    """
    Count the number of occurrences of a letter in a word or text.

    Args:
        word (str): The input text to search through
        letter (str): The letter to search for

    Returns:
        int: The number of times the letter appears in the text
    """
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count

def reverse_text(text: str) -> str:
    """Reverse the input text."""
    return text[::-1]

# Create a standard Gradio interface
letter_count_ui = gr.Interface(
    fn=letter_counter,
    inputs=["textbox", "textbox"],
    outputs="number",
    title="Letter Counter",
    description="Enter text and a letter to count how many times the letter appears in the text."
)

# Create a standard Gradio interface
word_reverse_ui = gr.Interface(
    fn=reverse_text,
    inputs=["textbox"],
    outputs="text",
    title="Word reverse",
    description="Enter text to reverse the text."
)

# Combine them into one app
demo = gr.TabbedInterface(
    [letter_count_ui, word_reverse_ui],
    ["Letter Counter", "Reverse Text"]
)

# Launch both the Gradio web interface and the MCP server
if __name__ == "__main__":
    demo.launch(mcp_server=True)