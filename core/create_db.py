from utilities import web_scrape
from utilities import db_store
from dotenv import load_dotenv


load_dotenv()

page_url = "https://sujancontitech.com/"

############ Scrape web page and store it in text file ###############

file_name = 'web_scrape.txt'
text = web_scrape.scrape_page(page_url)
web_scrape.write_to_file(file_name, text)



############### Read text file and extract information ###############

file_name = 'web_scrape.txt'
text = web_scrape.read_from_file(file_name)
text = web_scrape.extract_information(text)
file_name = "summarized_text.txt"
web_scrape.write_to_file(file_name, text)


############### Tokenize the text ####################
file_name = "summarized_text.txt"
text = web_scrape.read_from_file(file_name)
chunks = web_scrape.tokenize_text(text)

for i, chunk in enumerate(chunks):
    print(f"\nChunk No {i+1}")
    print(chunk)


############ Store the data in db ####################

vector_store = db_store.get_vector_store()
db_store.store_in_db(chunks)


##############  Get all from database ##################

db = db_store.get_vector_store()
docs = db.get()

for i,doc in enumerate(docs['documents']):
    print(f"\n\nDoc no {i+1} : \n",doc)

