import re
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter


def scrape_page(page_url):
    # Load web page
    loader = WebBaseLoader(page_url)

    docs = loader.load()

    # Clean text
    # Replace multiple newlines with a single newline
    cleaned_text = re.sub(r'\n+', '\n', docs[0].page_content)
    # print(cleaned_text)

    return cleaned_text


def write_to_file(filename,text):
    # Ensure that the folder exists
    folder_name = "temp_docs"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    filepath = os.path.join(folder_name,filename)

    with open(filepath,'w') as file:
        file.write(text)


def read_from_file(filename):
    folder_name = "temp_docs"
    filepath = os.path.join(folder_name, filename)

    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found"


def extract_information(text):
    # Summarize using LLM
    system_prompt_original = """
        Remove unimportant information from the following text. Restructure the text by separating information of the same context into distinct paragraphs.
        Do not omit any key details, and do not add any additional words or explanations. Maintain the original content and context as it is.
        Do not add any formatting characters such as asterisk and double asterisk.
        Do not add 'Read more'
        
        
        ~~~~~~~~~~~~~
        {text}
        ~~~~~~~~~~~~~
    
    """

    system_prompt = """
            Extract information from the given text. Separate the information based on relevance into paragraphs.
            Keep all the related information in one paragraph. 

            ~~~~~~~~~~~~~
            {text}
            ~~~~~~~~~~~~~

        """

    prompt = ChatPromptTemplate.from_template(system_prompt)

    llm = GoogleGenerativeAI(model="gemini-1.5-flash-8b")
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"text":text})

    # Clean summarized text
    cleaned_text_2  = re.sub(r'\n\n(?!\n)', '\n', response)
    # print(cleaned_text_2)

    return cleaned_text_2


def tokenize_text(text):
    # Tokenize
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=0, chunk_overlap=0)
    chunks = text_splitter.split_text(text)

    # for i, chunk in enumerate(chunks):
    #     print("\nChunk No: ",i+1)
    #     print(chunk)

    return chunks
