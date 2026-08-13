# 🛡️ Guardian Reviewer : Multi-Agent Local AI Auditor

**Guardian Reviewer** is a sophisticated, local-first code analysis platform that orchestrates **7 specialized AI agents** to provide deep technical audits, security scans, and pedagogical mentoring. 

Most AI tools provide a single stream of text; this project simulates a professional **Senior Developer Peer Review** by using multiple personas to evaluate your code from different specialized perspectives.
This project was built as a learning-focused system to understand how professional code reviews work in real engineering teams.

---

## ✨ Key Features

### 🤖 The 6-Agent Review Squad
Each agent operates with its own specific logic and persona:

| Agent Name              | Role / Responsibility |
|------------------------|----------------------|
| **Context Investigator** | Analyzes the high-level intent and structure of your script |
| **Bug Hunter**           | Performs deep-dive scans for logic flaws and security vulnerabilities |
| **Style Specialist**     | Ensures code follows language-specific conventions and clean-coding standards |
| **Best Practice Architect** | Compares implementation against industry standards like DRY and SOLID |
| **Friendly Mentor**      | Provides supportive feedback, encouragement, and a "Lesson of the Day" |
| **Scoring Auditor**      | Reviews all agent findings and assigns an objective quality score (0–100) |

### 🛠️ Master Architect Optimization
Beyond just finding issues, the **Master Architect agent** synthesizes all feedback to generate a fully optimized, production-ready version of your code. You can compare the "Original" and "Improved" versions side-by-side.

### 🌐 Wide Language Support
Built-in specialized prompts for over 15+ languages, including:
- Web: HTML, CSS, JavaScript, TypeScript, PHP
- Systems/Apps: Python, Java, C, C++, C#, Go, Rust, Swift, Kotlin, Ruby
- Data: SQL, R

---

## 📺 Demo

Check out the **Guardian Reviewer** in action:

<div align="center">
  <video src=https://github.com/user-attachments/assets/32041ff8-e5a4-4258-b197-7f8e4b418780 width="100%" controls>
    Your browser does not support the video tag.
  </video>
</div>

### 📸 What's happening in the Demo?
1. **Source Input:** We paste a Php script with a deliberate security flaw and poor variable naming.
2. **Parallel Analysis:** The 6 agents (Context, Bug, Style, etc.) trigger simultaneously, creating a comprehensive report.
3. **The Score:** The Scoring Auditor gives a metric based on the severity of the findings.
4. **The Fix:** We click the **Master Architect** button to receive a refactored, secure version of the code.

--- 

## ⚙️ Model Information & Performance

This project is built to be **Privacy-First** and **Hardware-Accessible**.

> [!NOTE]
> **Why Qwen 0.5B?**
> To ensure compatibility with standard laptops, this project defaults to **Qwen 2.5 Coder (0.5B)**. This allows the system to run locally and efficiently without a high-end GPU.

**Scaling for Accuracy:** While the 0.5B model is excellent for structure, its logical depth is limited. The system is entirely **model-agnostic**. You can swap to **Llama 3 (8B)** or **Mistral** by simply updating your `.env` file to see a massive jump in report accuracy with no major changes to the core code.

---

## Performance Evaluation

Tested across 3 code samples (bug-free, single real bug, multiple real bugs) 
on local Ollama models via CPU inference.

### Accuracy
| Model | Correct Diagnoses | Notes |
|---|---|---|
| qwen2.5-coder:0.5b | 0/3 | Hallucinated bugs not present in code; misdescribed actual logic |
| qwen2.5-coder:7b | 3/3 | Correctly identified real edge cases and missing error handling |

### Latency (avg across samples, 4 parallel agents)
| Model | Sequential | Parallel | Change |
|---|---|---|---|
| qwen2.5-coder:0.5b | 7.47s | 8.19s | -9.6% (parallel overhead > inference time) |
| qwen2.5-coder:7b | 32.14s | 29.33s | +8.7% |

**Takeaway:** Model size matters more than concurrency for output quality. 
0.5B is viable only where speed and full offline capability outweigh 
accuracy; 7B is recommended when correctness matters, and benefits 
measurably from parallelized agent execution.

## 🚀 Installation & Setup

### 1. Prerequisites
* **Python 3.10+**
* **Ollama:** Download and install from [ollama.com](https://ollama.com)

### 2. Prepare the AI
Open your terminal and pull the default model:
```bash
ollama pull qwen2.5-coder:0.5b
```

### 3. Clone and Install

#### 1. Clone the repository

```bash
git clone https://github.com/Dahlia0701/code_review_agent.git
cd code_review_agent
```

#### 2. Install Required Python Libraries

```bash
pip install -r requirements.txt
```


### 4. Configuration
Create a .env file in the root directory:
```bash
MODEL_NAME=qwen2.5-coder:0.5b

OLLAMA_BASE_URL=http://localhost:11434
```

### 5. Launch the App
```bash
python -m streamlit run core/app.py
```
---

## ⚙️ Advanced Configuration (Optional)
If you are running the AI on a different machine (like a dedicated home server or a Docker container), you can update the .env file:
- **MODEL_NAME**: The specific LLM you want to use (e.g., llama3, mistral).
- **OLLAMA_BASE_URL**: Only change this if your Ollama instance is not on your local laptop (e.g., http://192.168.1.50:11434).
---

## 📂 Project Structure

```text
GUARDIAN_REVIEWER/               
├── .env                  # Hidden configuration (Model name, base url)
├── .gitignore            # Version control rules (Prevents leaking .env to GitHub)
├── core/
|   ├── app.py            # Streamlit UI & orchestration logic
│   └── api_client.py     # Ollama API connection
├── agents/               # Specialized Prompt Definitions
│   ├── context_agent.py
│   ├── bug_agent.py
│   ├── style_agent.py
│   ├── best_practice.py
│   ├── mentor.py
│   ├── scoring_agent.py
│   └── refining_agent.py # Master Architect rewrite logic
└── requirements.txt      # Dependencies (Streamlit, python-dotenv, requests)
```
---

## 💡 How to Use

1. Paste your code into the text area.
2. Select the language from the sidebar (e.g., Python, C#, Ruby, SQL).
3. Click "Run Full Analysis" to see all 6 agents work in real-time.
4. Review your Code Quality Score and the Mentor's Lesson.
5. Click "Generate Improved Code" to get the Master Architect's optimized rewrite.
---

## 🤝 Contributing

Contributions are welcome! If you want to add a new agent (e.g., a "Documentation Agent" or a "Test-Case Generator"), feel free to fork the repo and submit a PR.

---




