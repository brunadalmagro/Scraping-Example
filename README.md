# Web Scraper for Mercado Livre and OLX

A Python script that scrapes product data (tables in this example) from Mercado Livre and OLX using Selenium and BeautifulSoup.

## Features

- Scrapes product names, prices, and links from:
  - Mercado Livre (https://lista.mercadolivre.com.br)
  - OLX (https://www.olx.com.br)
- Automates browser interactions using Selenium WebDriver
- Saves results to CSV files
- Includes price formatting functionality

## Requirements

- Python 3.7+
- Required packages (install via `pip install -r requirements.txt`):

selenium
beautifulsoup4
pandas

## Setup

### 1. Clone this repository:
 ```bash
   git clone https://github.com/yourusername/web-scraper.git
   cd web-scraper
```
### 2. Install dependencies:
```bash

  pip install -r requirements.txt
```
### 3. Download geckodriver (for Firefox):

    Download from: https://github.com/mozilla/geckodriver/releases

### 4.Place in project directory or update path in script:

    service = Service(r'C:\geckodriver-v0.36.0-win32\geckodriver.exe')

## Usage

Run the script:
```bash

python scraper.py
```
Output files will be saved to:

    csv-files/mercado_livre_mesas.csv

    csv-files/olx_mesas.csv

## Customization

To scrape different products:
```bash
    # Change the search URLs:
  ml_link = "https://lista.mercadolivre.com.br/mesas"  # Change 'mesas' to your product
  driver.get("https://www.olx.com.br/brasil?q=mesas")  # Change 'mesas' to your product
```
Adjust the selectors if website structure changes:
```bash
    # Mercado Livre selectors
    EC.presence_of_element_located((By.CLASS_NAME, "ui-search-item__title"))

    # OLX selectors
    EC.presence_of_element_located((By.CLASS_NAME, "olx-adcard__content"))
```
### Output Format

CSV files contain:
-     Product name

-     Formatted price (BRL)

-     Product URL

### Example:
nome_produto, preco_formatado, link_produto
"Mesa de jantar", R$ 1.200,00, https://www.olx.com.br/item/123

Important Notes

    This script is for educational purposes only

    Respect websites' Terms of Service and robots.txt

    Add delays between requests to avoid being blocked

    Websites may change their structure - selectors may need updating

### License

MIT License


## Key features of this README:
1. Clear structure with all essential sections
2. Installation and usage instructions
3. Customization guidance
4. Important notes about web scraping ethics
5. Clean Markdown formatting

### You should also create a `requirements.txt` file with:

- selenium
- beautifulsoup4
- pandas



The README assumes your script is named `scraper.py` - adjust if you're using a different filename.

