import re

def extract_error_context(log_text: str, max_lines: int = 100) -> str:
    """
    Scans raw Jenkins console log for common failure markers (BUILD FAILURE, Exception, Error)
    and extracts relevant surrounding lines to keep prompt size manageable.
    """
    lines = log_text.splitlines()
    error_indices = []

    # Common failure indicators in Jenkins logs
    failure_keywords = [r"BUILD FAILURE", r"ERROR", r"Exception", r"FATAL", r"FAILED"]
    pattern = re.compile("|".join(failure_keywords), re.IGNORECASE)

    for idx, line in enumerate(lines):
        if pattern.search(line):
            error_indices.append(idx)

    if not error_indices:
        # If no explicit keyword matches, return tail of log
        return "\n".join(lines[-max_lines:])

    # Extract surrounding lines around the first detected error spike
    first_error = error_indices[0]
    start = max(0, first_error - 10)
    end = min(len(lines), first_error + max_lines)

    return "\n".join(lines[start:end])