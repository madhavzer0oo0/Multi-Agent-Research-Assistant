from ollama import chat

class SummerizerAgent:
    def __init__(self,model='llama3.2'):
        self.model=model
    def run(self,paper):
        prompt = f"""
        Summarize the following research abstract clearly and concisely:

        Title: {paper['title']}
        Abstract: {paper['abstract']}
        """
        response=chat(model=self.model,messages=[{"role":"user","content":prompt}])
        return response['message']['content']

        