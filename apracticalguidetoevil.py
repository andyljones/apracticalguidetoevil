import requests
import re
from bs4 import BeautifulSoup

class Chapter:
    def __init__(self, title, text):
        self.title = title
        self.text = text

def download_chapter(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")

    content = ""

    title_node = soup.find("h1", { "class": "entry-title" })
    title = title_node.text

    entry_content = soup.find("div", { "class" : "entry-content" })
    for child in entry_content.findChildren():
        if child.name != "p": continue

        content += child.text + "\n\n"

    return Chapter(title, content)
    

def download_contents(book="all"):
    TABLE_OF_CONTENTS_URL = "https://practicalguidetoevil.wordpress.com/table-of-contents/"
    LINK_REGEX = "\<li\><a href=\"(https://practicalguidetoevil.wordpress.com/[0-9]+/[0-9]+/[0-9]+/.*/)\"\>(.*)\</a\>\</li\>"
    response = requests.get(TABLE_OF_CONTENTS_URL)
    response_text = response.text

    matches = re.findall(LINK_REGEX, response_text)

    for match in matches:
        # Hacky system for determining the book we want        
        if book != "all" and "prologue" in match[0]:
            book -= 1

        if book != 0 and book != "all": continue

        yield match[0]

def to_ascii(text):
    return ''.join(i for i in text if ord(i) < 128)

def write_book(book="all", output_file="A Practical Guide to Evil.md"):
    with open(output_file, "w") as f:
        book_name = "all books" if book == "all" else f"book {book}"
        f.write(f"% A Practical Guide to Evil ({book_name})\n")
        f.write("% erraticerrata\n\n")

        for link in list(download_contents(book)):
            chapter = download_chapter(link)

            f.write(f"# {to_ascii(chapter.title)}\n\n")
            f.write(to_ascii(chapter.text))
            
            print(f"Done {chapter.title}")

write_book()