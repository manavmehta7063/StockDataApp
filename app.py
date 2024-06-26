from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def fetch_and_filter_data(stock_name):
    url = f'https://www.screener.in/company/{stock_name}/consolidated/'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'data-table responsive-text-nowrap'})

    if not table:
        raise Exception("Failed to find the quarterly results table.")

    headers = [th.text.strip() for th in table.find('thead').find_all('th')] if table.find('thead') else []
    rows = []
    tbody = table.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            cells = [td.text.strip() for td in tr.find_all('td')]
            rows.append(cells)

    if not headers or not rows:
        raise Exception("Failed to extract data from the table.")

    df = pd.DataFrame(rows, columns=headers)
    net_profit_row = df[df[headers[0]].str.contains('Net Profit', case=False, na=False)]
    return net_profit_row

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    stock_name = request.form['stock_name']

    try:
        net_profit_row = fetch_and_filter_data(stock_name)
    except Exception as e:
        return str(e)

    # Extract numeric data while preserving large values
    net_profit_row = net_profit_row.iloc[:, 1:].replace({',': ''}, regex=True).astype(float).dropna(axis=1)

    if net_profit_row.empty or net_profit_row.shape[1] == 0:
        return "No valid data found for Net Profit."

    if net_profit_row.shape[0] != 1:
        return "Unexpected data format. Expected a single row for Net Profit."

    years = net_profit_row.columns
    values = net_profit_row.iloc[0]

    max_value = values.max()
    if max_value > 1000:
        values = values / 1000
        ylabel = 'Net Profit (in Thousands of Crores)'
    else:
        ylabel = 'Net Profit (in Crores)'

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(years, values, align='center')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., yval, f'{yval:.2f}', va='bottom', ha='center')

    plt.title(f'Net Profit for {stock_name}')
    plt.xlabel('Quarterly Data')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('results.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
