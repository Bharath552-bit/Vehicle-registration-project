Vehicle Registration Dashboard 🚗
This project is an interactive dashboard built with Streamlit and Python to analyze vehicle registration data from an investor's perspective. It provides a clean, user-friendly interface to visualize key performance indicators, trends, and growth metrics.

✨ Features
Year-over-Year (YoY) & Quarter-over-Quarter (QoQ) Analysis: Instantly view growth metrics for total vehicles.

Interactive Filters: Easily filter data by date range, vehicle category, and manufacturer.

Trend Visualizations: Line charts to show monthly registration trends over time.

Market Share Breakdown: Pie charts illustrating the distribution of vehicles by category and manufacturer.

Responsive UI: The dashboard is designed to be fully responsive and works well on various screen sizes.

🚀 How to Run the Project
Follow these simple steps to set up and run the dashboard locally.

Prerequisites
Make sure you have Python 3.7 or higher installed on your system.

Installation
Clone this repository or download the project files.

Install the required Python libraries using pip:

pip install streamlit pandas numpy plotly python-dateutil

Running the App
Save the provided Python code as app.py.

Open your terminal or command prompt.

Navigate to the directory where you saved app.py.

Run the following command to start the Streamlit server:

streamlit run app.py

The dashboard will automatically open in your default web browser.

⚙️ Project Structure
The code is organized into modular sections for readability and easy maintenance:

Data Generation: A function to create mock vehicle registration data. This is where you would integrate your actual data source (e.g., a database connection or a CSV file loader).

UI Layout: Defines the overall structure and components of the Streamlit dashboard, including the sidebar filters and main content area.

Metrics & Calculations: Contains functions to compute the YoY and QoQ growth rates.

Visualizations: Creates and displays the various charts and graphs using the Plotly Express library.

💡 Future Enhancements
Real Data Integration: Replace the mock data with a connection to a real data source (e.g., a SQL database, a CSV file, or a web scraping script for the Vahan dashboard).

Advanced Analytics: Add predictive modeling or anomaly detection to forecast future trends and highlight unusual registration activity.

Additional Views: Incorporate geographical maps to visualize vehicle registrations by state or district.