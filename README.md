---
title: Portfolio Chatbot
emoji: 👩🏾‍💻
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 👩🏾‍💻 Adebanke's Portfolio Chatbot

An agentic portfolio chatbot that talks as me — powered by OpenAI GPT-4o-mini via OpenRouter, Tavily web search, built with Gradio, and deployed on Hugging Face Spaces via Docker.

🔗 **Live Demo:** https://huggingface.co/spaces/AdebankeDev/portfolio-chatbot

## Features
- Speaks in first person as me
- Answers questions about my skills, projects, and experience
- Tavily web search for live information (GitHub, LinkedIn, Streamlit apps)
- Clean, professional Gradio UI
- Fully Dockerized

## Run Locally

1. Clone the repo
2. Copy `.env.example` to `.env` and add your keys
3. Install dependencies:
```bash
   uv add openai gradio python-dotenv pypdf tavily-python
```
4. Run:
```bash
   uv run python app.py
```
5. Visit `http://localhost:7860`

## Run with Docker

```bash
docker build -t portfolio-chatbot .
docker run --env-file .env -p 7860:7860 portfolio-chatbot
```

## Deploy to Hugging Face Spaces

1. Create a new Space → Docker SDK → Blank template
2. Add HF as a remote:
```bash
   git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/portfolio-chatbot
```
3. Push:
```bash
   git push hf chatbot:main
```
4. Add secrets in Space Settings:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`

## Tech Stack
- [OpenRouter](https://openrouter.ai) — OpenAI API access
- [Tavily](https://tavily.com) — web search for AI agents
- [Gradio](https://gradio.app) — UI
- [Hugging Face Spaces](https://huggingface.co/spaces) — deployment
- Docker