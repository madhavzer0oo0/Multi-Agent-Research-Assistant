from langchain_core.prompts import PromptTemplate
from agents.llm import DEFAULT_MODEL, build_llm, invoke_with_retry


class SummerizerAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = 0.2):
        self.llm = build_llm(model_name=model_name, temperature=temperature, max_tokens=450)
        template = (
            "You are preparing notes for a literature review.\n"
            "Analyze the following research result and summarize it in a useful, factual way.\n\n"
            "Title: {title}\n"
            "Source URL: {url}\n"
            "Content: {abstract}\n\n"
            "Include:\n"
            "1. Existing work done in this source.\n"
            "2. Main method, system, model, or approach.\n"
            "3. Key contribution or finding.\n"
            "4. Limitations or unanswered questions.\n"
            "5. Relevance to the topic.\n"
            "Keep the summary under 180 words.\n"
        )
        self.prompt = PromptTemplate(template=template, input_variables=["title", "url", "abstract"])
        self.chain = self.prompt | self.llm

    def run(self, paper: dict) -> str:
        abstract = paper.get("abstract", "")
        response = invoke_with_retry(
            self.chain,
            {
                "title": paper.get("title", ""),
                "url": paper.get("url", ""),
                "abstract": abstract[:2500],
            }
        )
        return response.content

        
