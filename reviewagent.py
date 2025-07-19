import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools import fetch_pr_files_tool, post_inline_comments_tool

class ReviewBot:
    def __init__(self):
        self._setup_environment()
        self.llm = self._setup_llm()
        self.tools = [fetch_pr_files_tool, post_inline_comments_tool]
        self.standards = self._gather_standards()
        self.agent = self._configure_agent()

    def _setup_environment(self):
        load_dotenv()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GEMINI_API_KEY is not set in the environment.")

    def _setup_llm(self):
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=self.api_key
        )

    def _read_file_contents(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception:
            return ""

    def _gather_standards(self):
        sections = [
            self._read_file_contents("clean_code_standards.md")
        ]
        return "\n\n".join(filter(None, sections))

    def _configure_agent(self):
        reviewer_instructions = (
            "You are a detail-oriented Senior Engineer assigned to perform focused, actionable, and standards-driven code reviews for pull requests.\n"
            "Tasks and constraints:\n"
            "1. Retrieve the latest diff with `fetch_pr_files_tool` (use only once per session).\n"
            f"2. Review all code changes using these standards:\n{self.standards}\n"
            "3. Only comment on added lines (marked with '+'); do not comment on deletions, test files, documentation, or unchanged lines.\n"
            "4. Comments must refer to the exact absolute line in the new file, counting only added and context lines, and must provide actionable, non-nitpicky feedback.\n"
            "5. Suggestions should address bugs, security, major logic, or clear violations of standards — not nitpicks or subjective style.\n"
            "6. All inline comments must be submitted together with `post_inline_comments_tool` (only once per session)."
            "7. Do not generate explanations outside the tool usage. After commenting, do not call further tools."
        )
        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=reviewer_instructions
        )

    def start_review(self):
        print("Starting pull request review agent...")
        self.agent.invoke(
            {"messages": [{"role": "user", "content": "Begin review."}]}
        )
        print("Review session finished.")

if __name__ == "__main__":
    bot = ReviewBot()
    bot.start_review()
