from langchain_core.prompts import PromptTemplate
from agents.llm import DEFAULT_MODEL, build_llm, invoke_with_retry


class WriterAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = 0.2):
        self.llm = build_llm(model_name=model_name, temperature=temperature, max_tokens=1200)
        template = (
            "Write a detailed research report on the topic: '{topic}'.\n"
            "Use the provided source summaries to explain the state of existing work.\n\n"
            "The report must include these sections:\n"
            "1. Title\n"
            "2. Introduction and problem background\n"
            "3. What work has already been done on this topic\n"
            "   - Group related approaches together.\n"
            "   - Mention important systems, methods, models, datasets, or applications.\n"
            "4. Comparison of existing approaches\n"
            "   - Compare strengths, weaknesses, and tradeoffs.\n"
            "5. Current trends and common techniques\n"
            "6. Research gaps and unsolved problems\n"
            "7. Practical applications and real-world relevance\n"
            "8. Future scope and possible improvements\n"
            "9. Conclusion\n"
            "10. Sources used\n\n"
            "Important writing rules:\n"
            "- Be specific about what previous researchers or systems have already done.\n"
            "- Do not invent paper names, authors, metrics, or results that are not in the summaries.\n"
            "- If the summaries are limited, clearly say that more source review is needed.\n"
            "- Keep the tone academic but easy to understand.\n"
            "- Include source URLs in the Sources used section when available.\n\n"
            "- Keep the full report under 900 words.\n\n"
            "Summaries:\n{summaries}"
        )
        self.prompt = PromptTemplate(template=template, input_variables=["topic", "summaries"])
        self.chain = self.prompt | self.llm

    def run(self, topic: str, summaries: list) -> str:
        combined = "\n\n".join(summaries)
        response = invoke_with_retry(self.chain, {"topic": topic, "summaries": combined[:8000]})
        return response.content
