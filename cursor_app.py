import subprocess
import json

def sentiment_analysis(text: str):
    # Run your MCP remote tool via subprocess
    result = subprocess.run(
        [
            r"C:\Users\rocki\AppData\Roaming\npm\mcp-remote.cmd",
            "https://nazish-qamar-sentiment-prediction.hf.space/gradio_api/mcp/sse",
            "--transport", "sse-only",
            "--tool", "sentiment-analysis",
            "--arg", f"text={text}"
        ],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        raise RuntimeError(f"MCP call failed: {result.stderr}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout


if __name__ == "__main__":
    feedback = "The product was amazing, I would definitely recommend it!"
    sentiment = sentiment_analysis(feedback)
    print("Input:", feedback)
    print("Output:", sentiment)
