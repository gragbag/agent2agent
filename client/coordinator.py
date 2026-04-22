from client import A2AClient


ECHO_AGENT_URL = "https://echo-a2a-agent-5s56tqxt7q-uc.a.run.app"
REVERSE_AGENT_URL = "https://reverse-a2a-agent-5s56tqxt7q-uc.a.run.app"
INPUT_TEXT = "Hello from the coordinator script"


def _print_agent_info(label: str, client: A2AClient) -> None:
    card = client.fetch_agent_card()
    print(f"{label} agent: {card.get('name', 'Unknown')} ({card.get('id', 'unknown-id')})")
    print(f"{label} skills:")
    for skill in client.get_skills():
        print(f"- {skill.get('name')} ({skill.get('id')})")


def main() -> None:
    with A2AClient(ECHO_AGENT_URL) as echo_client, A2AClient(REVERSE_AGENT_URL) as reverse_client:
        _print_agent_info("Echo", echo_client)
        _print_agent_info("Reverse", reverse_client)

        print(f"Original input: {INPUT_TEXT}")

        echo_response = echo_client.send_task(INPUT_TEXT)
        echo_output = echo_client.extract_text(echo_response)
        print(f"Echo output: {echo_output}")

        reverse_response = reverse_client.send_task(echo_output)
        reverse_output = reverse_client.extract_text(reverse_response)
        print(f"Reverse output: {reverse_output}")


if __name__ == "__main__":
    main()
