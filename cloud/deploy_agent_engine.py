from pathlib import Path
import importlib.util
import sys

import vertexai
from vertexai.preview import reasoning_engines


PROJECT_ID = "agent2agent-493406"
REGION = "us-central1"
STAGING_BUCKET = f"gs://{PROJECT_ID}-a2a-staging"
DISPLAY_NAME = "Echo A2A Agent"
DESCRIPTION = "A2A Lab - Echo Agent on Agent Engine"

REPO_ROOT = Path(__file__).resolve().parent.parent
WRAPPER_PATH = REPO_ROOT / "agent_engine_wrapper.py"


def _load_echo_agent_class():
    sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location("agent_engine_wrapper", WRAPPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {WRAPPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EchoAgent


def main() -> None:
    vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=STAGING_BUCKET)
    EchoAgent = _load_echo_agent_class()

    remote_agent = reasoning_engines.ReasoningEngine.create(
        EchoAgent(),
        requirements=[
            "fastapi==0.111.0",
            "uvicorn[standard]==0.29.0",
            "pydantic==2.13.0",
            "httpx==0.28.1",
            "cloudpickle==3.1.2",
        ],
        extra_packages=[str(REPO_ROOT / "agent_engine_wrapper.py")],
        display_name=DISPLAY_NAME,
        description=DESCRIPTION,
        gcs_dir_name="echo-a2a-agent",
        sys_version="3.11",
    )

    print("Deployed! Resource name:", remote_agent.resource_name)
    print("Engine ID:", remote_agent.resource_name.split("/")[-1])


if __name__ == "__main__":
    main()
