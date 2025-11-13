# Member Data Q&A System

A question-answering system that answers natural-language questions about member data from a public API using AI.

---

## 1. Problem Statement

The challenge was to build a simple question-answering system that can answer natural-language questions about member data provided by a public API. The system needs to:

- Accept natural language questions (e.g., "When is Layla planning her trip to London?", "How many cars does Vikram Desai have?", "What are Amira's favorite restaurants?")
- Fetch member messages from an external API endpoint: `https://november7-730026606190.europe-west1.run.app/messages`
- Process and understand the context from these messages
- Generate accurate, concise answers based on the available data
- Expose a simple API endpoint (`/ask`) that accepts questions and returns answers in the format: `{"answer": "..."}`
- Be deployable and publicly accessible

The system must handle large datasets efficiently, provide meaningful responses even when information is incomplete, and be user-friendly for both end-users and developers.

---

## 2. My Approach Towards the Problem

### Architecture & Design

I designed a **FastAPI-based REST service** with the following key components:

#### **2.1 Data Fetching & Caching**
- Implemented pagination support to fetch all messages from the external API
- Added a **5-minute caching mechanism** to reduce API calls and improve response times
- Handled edge cases like API failures and empty responses gracefully

#### **2.2 AI-Powered Question Answering**
- Integrated **OpenAI GPT-4o-mini** for cost-effective natural language processing
- Designed a context-aware prompt that:
  - Provides all member messages as context
  - Instructs the AI to give concise, natural answers without verbose citations
  - Handles cases where information is not available
- Implemented context truncation for large datasets (100k character limit) while prioritizing recent messages

#### **2.3 API Design**
- Created a clean REST API with:
  - `POST /ask` - Main endpoint for question answering
  - `GET /` - Web interface for easy interaction
  - `GET /health` - Health check endpoint
  - `GET /docs` - Auto-generated API documentation (Swagger UI)

#### **2.4 User Experience**
- Built a **modern, responsive web interface** with:
  - Clean, intuitive design
  - Example questions for quick testing
  - Loading indicators and error handling
  - Real-time question submission

#### **2.5 Security & Configuration**
- Implemented secure API key management using `.env` files
- Added `.env.example` template for easy setup
- Ensured `.env` files are gitignored to prevent accidental key exposure
- Provided clear error messages when configuration is missing

#### **2.6 Deployment Readiness**
- Created Dockerfile for containerized deployment
- Added Procfile for platform deployment (Railway, Heroku, etc.)
- Designed to work with environment variables for cloud deployments

### Technology Stack

- **FastAPI** - High-performance Python web framework
- **OpenAI GPT-4o-mini** - Efficient AI model for question answering
- **Python 3.11+** - Modern Python with type hints
- **Uvicorn** - ASGI server for production deployment
- **python-dotenv** - Environment variable management

---

## 3. Instructions to Run the Code

### Prerequisites

- Python 3.11 or higher
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step-by-Step Setup

#### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd qa-system
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure OpenAI API Key

**Option A: Using .env file (Recommended)**

1. Copy the example file:
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. Open `.env` in a text editor and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

**Option B: Using Environment Variable (Temporary)**

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"
```

> **Note:** Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys). Keep it secure and never commit it to version control.

#### Step 4: Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`. You should see output indicating the server is running.

---

## Using the Application

The application provides two ways to interact with it:

### Option 1: Using the API Endpoint (Required Format)

This is the **programmatic way** to use the service, which returns responses in the exact format specified: `{"answer": "..."}`

#### Endpoint Details

- **URL:** `POST http://localhost:8000/ask`
- **Content-Type:** `application/json`
- **Request Body:** `{"question": "your question here"}`
- **Response Format:** `{"answer": "response text"}`

#### Example Usage

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "When is Layla planning her trip to London?"}'
```

**Expected Response:**
```json
{
  "answer": "Layla is planning her trip to London in the first week of December."
}
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What are Amira's favorite restaurants?"}
)
data = response.json()
print(data["answer"])
```

**Using JavaScript/Node.js:**
```javascript
const response = await fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: "How many cars does Vikram Desai have?"
  })
});

const data = await response.json();
console.log(data.answer);
```

**Using PowerShell:**
```powershell
$body = @{
    question = "When is Layla planning her trip to London?"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/ask" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Write-Host $response.answer
```

#### Interactive API Documentation

For testing the API interactively, visit the Swagger UI documentation:

- **URL:** http://localhost:8000/docs

This provides an interactive interface where you can:
- Test the `/ask` endpoint directly in your browser
- See request/response schemas
- View example requests and responses
- Try different questions without writing code

---

### Option 2: Using the Web Interface (UI)

For a **user-friendly graphical interface**, use the web UI:

#### Access the Web Interface

1. Start the server (if not already running):
   ```bash
   python main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

#### Features

- **Clean, Modern Interface:** Beautiful gradient design with intuitive layout
- **Question Input:** Large text area for typing your questions
- **Example Questions:** Clickable example questions to get started quickly
- **Real-time Answers:** Answers appear instantly below the question
- **Loading Indicators:** Visual feedback while processing
- **Error Handling:** Clear error messages if something goes wrong

#### How to Use

1. Type your question in the text box (e.g., "When is Layla planning her trip to London?")
2. Click the "Ask Question" button
3. Wait for the answer to appear below
4. Try different questions using the example buttons or typing your own

#### Example Questions to Try

- "When is Layla planning her trip to London?"
- "How many cars does Vikram Desai have?"
- "What are Amira's favorite restaurants?"
- "What are Layla's travel preferences?"
- "Where is Vikram Desai traveling?"

---

### Additional Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```
Returns: `{"status": "healthy"}`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### Troubleshooting

**"OpenAI API key is not configured" Error:**
- Ensure you've created a `.env` file in the project root
- Verify the file contains: `OPENAI_API_KEY=sk-your-actual-key-here`
- Restart the application after creating/editing the `.env` file

---

## 4. Future Enhancements

Here are potential improvements that could be made to this project:

### 4.1 Enhanced AI Capabilities
- **Multi-model support**: Allow users to choose between different AI models (GPT-4, Claude, etc.)
- **Fine-tuning**: Train a custom model on the specific domain for better accuracy
- **Confidence scoring**: Provide confidence levels for answers
- **Answer sources**: Show which messages were used to generate the answer (optional)

### 4.2 Performance Optimizations
- **Vector database integration**: Use embeddings and vector search (e.g., Pinecone, Weaviate) for faster, more relevant message retrieval
- **Streaming responses**: Implement streaming for real-time answer generation
- **Advanced caching**: Implement Redis for distributed caching and longer cache durations
- **Database storage**: Store messages in a database for faster queries and historical tracking

### 4.3 User Experience Improvements
- **Conversation history**: Allow users to view and manage their question history
- **Question suggestions**: Auto-complete and suggest similar questions
- **Export functionality**: Allow users to export answers as PDF, CSV, or JSON
- **Multi-language support**: Support questions and answers in multiple languages
- **Voice input**: Add speech-to-text for voice questions

### 4.4 Advanced Features
- **User authentication**: Add user accounts and API key management
- **Rate limiting**: Implement rate limiting to prevent abuse
- **Analytics dashboard**: Track popular questions, usage patterns, and system performance
- **Webhook support**: Allow external systems to receive answers via webhooks
- **Batch processing**: Support multiple questions in a single request

### 4.5 Data Management
- **Message filtering**: Allow filtering by date, user, or keywords before answering
- **Data visualization**: Create charts and graphs based on message data
- **Real-time updates**: Implement WebSocket support for real-time message updates
- **Data export**: Export all messages and answers for analysis

### 4.6 Security & Reliability
- **API key rotation**: Automatic API key rotation and management
- **Request validation**: Enhanced input validation and sanitization
- **Error recovery**: Better error handling and automatic retry mechanisms
- **Monitoring & logging**: Comprehensive logging and monitoring with tools like Prometheus
- **Backup & recovery**: Automated backup of cached data and configurations

### 4.7 Integration & Extensibility
- **Plugin system**: Allow third-party plugins for custom functionality
- **API versioning**: Support multiple API versions for backward compatibility
- **GraphQL endpoint**: Add GraphQL support for flexible queries
- **SDK development**: Create SDKs for popular programming languages
- **Slack/Discord bots**: Create chatbot integrations for team communication

### 4.8 Testing & Quality
- **Unit tests**: Comprehensive test coverage for all functions
- **Integration tests**: End-to-end testing with mock APIs
- **Performance testing**: Load testing and performance benchmarking
- **A/B testing**: Test different AI models and prompts for optimal results

---

## Bonus Goals

### Bonus 1: Design Notes

During the development of this question-answering system, I considered several alternative approaches. Here are the key alternatives and why the current approach was chosen:

#### **Alternative 1: Vector Database with Embeddings (RAG - Retrieval Augmented Generation)**

**Approach:**
- Use embeddings (OpenAI embeddings or sentence transformers) to convert messages into vector representations
- Store vectors in a vector database (Pinecone, Weaviate, or Chroma)
- For each question, find the most relevant messages using similarity search
- Pass only relevant messages to the LLM for answer generation

**Pros:**
- More efficient for large datasets (only relevant context sent to LLM)
- Faster response times (no need to process all messages)
- Lower token costs (smaller context windows)
- Better scalability for millions of messages

**Cons:**
- Additional infrastructure complexity (vector database setup)
- Requires embedding model and storage
- Initial setup and indexing overhead
- May miss relevant information if embeddings aren't perfect

**Why Not Chosen:**
- The current dataset (~3,000 messages) is manageable without vector search
- Simpler architecture for the initial implementation
- No additional infrastructure dependencies
- Faster to implement and deploy

**When to Use:**
- If the message dataset grows to 10,000+ messages
- When response time becomes critical
- When token costs need optimization
- For production systems with high query volumes

---

#### **Alternative 2: Fine-Tuned Custom Model**

**Approach:**
- Fine-tune a smaller language model (like Llama 2, Mistral, or GPT-3.5) on the specific message dataset
- Train the model to understand the domain-specific context
- Deploy the fine-tuned model for question answering

**Pros:**
- Better domain-specific understanding
- Potentially lower inference costs (smaller models)
- No need to send full context with each query
- Can be optimized for specific question types

**Cons:**
- Requires training data preparation and labeling
- Training time and computational resources needed
- Model maintenance and versioning complexity
- Less flexible for new types of questions
- Higher initial development time

**Why Not Chosen:**
- No labeled training data available
- Longer development cycle
- Requires ML expertise and infrastructure
- Current approach is more flexible and adaptable

**When to Use:**
- When you have labeled training data
- For domain-specific terminology and patterns
- When query patterns are predictable
- For cost optimization at scale

---

#### **Alternative 3: Rule-Based System with NLP**

**Approach:**
- Use NLP libraries (spaCy, NLTK) to extract entities and relationships
- Create rule-based patterns for common question types
- Build a knowledge graph from messages
- Use pattern matching and templates for answers

**Pros:**
- No API costs (OpenAI)
- Predictable and explainable results
- Fast response times
- Full control over answer generation

**Cons:**
- Requires extensive rule engineering
- Brittle - breaks with new question types
- Limited understanding of context and nuance
- High maintenance overhead
- Poor handling of ambiguous questions

**Why Not Chosen:**
- Natural language questions are too varied for rules
- Would require extensive domain knowledge
- Less flexible and adaptable
- Modern LLMs provide better understanding

**When to Use:**
- For very specific, predictable question types
- When cost is a primary concern
- For domains with strict, well-defined schemas
- When explainability is critical

---

#### **Alternative 4: Hybrid Approach (Keyword Search + LLM)**

**Approach:**
- Use keyword/search-based filtering to narrow down relevant messages
- Apply TF-IDF or BM25 for message ranking
- Pass top-k relevant messages to LLM for answer generation
- Combine search results with LLM reasoning

**Pros:**
- More efficient than sending all messages
- Better precision for specific queries
- Can leverage traditional information retrieval techniques
- Good balance between accuracy and efficiency

**Cons:**
- Requires implementing search/indexing logic
- May miss semantically similar but lexically different content
- More complex than pure LLM approach
- Still needs LLM for answer generation

**Why Not Chosen:**
- Current dataset size doesn't justify the complexity
- Pure LLM approach provides better semantic understanding
- Simpler to maintain and debug
- Sufficient for the current use case

**When to Use:**
- For larger datasets (5,000+ messages)
- When specific keyword matching is important
- For systems requiring fast keyword-based filtering
- As an intermediate step before full vector search

---

#### **Alternative 5: Multi-Agent System**

**Approach:**
- Create specialized agents for different question types (travel, preferences, ownership, etc.)
- Use a router agent to classify questions and route to appropriate specialist
- Each agent processes relevant subset of messages
- Combine agent outputs for final answer

**Pros:**
- Specialized handling for different question types
- Potentially more accurate for domain-specific queries
- Modular and extensible architecture
- Can optimize each agent independently

**Cons:**
- Significant architectural complexity
- Multiple LLM calls per query (higher cost)
- Coordination and routing logic needed
- Overkill for current problem scope

**Why Not Chosen:**
- Too complex for the current requirements
- Single LLM call is sufficient and cost-effective
- Simpler architecture is easier to maintain
- Current approach handles all question types adequately

**When to Use:**
- For complex systems with distinct question categories
- When different question types need specialized processing
- For enterprise systems with multiple domains
- When accuracy for specific categories is critical

---

#### **Chosen Approach: Direct LLM with Full Context**

**Final Decision:**
I chose the **direct LLM approach with full context** because:

1. **Simplicity**: Straightforward architecture, easy to understand and maintain
2. **Flexibility**: Handles any type of natural language question without rule engineering
3. **Accuracy**: Modern LLMs (GPT-4o-mini) provide excellent understanding of context
4. **Cost-Effective**: GPT-4o-mini offers good performance at low cost
5. **Scalability**: Can easily transition to vector search if dataset grows
6. **Time-to-Market**: Fastest to implement and deploy
7. **Maintainability**: Minimal moving parts, easier debugging

**Trade-offs Accepted:**
- Sending full context to LLM (acceptable for current dataset size)
- Single API call per question (simple but could be optimized)
- No specialized routing (general-purpose solution)

**Future Migration Path:**
If the system needs to scale, the natural evolution would be:
1. Current: Full context → LLM
2. Next: Vector search → Top-k messages → LLM
3. Future: Fine-tuned model + Vector search for optimal performance

---

