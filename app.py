import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from tavily import TavilyClient

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("API_TOKEN"),
    base_url="https://openrouter.ai/api/v1"
)

tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def load_profile(pdf_path: str) -> str:
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

PROFILE = load_profile("Adebanke_Eunice_CV.pdf")

SYSTEM_PROMPT = f"""You are Adebanke Eunice, a final-year Computer Engineering student at Federal University Oye Ekiti with a CGPA of 4.81/5.0 and an aspiring ML Engineer based in Nigeria.

You are chatting directly with recruiters, collaborators, and visitors on your portfolio. Speak naturally in first person — as yourself.

Here is your profile information:
{PROFILE}

Your personality:
- Warm, confident, and enthusiastic about your work
- Passionate about ML, AI, and solving real-world problems
- Hardworking — you balance a sysadmin internship at Xpresspay while building ML projects
- Ambitious — actively targeting ML Engineering and Data Science roles from August 2025

Guidelines:
- Always say "I", "my", "me" — never "she", "her", or "Adebanke"
- Be conversational but professional
- When mentioning projects, always share the GitHub link and live demo if available
- If asked about availability, say you are open to opportunities starting August 2025
- If asked something not in your profile, use the web_search tool to find relevant info
- If asked something personal you can't answer, say "That's not something I've shared here, but feel free to reach out at adebankepeke04@gmail.com or connect with me on LinkedIn!"
- Never make up information not in your profile or found via search
- End responses with a follow-up question or invitation to learn more when appropriate
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information about Adebanke's projects, GitHub, LinkedIn, or any relevant topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def perform_web_search(query: str) -> str:
    try:
        result = tavily.search(query=query, max_results=3)
        return "\n".join([r["content"] for r in result["results"]])
    except Exception as e:
        return f"Search failed: {str(e)}"


def chat(message: str, history: list) -> str:
    try:
        # Build message history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for item in history:
            if isinstance(item, dict):
                messages.append({"role": item["role"], "content": item["content"]})
            else:
                user_msg, bot_msg = item
                messages.append({"role": "user", "content": user_msg})
                if bot_msg:
                    messages.append({"role": "assistant", "content": bot_msg})

        messages.append({"role": "user", "content": message})

        # First call
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1000
        )

        response_message = response.choices[0].message

        # Handle tool calls
        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "web_search":
                    import json
                    args = json.loads(tool_call.function.arguments)
                    search_result = perform_web_search(args["query"])

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": search_result
                    })

            second_response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages,
                max_tokens=1000
            )
            return second_response.choices[0].message.content

        return response_message.content

    except Exception as e:
        return f"Error: {str(e)}"


# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(title="Adebanke Eunice | Portfolio") as demo:

    gr.Markdown("""
    # Adebanke Eunice
    ### Computer Engineering Student | ML Engineer in the Making
    *Feel free to ask me about my skills, projects, experience, or how to get in touch.*
    """)

    chatbot = gr.ChatInterface(
        fn=chat,
        examples=[
            "What projects have you built?",
            "What are your technical skills?",
            "Are you open to job opportunities?",
            "Tell me about your churn prediction project",
            "How can I contact you?",
        ],
        cache_examples=False,
    )

    gr.Markdown("""
    ---
    📧 adebankepeke04@gmail.com &nbsp;|&nbsp;
    🔗 [LinkedIn](https://linkedin.com/in/adebankedev) &nbsp;|&nbsp;
    💻 [GitHub](https://github.com/AdebankeDev)
    """)

if __name__ == "__main__":
    demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    theme=gr.themes.Soft(primary_hue="blue")
)
