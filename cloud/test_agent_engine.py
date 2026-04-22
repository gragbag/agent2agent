import json
import os
import sys

import vertexai
from vertexai.preview import reasoning_engines

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))

PROJECT_ID = "agent2agent-493406"
REGION = "us-central1"
ENGINE_ID = "5792100167041679360"


def main() -> None:
    vertexai.init(project=PROJECT_ID, location=REGION)

    agent = reasoning_engines.ReasoningEngine(
        f"projects/{PROJECT_ID}/locations/{REGION}/reasoningEngines/{ENGINE_ID}"
    )

    response = agent.query(message_text="Hello from Vertex AI Agent Engine!")
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
