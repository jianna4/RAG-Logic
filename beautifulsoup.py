"""
ow lets do abit of web scraping with BeautifulSoup
for webcrapping for RAG, you might wnt to use webbasedloader for static files that are well structued,but for dynamic
websites, you might want to use BeautifulSoup to parse the HTML and extract the data you need acccording to your needs manually
lets look atht e basic concepts first:
we need to first install it by using > pip install beautifulsoup4 requests lxml
we will use xml parser to parse the HTML content
then we continue to our cde with:
"""

import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
def fetch_and_clean(url):
    r= requests.get(url)
    r.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(r.content, 'lxml')  # Parse the HTML content with lxml parser
    for tag in soup(['script', 'style']):
        tag.decompose()  # Remove script and style tags
    text="\n\n".join(el.get_text(strip=True) for el in soup.find_all(['h1', 'h2', 'h3', 'p']))# Extract text from headers and paragraphs
    return Document(page_content=text, metadata={"source": url})

"""
you might have noticed that we needed to dothe request first to get the html content and we also had to manually return the Document object
this is because BeautifulSoup does not have a built-in loader like the langchain loaders, so we need to do it manually
we can inegrate langchain webbasedloader to do this for us.
So now lets cmbine beautifulsoup with langchain"""
from langchain_community.document_loaders import WebBaseLoader


loader = WebBaseLoader("https://en.wikipedia.org/wiki/Web_scraping")  # Use WebBaseLoader to load the webpage
docs = loader.load()
# docs is a list of Document objects
print(f"Number of docs: {len(docs)}")
  # 2️⃣ Extract HTML from the first Document
html_content = docs[0].page_content
3# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'lxml')
for tag in soup(['script', 'style']):
 tag.decompose()
text = "\n\n".join(el.get_text(strip=True) for el in soup.find_all(['h1', 'h2', 'h3', 'p']))  # Extract text from headers and paragraphs
    
print(text[:500])  # Print the first 500 characters of the cleaned text

