# TestGenAI – Complete Test Case Generator (Froth Test Ops)

🚀 An AI-powered **Test Case Generator** that transforms plain-English requirements into structured test cases.  
It combines **OpenAI LLMs**, **vector similarity search (ChromaDB + Sentence Transformers)**, **caching**, and **audit logging** to deliver cost-efficient, reusable, and high-quality test artifacts.

---

## ✨ Features
- **OpenAI Integration** – Generate comprehensive test cases with GPT models
- **Smart Token Management** – Tracks usage, cost, and applies daily/monthly quotas
- **Caching** – Prevents duplicate costs for repeated requirements
- **Vector Similarity** – Finds and reuses similar requirements via embeddings
- **Local Fallback** – Adapts existing cases if close matches exist
- **Audit Logging** – JSONL logs for every request with metadata
- **User Quotas** – Enforces limits and usage tracking per user

---

Requirements
	•	Python 3.9+ (tested on 3.10/3.11)
	•	Disk access for ./data (cache, quotas, logs, vector DB)
	•	OpenAI API key (for generation mode)
 
``````



#Clone repo
git clone https://github.com/pritishpattanaik/test-ops-poc

cd testgenai

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install openai tiktoken sentence-transformers chromadb pandas numpy python-dotenv




#Configuration

Create a .env file in the project root:
OPENAI_API_KEY=sk-your-api-key

```
#Run the example script:
python3 rd_froth_testops.py

# check the cache status

# Run again and see the cache status whether its beign served from local or not ? 

``````

📂 Data & Logs
	•	Cache: ./data/cache.json
	•	Quotas: ./data/quotas.json
	•	Audit Logs: ./data/audit_logs.jsonl
	•	Vector DB: ./data/chroma_db/


 📊 Quotas & Costs
	•	Daily Limit: 10,000 tokens per user
	•	Monthly Limit: 300,000 tokens per user
	•	Pricing Reference:
	•	gpt-3.5-turbo: $0.001 / 1K input, $0.002 / 1K output
	•	gpt-4: $0.03 / 1K input, $0.06 / 1K output

❓ FAQ

Q: Can it run without OpenAI?
Yes. It will still serve results via cache and vector similarity if similar requirements exist.

Q: Where are test cases stored?
Each request is logged and cached locally; vector DB enables reusability.

Q: Can I add other LLM providers?
Yes, extend _call_openai_api() or add new providers with a similar interface.


🛣️ Roadmap
	•	🔗 Support for Gemini & Anthropic Claude
	•	🖥️ REST API wrapper with FastAPI
	•	📊 Web dashboard for usage & quota monitoring
	•	🧪 Export test cases to CSV/Excel/JIRA

 📜 License

