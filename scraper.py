import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os

URL = 'https://www.amazon.com/gp/product/B07JZK5R5W?pf_rd_p=2d1ab404-3b11-4c97-b3db-48081e145e35&pf_rd_r=QWCCXWZHXHYYK8F7ZY6C'

headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

page = requests.get(URL, headers=headers)


def check_price():
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="productTitle").get_text()             
    price = soup2.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:4]) # latest price / remove decimal and currency sign
    srp = 209 # suggested retail price / original price

    if(converted_price < srp):
        send_mail() # notify me when my product's price fell down    

        print('Product: ' + title.strip())
        print('Price: ' + price)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    sender = os.environ.get('EMAIL_USER') # sender's email address to be used
    password = os.environ.get('EMAIL_PASS') # email password

    server.login(sender, password)

    recepient = 'gabrielrebadulla@gmail.com' # your email

    subject = 'Price fell down!'
    body = 'Get your discounted helmet now! Check out on Amazon \n' + URL

    msg = f"Subject: {subject}\n\n{body}"


    server.sendmail(
        sender,
        recepient,
        msg
    )
    print('EMAIL HAS BEEN SENT')

    server.quit()

while(True):
    check_price()
    time.sleep(86400) # check once a day (arg is on seconds basis)
