import json
import unicodedata
import requests
from bs4 import BeautifulSoup, Tag
import csv
import headers

# Get the data from the csv file i.e the links
def read_csv():
    rows = []
    the_links = []
    with open("Amazon Scraping - Sheet1.csv", "r", newline="") as file1:
        content = csv.reader(file1)
        next(content)
        for i in content:
            rows.append(i)
    for i in rows:
        link_format = "https://www.amazon.{country}/dp/{asin}"
        the_links.append(link_format.format(country=i[3], asin=i[2]))
    return the_links

# The price from the string
def get_pr(text):
    valid_character = "1234567890,."
    price = ""
    for i in text:
        if str(i) in valid_character:
            price = price+i
    return price

# removing control characters from string
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

# getting details from link of product
def get_product_details(product_link, header):
    response = requests.get(product_link, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")

    # To check IF NO DATA FOUND page shown
    status = response.status_code
    if status == 404:
        print("Stats: Not Found")
        return "Not found"
    #To check if server error
    elif status>=500 and status<=600:
      print("Stats: Server Error")
      return "Server Error"
    # To check if captcha verification found
    elif soup.find("form", {"action": "/errors/validateCaptcha"}):
        print("Stats: Captcha")
        return "Captcha"

# To fetch all product details
    else:

        # Getting product_title
        product_title = soup.find("span", {"id": "productTitle"})
        product_title = product_title.text
        product_title = remove_control_characters(
            product_title).replace("\n", "").strip()

        # Getting product image by '#imgBlkFront'
        # checking if id changed and using alternate id
        product_image = soup.find("img", {"id": "imgBlkFront"})
        if not product_image:
            product_image = soup.find(
                "div", {"id": "imgTagWrapperId"}).select_one("img")["src"]
        else:
            product_image = product_image["src"]

        # - fetching product price by '#tmmSwatches'
        # - checking if id changed and using alternate id
        # - removing extra characters from price string
        product_price = soup.find(
            "div", {"id": "tmmSwatches"})
        if not product_price:
            product_price = soup.find("div", {
                "id": "corePriceDisplay_desktop_feature_div"}).select_one("span.a-offscreen")
        else:
            product_price = product_price.select_one(
                "a.a-button-text span.a-color-base")

        product_price = get_pr(product_price.text)

        # - fetching product detail;s by '#detailBullets_feature_div'
        # - checking if id changed and using alternate id
        # - removing extra and invalid characters from product details string
        # - addind details in the form of dictionary {detail_heading : detail_text}
        all_product_details = soup.find(
            "div", {"id": "detailBullets_feature_div"})
        if not all_product_details:
            product_detail_row = soup.find("div", {"id": "prodDetails"}).select(
                "table#productDetails_techSpec_section_1 tr")
            product_details = []
            for detail in product_detail_row:
                heading = detail.select_one("th").text

                # removing special control character
                heading = remove_control_characters(
                    heading).replace("\n", "").strip()
                details = detail.select_one("td").text
                details = remove_control_characters(
                    details).replace("\n", "").strip()
                product_details.append({heading: details})
        else:
            all_product_details = all_product_details.select_one("ul")
            product_details = []
            for product_detail_items in all_product_details:
                if isinstance(product_detail_items, Tag):
                    title = product_detail_items.select_one(
                        "span.a-text-bold").text

                    # removing special control character
                    clean_title = remove_control_characters(
                        title).replace(":", "").strip()

                    detail = product_detail_items.find(
                        'span').find_next('span').find_next('span').text

                    clean_detail = remove_control_characters(
                        detail).replace(":", "").strip()
                    dic = {clean_title: clean_detail}
                    product_details.append(dic)

        product = {
            "product_title": product_title,
            "product_image": product_image,
            "product_price": product_price,
            "product_details": product_details
        }

        print("Status: Success")

        return product

# getting a list of all product details and bypass captcha by changing user agents for all link
def get_all_products_detail():
    products_list = []
    links = read_csv()
    for idx, link in enumerate(links):
        current_header = headers.user_agents[idx % 5]
        print("Started #", idx, ": ", link)
        products_list.append(get_product_details(link, current_header))
    return products_list

# export data to JSON file
def export_to_json(json_data):
    json_object = json.dumps(json_data)
    with open("details_of_product.json", "w") as outfile:
        outfile.write(json_object)

all_products_details = get_all_products_detail()
all_products_details