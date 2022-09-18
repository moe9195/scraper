from bs4 import BeautifulSoup
import requests
import boto3
from botocore.exceptions import ClientError

SENDER = "Moe Rahmeh <moerahmeh95@hotmail.com>"
RECIPIENT = "moerahmeh95@hotmail.com"

AWS_REGION = "eu-central-1"

SUBJECT = "Amazon SES Test (SDK for Python)"
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )

BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """ 
        
        # The character encoding for the email.
CHARSET = "UTF-8"


def get_products(gender: str, tags: list):
    if not gender in ['mens', 'womens']:
        raise ValueError('Gender must be either "mens" or "womens"')

    discounts = []
    url = f'https://www.patagonia.com/shop/web-specials-{gender}-jackets-vests?page=1000'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    products = soup.find_all('div', class_='product-tile__meta-primary')
    for product in products:
        link = product.find('a', class_='link')
        if link:
            name = link.find(class_='product-tile__name').text
            if any(tag in name.lower() for tag in tags):
                discounts.append({"name": name, "link": 'https://www.patagonia.com' + link['href']})

    return discounts


    

if __name__ == '__main__':
    gender = 'mens'
    tags = ['frozen', 'glacier', 'parka', 'down']
    discounts = get_products(gender, tags)

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,

        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



