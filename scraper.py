import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://ideaufro.com/blog/'
XPATH_LINK_TO_BLOGPOSTS = '//h2[@class="entry-title"]/a/@href'
XPATH_TITLE = '//h1[@class="entry-title"]/text()'
XPATH_BODY = '//div[@class="entry-content clear"]/p[not(@class)]/text()'

def parse_blogpost(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            blogpost = response.content.decode('utf-8')
            parsed = html.fromstring(blogpost)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            with open(f'{today}/{title}.txt', 'w', encoding = 'utf-8') as f:
                f.write(title)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_blogposts = parsed.xpath(XPATH_LINK_TO_BLOGPOSTS)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_blogposts:
                parse_blogpost(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()