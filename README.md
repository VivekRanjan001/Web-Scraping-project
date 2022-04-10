# Web Scraping - Credicxo
Scraping www.amazon.com for product information like name, price, image and details

## How it works?
- Read csv of product ASIN code, country code and generate amazon web links.
- For each link do -
  - To prevent amazon from blocking our request
    - Select next header (user_agent and referer) from a predefined list of headers from `headers.py`
  - Fetch page html using requests module and parse it using BeautifulSoup
  - Check if page not found using status_code
  - Check if captcha has occurred
  - Else,
    - Get product details using id and/or class selectors
    - If element is not present try another id and/or class selectors
    - Clean all data and remove invalid characters
    - Generate a dictionary having:
      - Product Title
      - Product Image Link
      - Product Price
      - Product Details
- Generate list of product details
- Export product details to JSON file `detail_of_products.json`
- Insert product details to MySQL database. 
  - Dump database to `dump-Credicxo.sql`

## How to run?
- Activate virtual environment `source venv/bin/activate.[__YOUR_SHELL_EXTENSION__]`
  - Ex. `source venv/bin/activate.fish`
- `pip install -r requirements.txt`
- Open [Jupyter Notebook](https://github.com/sagarsangwan/web-scraping-Credicxo/blob/main/main.ipynb)

or

- Open [Google Colab Notebook](https://colab.research.google.com/drive/18YtUbh9oqM98Wfm1dGnScxWG7X3C_1MX?usp=sharing)