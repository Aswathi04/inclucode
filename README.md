Here is a comprehensive README structure for Vazhikatti tailored for your GitHub repository. You can copy and paste this directly into your `README.md` file.

---

# VAZHIKATTI 🧭

**Code Inclusive. Build Accessible. Empower Independence.**

Vazhikatti is an accessible, bilingual web platform designed to help youth with locomotive disabilities in Kerala easily discover, navigate, and access government welfare schemes and scholarships. Built for the **INCLUCODE 2026 Buildathon**, this project bridges the information gap through multi-modal inputs and accessible design.

## 🎯 The Problem

Youth with locomotive disabilities often face significant digital and informational barriers when attempting to find welfare schemes. Searching through fragmented sources manually leads to confusion over eligibility, documentation requirements, and the complex process of obtaining a disability certificate.

## 💡 Our Solution

The platform provides fully voice-accessible scheme details, eligibility estimates, downloadable document checklists, and guidance on obtaining a disability certificate. By prioritizing accessibility by design, Vazhikatti empowers users to independently manage their applications.

## ✨ Key Features

* **Multi-Modal Input:** Users can enter their disability, age, and district using either text or voice commands.
* **Bilingual Support:** Full text support in both Malayalam and English to ensure local relevance in Kerala.
* **Universal Voice Output:** Integrated voice output across all pages to assist visually or physically impaired users in navigating content.
* **Smart Scheme Matching:** Instantly displays available schemes and calculates the user's likelihood of eligibility based on their input profile.
* **Actionable Resources:**
* Generates a downloadable PDF checklist of required documents for each scheme.
* Provides a dedicated guide on the step-by-step process to procure a disability certificate.



## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **AI / Logic:** LangChain, Google Generative AI (Gemini) for embedding and RAG (Retrieval-Augmented Generation) processes.
* **Frontend:** HTML, CSS, Vanilla JavaScript (`voice.js` for speech-to-text and text-to-speech integration)
* **Data:** JSON-based scheme datasets and local document ingestion (`ingest.py`, `rag.py`)

## 🚀 Local Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/vazhikatti.git
cd vazhikatti

```


2. **Set up a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Environment Variables:**
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY="your_api_key_here"

```


5. **Run the Application:**
```bash
python app.py

```


The application will be accessible at `[http://127.0.0.1:5000](http://127.0.0.1:5000)`.

## 👩‍💻 Meet the Team

This project was developed by a team passionate about leveraging technology for social good and community building:

* **Anosha Roy** - Frontend Development & UI/UX
* **Aswathi Thummarukudy** - Backend Development & AI Integration

## 🏆 Acknowledgments

Created with ❤️ for **INCLUCODE 2026: Inclusive Software Innovation Buildathon**.
