# AI Research Team - Automated Research Workflow

## Overview

AI Research Team is a multi-agent research automation platform built with Flask and LangGraph. It leverages advanced language models (Google Gemini via LangChain) to automate the process of researching, analyzing, and reporting on any topic. The system simulates a collaborative team of AI agents—each with specialized roles—to deliver comprehensive, structured research reports with minimal human input.

## Features
- **Multi-Agent Workflow:** Simulates a team of AI agents (Researcher, Analyst, Writer, Supervisor) for end-to-end research automation.
- **Broadened Research Sources:**
  - **Arsiv Agent:** Searches for and summarizes research papers from academic sources.
  - **Tavily Agent:** Performs web searches for the latest and most relevant information.
  - **Translator Agent:** Translates and summarizes non-English or complex content from Arsiv and Tavily agents.
- **LLM-Powered:** Utilizes Google Gemini via LangChain for high-quality, context-aware research and analysis.
- **Web Interface:** Simple Flask web app for entering research topics and viewing generated reports.
- **Modular Codebase:** Clean, maintainable architecture with clear separation of concerns (agents, workflow, LLM setup, state management).
- **Extensible:** Easily add new agent types or customize workflows for advanced use cases.

## Tech Stack
- **Backend:** Python, Flask
- **AI/LLM:** LangGraph, LangChain, Google Gemini (Generative AI)
- **Research Paper Search:** Arsiv Agent (arXiv or similar sources)
- **Web Search:** Tavily Agent (web search API or LLM-powered)
- **Translation/Summarization:** Translator Agent (LLM-powered)
- **Frontend:** HTML (Jinja2 templates)
- **Environment Management:** python-dotenv

## Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key ([get one here](https://ai.google.dev/))

### Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your-google-api-key-here
     ```

### Running the App
```bash
python app.py
```
- Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.
- Enter a research topic and receive a detailed, AI-generated report.

## Project Structure
```
├── app.py                # Flask app entry point
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not committed)
├── core/
│   ├── llm.py            # LLM setup and configuration
│   ├── state.py          # Shared state and type definitions
│   ├── agents.py         # Agent creation logic (Researcher, Analyst, Writer, Supervisor, Arsiv, Tavily, Translator)
│   └── workflow.py       # Workflow/graph logic
└── templates/
    └── index.html        # Web UI template
```

## Customization & Extensibility
- Add new agent types (e.g., more data sources, custom analysis) in `core/agents.py`.
- Modify or extend the workflow in `core/workflow.py`.
- Update the web UI in `templates/index.html`.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements, new features, or bug fixes.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Gemini](https://ai.google.dev/)
- [arXiv](https://arxiv.org/) (for research paper data) 