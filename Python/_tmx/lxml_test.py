from lxml import etree

# XML рядок, який ми будемо парсити
xml_string = """
<bookstore>
  <book>
    <title lang="en">Harry Potter</title>
    <author>J.K. Rowling</author>
  </book>
  <book>
    <title lang="en">The Hobbit</title>
    <author>J.R.R. Tolkien</author>
  </book>
</bookstore>
"""

# Парсимо XML рядок
root = etree.fromstring(xml_string)

# Отримуємо всі елементи 'book' у дереві
books = root.findall('book')

# Виводимо інформацію про книги
for book in books:
    title = book.find('title').text
    author = book.find('author').text
    print(f"Title: {title}, Author: {author}")

titles = root.xpath("//title[@lang='en']/text()")
print("English Titles:", titles)
