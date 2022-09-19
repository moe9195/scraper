import requests
from bs4 import BeautifulSoup

def get_products(gender: str, tags: list):
    if not gender in ['mens', 'womens']:
        raise ValueError('Gender must be either "mens" or "womens"')

    discounts = []
    url = f'https://www.patagonia.com/shop/web-specials-{gender}-jackets-vests?page=1000'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    products = soup.find_all('div', class_='product')
    for product in products:
        link = product.find('a', class_='link')
        img = product.find('product-tile-image')
        price = product.find('span', class_='product-tile__price')
        if link and img:
            name = link.find(class_='product-tile__name').text
            if any(tag in name.lower() for tag in tags):
                discounts.append({"name": name, "link": 'https://www.patagonia.com' + link['href'], "img": img['base'], "price": price.text})

    return discounts