import arxiv

class ResearchAgent:
    def __init__(self,topic):
        self.topic=topic
    def run(self,max_results=5):
        search=arxiv.Search(
            query=self.topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        papers=[]
        for result in search.results():
            papers.append({
                "title":result.title,
                "abstract":result.summary,
                "url":result.entry_id,
                "authors":[a.name for a in result.authors],
                "published": result.published.strftime("%Y-%m-%d")
            })
        return papers
    