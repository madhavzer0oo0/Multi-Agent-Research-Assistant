from ollama import chat

class CriticAgent:
    def __init__(self,model='llama3.2'):
        self.model=model
    def run(self,report):
        prompt = f"""
        You are an expert research reviewer. Critically evaluate the following research report.
        Provide a 3-4 line review on each of the following aspects:
        - Strengths
        - Weaknesses
        - Missing points or unclear arguments
        - Suggestions for improvement

        Report:
        {report}
        """
        result=chat(model=self.model,messages=[{"role":"user","content":prompt}])
        return result['message']['content']