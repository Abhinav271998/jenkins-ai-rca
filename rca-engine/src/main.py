from src.parsers.log_parser import extract_error_context
from src.llm.analyzer import analyze_log_context

# Mock Jenkins failure log for testing
SAMPLE_JENKINS_LOG = """
[INFO] Scanning for projects...
[INFO] Building my-app 1.0-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO] --- maven-compiler-plugin:3.8.1:compile (default-compile) @ my-app ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 2 source files to /app/target/classes
[ERROR] /app/src/main/java/com/demo/App.java:[14,23] cannot find symbol
[ERROR]   symbol:   variable unknownVariable
[ERROR]   location: class com.demo.App
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.412 s
[INFO] Finished at: 2026-03-24T10:00:00Z
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.1:compile
"""

def main():
    print("1. Parsing raw Jenkins log...")
    context = extract_error_context(SAMPLE_JENKINS_LOG)
    print(f"--- Extracted Log Context ---\n{context}\n-----------------------------\n")

    print("2. Sending extracted context to Ollama local model...")
    rca_result = analyze_log_context(context)

    print("3. Received RCA Report:")
    import json
    print(json.dumps(rca_result, indent=2))

if __name__ == "__main__":
    main()