# ai_sug.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

def get_code_suggestions(code: str, api_key: str) -> str:
    """
    Analyze Java code and provide suggestions based on:
    1. Code readability and maintainability
    2. Use of modern Java features
    3. Performance optimization
    4. Design patterns and SOLID principles
    """
    
    system_prompt = """
    As an expert Java developer, analyze the following code and provide specific suggestions 
    for improvement based on Java best practices. Focus on:
    1. Code readability and maintainability
    2. Use of modern Java features
    3. Performance optimization
    4. Design patterns and SOLID principles
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Code:\n{code_snippet}")  # Use correct placeholder
    ])
    
    llm = ChatGroq(api_key=api_key, model="mixtral-8x7b-32768")  # Correct initialization
    
    try:
        str_parser = StrOutputParser()
        chain = prompt | llm | str_parser
        result = chain.invoke({"code_snippet": code})  # Use correct key
        return result
    except Exception as e:
        return f"AI Review failed: {str(e)}"
