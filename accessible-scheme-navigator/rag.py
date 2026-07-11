import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()

PROMPT_TEMPLATE = """
You are an assistant helping persons with disabilities in Kerala, India find government schemes they qualify for.

The user has told you:
- Disability type: {disability}
- Age: {age}
- District: {district}

Using only the information in the provided context, list all government schemes this person qualifies for or may qualify for.

For each scheme, respond in this EXACT format:

SCHEME: [scheme name in English and Malayalam]
WHAT YOU GET: [plain simple English, 1-2 sentences]
MALAYALAM: [same as above but in simple conversational Malayalam]
DO YOU QUALIFY: [yes/likely/check - with brief reason]
DOCUMENTS NEEDED: [numbered list]
NEXT STEP: [one sentence - which office, what to ask for]
---

If no schemes are found for this profile, say so clearly.
Do not invent schemes not present in the context.
Keep language simple. Avoid legal jargon.

Context:
{context}

Question: {question}
"""

def get_schemes(disability: str, age: str, district: str) -> str:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )

    query = f"Government schemes for person with {disability}, age {age}, living in {district} Kerala"

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE.replace("{disability}", disability)
                                .replace("{age}", age)
                                .replace("{district}", district)
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    result = chain.invoke({"query": query})
    return result["result"]