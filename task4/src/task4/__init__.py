import os
import sys
# replaced direct import with guarded import
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def _get_api_key():
    # read API key from environment; don't hardcode keys
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    return key

# new: shared client instance
_client = None

def _summarize_paragraph(paragraph: str) -> str:
    """
    Send a single paragraph to the Chat Completions API (gpt-5-mini)
    and return the model's short-phrase summary.
    """
    if OpenAI is None:
        return "<error: openai package not installed>"
    if _client is None:
        return "<error: OpenAI client not initialized>"
    # system instruction asks for a very short phrase summary
    messages = [
        {"role": "system", "content": "You are a concise summarizer. Produce a short phrase (no more than 4 words) that captures the task described."},
        {"role": "user", "content": paragraph},
    ]
    try:
        resp = _client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            max_tokens=16,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"<error: {e}>"


def main() -> None:
    if OpenAI is None:
        print("Missing dependency 'openai'. Install with: uv add openai  (or)  pip install openai")
        return
    # initialize client (reads API key from env or use explicit)
    try:
        api_key = _get_api_key()
    except Exception as e:
        print(e)
        return
    global _client
    _client = OpenAI(api_key=api_key)

    # Longer, multi-sentence paragraph-length descriptions
    sample_paragraphs = [
        (
            "Build a small command-line utility that recursively scans a directory tree to locate files exceeding a configurable size threshold and produces a structured JSON report. "
            "The report should include absolute file paths, sizes in bytes, human-readable sizes, last-modified timestamps (ISO 8601), and an indicator for whether the file is readable by the current user. "
            "The tool must accept command-line arguments for the target directory, the size threshold (with suffixes like KB/MB/GB), an optional output file path, and a verbose flag for progress reporting. "
            "It should handle permission errors gracefully (skipping unreadable directories but logging them), be reasonably performant for large trees, and include a brief usage message and exit codes for success, partial failures, and fatal errors."
        ),
        (
            "Create a lightweight web service that accepts CSV payloads via POST requests, validates the CSV format and schema, and returns a JSON summary containing per-column statistics (count, mean, median, standard deviation, min, max) plus counts of missing or malformed entries. "
            "The service should support optional query parameters to control which statistics are computed and accept a header row or allow user-specified column names. "
            "Responses must use appropriate HTTP status codes for success (200), client errors (400) such as malformed CSV, and server errors (500). "
            "Include input validation, clear error messages, and a small test suite demonstrating correct behavior for numeric, categorical, and missing-data cases. "
            "Document expected input formats and example requests in the README."
        ),
        (
            "Implement task3: design and deliver an automated test harness for the repository that can run unit and integration tests locally and in continuous integration. "
            "The harness should execute tests, collect coverage metrics, and fail the build when coverage for configured modules falls below a specified threshold; it should also generate machine-readable test reports in JUnit XML and a JSON summary for downstream tooling. "
            "Provide configuration files and example CI pipeline snippets (e.g., GitHub Actions) showing how to run the harness, how to upload artifacts, and how to interpret results. "
            "Include documentation that explains how to add new tests, standards for test naming and organization, and guidance on keeping tests fast and deterministic."
        ),
    ]

    # Loop over each paragraph independently and print a short phrase summary
    for idx, para in enumerate(sample_paragraphs, start=1):
        summary = _summarize_paragraph(para)
        print(f"Summary {idx}: {summary}")


if __name__ == "__main__":
    main()
