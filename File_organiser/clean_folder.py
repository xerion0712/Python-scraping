from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

url = 'https://www.buyucoin.com/altcoin-rate-inr-india'


def get_data():
    """
    Fetch data from the website and parse it.
    """
    try:
        logging.info(f"Fetching data from {url}...")
        res = requests.get(url)
        res.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return []

    soup = BeautifulSoup(res.text, 'lxml')

    # Find the table with the altcoin data
    table = soup.find('table', {'id': 'inr_rate'})
    if not table:
        logging.error("Error: Could not find the table with id 'inr_rate'.")
        return []

    # Parse rows from the table
    rows = table.find_all('tr')
    data = []

    for row in rows:
        row_data = [item.text.strip() for item in row.find_all('td')]
        if row_data:
            data.append(row_data)

    return data


def print_data(data):
    """
    Print the data in a formatted way.
    """
    if data:
        header = ['Coin', 'Price (INR)', 'Change (24h)', 'Volume (24h)']
        logging.info(f"Printing {len(data)} rows of data...")
        print(" {:<25} {:<20} {:<20} {}".format(*header))  # Print the header
        for row in data:
            print(" {:<25} {:<20} {:<20} {}".format(*row))
    else:
        logging.warning("No data to display.")


def store_csv(data):
    """
    Store the data in a CSV file.
    """
    if data:
        df = pd.DataFrame(data, columns=['Coin', 'Price (INR)', 'Change (24h)', 'Volume (24h)'])
        df.to_csv('Crypto.csv', index=False)
        logging.info("Data has been stored in 'Crypto.csv'.")
    else:
        logging.warning("No data to store in CSV.")


def store_excel(data):
    """
    Store the data in an Excel file.
    """
    if data:
        df = pd.DataFrame(data, columns=['Coin', 'Price (INR)', 'Change (24h)', 'Volume (24h)'])
        df.to_excel('Crypto.xlsx', sheet_name='Prices', index=False)
        logging.info("Data has been stored in 'Crypto.xlsx'.")
    else:
        logging.warning("No data to store in Excel.")


def main():
    """
    Main function to execute the scraping, display, and storage.
    """
    logging.info("Starting the scraping process...")
    data = get_data()

    if data:
        print_data(data)
        store_csv(data)
        store_excel(data)
    else:
        logging.error("No data found to process.")


if __name__ == '__main__':
    main()
