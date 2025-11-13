from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import os
from openai import OpenAI
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Member Data Q&A System")

# Create templates directory if it doesn't exist
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)

# External API endpoint
MESSAGES_API_URL = "https://november7-730026606190.europe-west1.run.app/messages"

# Initialize OpenAI client (will be set when needed)
# Loads from .env file first, then falls back to environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
client = None
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

# Cache for messages (refresh every 5 minutes)
_messages_cache = None
_cache_timestamp = 0
CACHE_TTL = 300  # 5 minutes


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


def fetch_all_messages(use_cache=True):
    """Fetch all messages from the external API with caching."""
    global _messages_cache, _cache_timestamp
    
    # Check cache
    if use_cache and _messages_cache is not None:
        if time.time() - _cache_timestamp < CACHE_TTL:
            return _messages_cache
    
    all_messages = []
    page = 1
    page_size = 100
    
    while True:
        try:
            params = {"page": page, "page_size": page_size}
            response = requests.get(MESSAGES_API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            if not items:
                break
                
            all_messages.extend(items)
            
            # Check if we've fetched all messages
            total = data.get("total", 0)
            if len(all_messages) >= total:
                break
                
            page += 1
            
        except requests.exceptions.RequestException as e:
            # If pagination fails, try without params to get all at once
            if page == 1:
                response = requests.get(MESSAGES_API_URL, timeout=30)
                response.raise_for_status()
                data = response.json()
                all_messages = data.get("items", [])
            break
    
    # Update cache
    _messages_cache = all_messages
    _cache_timestamp = time.time()
    
    return all_messages


def answer_question(question: str, messages: list) -> str:
    """Use OpenAI to answer questions based on the messages."""
    global client
    
    if not client:
        return "Error: OpenAI API key is not configured. Please set your OPENAI_API_KEY in the .env file or as an environment variable. See README.md for setup instructions."
    
    # Format messages for context (more efficient)
    context_parts = []
    for msg in messages:
        user_name = msg.get('user_name', 'Unknown')
        timestamp = msg.get('timestamp', '')
        message = msg.get('message', '')
        context_parts.append(f"User: {user_name} ({timestamp})\nMessage: {message}")
    
    context = "\n\n".join(context_parts)
    
    # Truncate context if too long (OpenAI has token limits ~128k tokens for gpt-4o-mini)
    # Approximate: 1 token ≈ 4 characters, so ~500k characters max
    # But we'll be conservative and use ~100k characters to stay safe
    max_context_length = 100000
    if len(context) > max_context_length:
        # Try to keep recent messages (they might be more relevant)
        context = context[-max_context_length:] + "\n\n[Earlier messages truncated...]"
    
    prompt = f"""You are a helpful assistant that answers questions about member data from messages.

Here are the messages from various members:

{context}

Based on the messages above, answer the following question. 

IMPORTANT INSTRUCTIONS:
- Provide a concise, natural answer without explicitly citing messages or using "Message:" format
- Write in a flowing, conversational style
- If the exact information is not available in the messages, say "I don't have that information in the available messages."
- If there is related information (e.g., mentions of car services but not car ownership), you can mention what related information exists
- Be specific but brief - avoid repeating message content verbatim
- If asking about quantities or ownership that isn't mentioned, clearly state that information is not available
- Keep answers under 3-4 sentences when possible

Question: {question}

Answer:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using a cost-effective model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context. Provide concise, natural answers without explicitly citing messages. Write in a conversational style."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
        
    except Exception as e:
        return f"Error processing question: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    html_file = templates_dir / "index.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    else:
        return """
        <html>
            <body>
                <h1>Member Data Q&A System</h1>
                <p>API is running. Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Answer a natural language question about member data."""
    try:
        # Fetch messages
        messages = fetch_all_messages()
        
        if not messages:
            raise HTTPException(status_code=500, detail="Failed to fetch messages from the API")
        
        # Answer the question
        answer = answer_question(request.question, messages)
        
        return AnswerResponse(answer=answer)
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

