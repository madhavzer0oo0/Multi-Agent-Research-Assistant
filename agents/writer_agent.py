from ollama import chat

class WriterAgent:
    def __init__(self,model='llama3.2'):
        self.model=model
    def run(self,topic,summaries):
        combined='\n\n'.join(summaries)
        prompt = f"""
        Based on the following paper summaries, write a structured research report on '{topic}'.
        Include an introduction, main findings, and conclusion.

        Summaries:
        {combined}
        """
        response=chat(model=self.model,messages=[{"role":"user","content":prompt}])
        return response['message']['content']
