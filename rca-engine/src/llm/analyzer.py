import json
import ollama

SYSTEM_PROMPT = """
You are an expert DevOps engineer specializing in Root Cause Analysis (RCA) for CI/CD build failures.
Analyze the provided Jenkins log output and explain what went wrong.

Output ONLY valid JSON matching this schema:
{
  "summary": "Short 1-sentence failure summary",
  "root_cause": "Detailed explanation of why the build failed",
  "suggested_fix": "Concrete code change or command to fix the issue"
}
"""

def analyze_log_context(parsed_log_context: str, model_name: str = "llama3.2") -> dict:
    """
    Sends the parsed log context to a local Ollama model and returns a structured RCA report.
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Jenkins Log Context:\n\n{parsed_log_context}"}
            ],
            format="json"  # Forces structured JSON output from Ollama
        )
        
        # Parse output into a Python dictionary
        result = json.loads(response['message']['content'])
        return result
    except Exception as e:
        return {
            "error": f"Failed to perform RCA analysis: {str(e)}"
        }