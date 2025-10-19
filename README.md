# 📊 Data Insights Generator 

This is a full-stack web application developed for the **Multimeta.ai Technical Hiring Assessment (Role 1)**.

It allows users to upload numerical datasets (CSV or Excel), performs statistical analysis, generates visualizations, and uses a **Generative AI model** (via **Groq/Llama 3**) to produce a textual summary of key trends and anomalies.

The final deliverable is a fully deployed and functional data insights platform.

---

## 💻 Tech Stack & Dependencies

| Component           | Technology                | Role                                                     |
| ------------------- | ------------------------- | -------------------------------------------------------- |
| **Backend**         | Python 3.10+, FastAPI     | REST API for file handling and processing                |
| **Data Processing** | Pandas, NumPy, Matplotlib | Numerical analysis and chart generation                  |
| **Generative AI**   | Groq SDK (LLaMA 3)        | Generate textual insights from statistical data          |
| **Frontend**        | React.js (Vite), Axios    | Interactive interface for file upload and result display |
| **Deployment**      | Heroku / Railway / Vercel | Host backend and frontend                                |
| **Version Control** | Git, GitHub               | Source code management and collaboration                 |

---

## ⚙️ Setup and Installation

### 🔧 1. Backend Setup (FastAPI)

#### Clone the repository

```bash
git clone https://github.com/kkv-dinesh/Data_Insights_generator_backend
cd multimeta-data-insights
```

#### Create and activate a virtual environment

```bash
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Set up environment variables

Create a `.env` file in the project root with your **Groq API Key**:

```env
# .env
GEMINI_API_KEY="YOUR_GROQ_API_KEY_HERE"
```

#### Run the backend server

```bash
uvicorn main:app --reload
```

> The API will now be available at:
> 🔗 [http://localhost:8000](http://localhost:8000)

---


## 🧠 Features

* Upload `.csv` or `.xlsx` files
* Compute statistical summaries (mean, median, std, etc.)
* Generate visual charts from datasets
* Get AI-generated insights from **Groq's LLaMA 3 model**
* Easy-to-use frontend interface


