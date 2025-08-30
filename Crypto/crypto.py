from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.buyucoin.com/altcoin-rate-inr-india'


def get_data():
    """
    Fetch data from the website and parse it.
    """
    try:
        res = requests.get(url)
        res.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

    soup = BeautifulSoup(res.text, 'lxml')

    table = soup.find('table', {'id': 'inr_rate'})
    if not table:
        print("Error: Could not find the table with id 'inr_rate'.")
        return []

    all_rows = table.find_all('tr')
    data = []

    # Extract header and rows
    for row in all_rows:
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
        print(" {:<25} {:<20} {:<20} {}".format(*header))  # Print the header
        for row in data:
            print(" {:<25} {:<20} {:<20} {}".format(*row))
    else:
        print("No data to display.")


def store_csv(data):
    """
    Store the data in a CSV file.
    """
    if data:
        df = pd.DataFrame(data, columns=['Coin', 'Price (INR)', 'Change (24h)', 'Volume (24h)'])
        df.to_csv('Crypto.csv', index=False)
        print("Data has been stored in 'Crypto.csv'.")
    else:
        print("No data to store in CSV.")


def store_excel(data):
    """
    Store the data in an Excel file.
    """
    if data:
        df = pd.DataFrame(data, columns=['Coin', 'Price (INR)', 'Change (24h)', 'Volume (24h)'])
        df.to_excel('Crypto.xlsx', sheet_name='Prices', index=False)
        print("Data has been stored in 'Crypto.xlsx'.")
    else:
        print("No data to store in Excel.")


def main():
    """
    Main function to execute the scraping, display, and storage.
    """
    data = get_data()
    print_data(data)
    store_csv(data)
    store_excel(data)


if __name__ == '__main__':
    main()
