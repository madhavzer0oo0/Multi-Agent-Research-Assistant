from agents.research_agent import ResearchAgent
from agents.summerizer_agent import SummerizerAgent 
from agents.writer_agent import WriterAgent
from agents.critic_agent import CriticAgent

class Coordinator:
    def __init__(self,topic:str):
        self.topic=topic
        self.research = ResearchAgent(topic)
        self.summarizer=SummerizerAgent()
        self.writer=WriterAgent()
        self.critic=CriticAgent()
    def run(self,max_results=3):
        print(f"🧠 Starting research process for topic: {self.topic}\n")
        print("📚 Fetching research papers...")
        papers = self.research.run(max_results=max_results)
        print("📝 Summarizing papers...")
        summaries = []
        for i, paper in enumerate(papers, start=1):
            print(f"   → Summarizing paper {i}/{len(papers)}")
            summary = self.summarizer.run(paper)
            summaries.append(summary)
        print("✅ All papers summarized!\n")

        print("✍️ Generating structured research report...")
        draft = self.writer.run(self.topic, summaries)
        print("✅ Draft complete!\n")
        print("🔍 Getting critic feedback...")
        feedback = self.critic.run(draft)
        print("✅ Feedback generated!\n")

        final_output = f"""
        🧾 FINAL RESEARCH REPORT
        ========================

        **Topic:** {self.topic}

        ---  
        **Draft Report:**  
        {draft}

        ---  
        **Critic Feedback:**  
        {feedback}
        """

        print("🚀 Research process complete!\n")
        return final_output

     
