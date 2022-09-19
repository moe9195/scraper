from mailer import send_mail
from datetime import datetime
from scraper import get_products

SUBJECT = f'Patagonia Discounts {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

if __name__ == '__main__':
    gender = 'mens'
    tags = ['frozen', 'glacier', 'parka', 'down']
    discounts = get_products(gender, tags)

    body_html = ''
    body_text = ''
    for discount in discounts:
        body_text += f"{discount['name']} - {discount['price']}\n{discount['link']}\n\n"
        body_html += f'<a href="{discount["link"]}">{discount["name"]}</a><br><br><img src="{discount["img"]}"><br><br>{discount["price"]}<br><br><hr><br><br>'
    
    send_mail(SUBJECT, body_text, body_html)


 

