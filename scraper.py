import requests
import lxml.html as html
import os
import datetime

books = [
    "libro-python-data-science-handbook-essential-tools-for-working-with-data-libro-en-ingles/9781491912058/p/48477050",
    "libro-practical-statistics-for-data-scientists-50-essential-concepts-using-r-and-python-libro-en-ingles/9781492072942/p/52304858",
    "libro-star-wars-datos-fascinantes/9788411121910/p/54051514"
]

BOOK_URL = 'https://www.buscalibre.cl/'
XPATH_TITLE = '//h1/text()'
XPATH_PRICE = '//p[@class="precioAhora margin-0 font-weight-strong"]/span/text()'

def parse_book(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            blogpost = response.content.decode('utf-8')
            parsed = html.fromstring(blogpost)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                price = parsed.xpath(XPATH_PRICE)
            except IndexError:
                return
            if not os.path.isfile(f'resultados/{title}.txt'):
                with open(f'resultados/{title}.txt', 'w', encoding = 'utf-8') as f:
                    f.write(title)
                    f.write('\n')
                    f.write(f"{today} => {price[0]}")
                    f.write('\n')
            else:
                with open(f'resultados/{title}.txt', 'a', encoding = 'utf-8') as f:
                    f.write(f"{today} => {price[0]}")
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_books():
    try:
        response = requests.get(BOOK_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir("resultados"):
                os.mkdir("resultados")
            for book in books:
                link = BOOK_URL + book
                parse_book(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_books()

if __name__ == '__main__':
    run()