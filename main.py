from agents.coordinator_agent import Coordinator

def main():
    topic=input("Enter the topic for the article:")
    coordinator = Coordinator(topic=topic)
    result = coordinator.run()

    # Save result to file for inspection
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(result)

    print("\n✅ Final report saved to 'final_report.txt'")


if __name__=="__main__":
    main()