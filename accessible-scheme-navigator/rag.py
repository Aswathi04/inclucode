import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
DO YOU QUALIFY: [Start with yes/likely/check. Then one sentence explaining exactly why — which specific criterion confirms it and which criterion still needs verification. Example: "Likely — your age qualifies. Bring your disability certificate to confirm the income threshold at the office."]DOCUMENTS NEEDED: [numbered list]
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
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )

    query = f"Government schemes for person with {disability}, age {age}, living in {district} Kerala"
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    docs = retriever.invoke(query)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE.replace("{disability}", disability)
                                .replace("{age}", age)
                                .replace("{district}", district)
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": query})

if __name__ == "__main__":
    print(get_schemes("locomotor disability", "22", "Kottayam"))