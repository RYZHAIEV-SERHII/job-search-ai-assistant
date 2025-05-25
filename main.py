"""Main entry point for the job-search-ai-assistant project."""

import uvicorn

from src.job_search_ai_assistant.assistant import assistant

job_search_ai_assistant = assistant()

if __name__ == "__main__":
    uvicorn.run(job_search_ai_assistant, host="127.0.0.1", port=8000)
