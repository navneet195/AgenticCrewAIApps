from langchain.tools import BaseTool
from .client import Client as LinkedinClient

class LinkedInTool(BaseTool):
    name: str = "retrieve_linkedin_profiles"  # Define name with type annotation
    description: str = "Retrieve LinkedIn profiles given a list of skills. Comma separated."  # Define description with type annotation

    def _run(self, skills: str) -> str:
        linkedin_client = LinkedinClient()
        people = linkedin_client.find_people(skills)
        people = self._format_people_to_text(people)
        linkedin_client.close()
        return people

    def _arun(self, skills: str):
        raise NotImplementedError("Async support not implemented.")

    def _format_people_to_text(self, people):
        result = [
            "\n".join([
                "Person Profile",
                "-------------",
                p['name'],
                p['position'],
                p['location'],
                p["profile_link"],
            ]) for p in people
        ]
        return "\n\n".join(result)
