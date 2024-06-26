# Stock Data App 

This is a Flask web application that fetches quarterly financial data for a given stock from Screener.in and displays a bar chart of the net profit over the years.

## Features

- User inputs the stock name.
- Scrapes quarterly results data from Screener.in.
- Displays the net profit over the years in a bar chart.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your local machine.
- `pip` (Python package installer) is available.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/StockDataApp.git
    cd StockDataApp
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the Flask application:**

    ```sh
    python app.py
    ```

2. **Open your web browser and go to:**

    ```
    http://127.0.0.1:5000/
    ```

3. **Use the application:**

    - Enter the stock name in the input field and click "Submit".
    - View the bar chart displaying the net profit over the years.

## File Structure

