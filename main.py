import os
import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

product_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "x-https": "on",
    "sec-ch-ua-platform": "Windows",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 "
                  "Safari/537.36"
}

response = requests.get(product_url, headers=HEADERS)
web_data = response.content

soup = BeautifulSoup(web_data, "lxml")

TITLE = soup.title.text
price_text = soup.find(class_="a-offscreen").get_text()
price_as_float = float(price_text.split("$")[1])
MESSAGE = f"{TITLE} is now {price_as_float}"

BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="riza.mansuri11@gmail.com",
                msg=f"Subject: Amazon Price ALert!\n\n {str(MESSAGE)}".encode("utf-8")
            )

        print('Email sent successfully')

    except Exception as e:
        print(f'Error occurred: {str(e)}')
