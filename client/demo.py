from client import A2AClient


def main():
    with A2AClient("https://agent2agent-1081000059174.us-central1.run.app") as client:
        card = client.fetch_agent_card()

        print(f"Agent name: {card.get('name', 'Unknown')}")

        skills = client.get_skills()
        print("Skills:")
        for skill in skills:
            print(f"- {skill.get('name')} ({skill.get('id')})")

        response = client.send_task("Hello from the client!")
        echoed_text = client.extract_text(response)

        print(f"Response: {echoed_text}")


if __name__ == "__main__":
    main()