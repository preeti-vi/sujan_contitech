from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

system_prompt_original = """
    You are an expert assistant at Sujan Contitech.
    Answer the user query based on the given information below, 
    
    First check, If the query is about the company, 
    
    If the query is not about the company, inform the user that you would help users with queries related to the company.  
    
    If the query is about the company but the given information is not related to the user query, 
    apologise user for not having information about it currently. 
    

    ~~~
    Information: {information}
    ~~~

    ```
    Query: {user_query}
    ```
"""

system_prompt = """
    You are an expert assistant at Sujan Contitech. You help users with queries related to the company. Here's how you should respond:

    1. If the query is about the company: Answer based on the provided company information, including location, 
    services, contact details, etc.
    
    2. If the query is not about the company: Inform the user politely that you can only assist with questions 
    related to the company.
    
    3. If the query is about the company, but the given information does not cover it: 
    Apologize and inform the user that the company doesn't have that information currently.
    
    
    ~~~
    Information: 
    {information}
    ~~~

    ```
    Query: 
    {user_query}
    ```
"""

def get_response(db_response, user_query):
    prompt_template = ChatPromptTemplate([
        ("system", system_prompt),
        # MessagesPlaceholder("msgs")
    ])

    information = ""
    for doc in db_response:
        information += doc.page_content + "\n\n"

    llm = ChatOpenAI(model="gpt-3.5-turbo")
    chain = prompt_template| llm | StrOutputParser()
    response = chain.invoke({'information': information, 'user_query':user_query})

    return response



    # prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})