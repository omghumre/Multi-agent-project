from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

def test_gemini():
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize Gemini
        llm = GoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        # Test generation
        response = llm.invoke("Hello! Can you help me with a simple task?")
        print("Test response:", response)
        print("\nGemini LLM is working correctly!")
        return True
    except Exception as e:
        print(f"Error testing Gemini: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini()