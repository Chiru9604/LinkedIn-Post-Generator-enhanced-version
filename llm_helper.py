from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os


load_dotenv()

# Simple initialization without optional parameters that might cause conflicts
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv('GROQ_API_KEY')
)


if __name__ == '__main__':
    response = llm.invoke('What are the main ingredients in biriyani')
    print(response.content)
