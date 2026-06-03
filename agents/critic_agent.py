from langchain_core.prompts import PromptTemplate
from agents.llm import DEFAULT_MODEL, build_llm, invoke_with_retry


class CriticAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = 0.2):
        self.llm = build_llm(model_name=model_name, temperature=temperature, max_tokens=350)
        template = (
            "You are an expert research reviewer. Critically evaluate the following research report.\n"
            "Provide a concise review with one short bullet for each aspect:\n"
            "- Strengths\n"
            "- Weaknesses\n"
            "- Missing points or unclear arguments\n"
            "- Whether it clearly explains what work has already been done\n"
            "- Whether research gaps and future scope are useful\n"
            "- Suggestions for improvement\n\n"
            "Report:\n{report}"
        )
        self.prompt = PromptTemplate(template=template, input_variables=["report"])
        self.chain = self.prompt | self.llm

    def run(self, report: str) -> str:
        response = invoke_with_retry(self.chain, {"report": report[:3500]})
        return response.content
