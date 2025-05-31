# Eurojackpot Statistics Analyzer

This Streamlit application allows you to analyze Eurojackpot number statistics by uploading a PDF document or entering a URL of a webpage containing Eurojackpot draw data. The app extracts the data, analyzes the frequency of number combinations, and displays the top 4 most frequently drawn combinations.

## Features

- Upload a PDF file containing Eurojackpot statistics.
- Enter a URL to scrape Eurojackpot statistics from a webpage.
- Analyze and display the most frequently drawn number combinations.
- Download the analysis results as a CSV file.

## Installation

1. Clone or download this repository.
2. Navigate to the `streamlit-eurojackpot` directory.
3. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app with the following command:

```bash
streamlit run app.py
```

## How to Use

- Select the input mode from the sidebar: either upload a PDF file or enter a URL.
- If uploading a PDF, choose a valid Eurojackpot statistics PDF file.
- If entering a URL, provide a valid webpage URL containing Eurojackpot draw data.
- The app will extract and analyze the data, then display the top 4 most frequently drawn combinations.
- You can download the results as a CSV file.

## Troubleshooting

- Ensure the PDF file is not corrupted and contains readable text.
- Verify the URL is accessible and contains Eurojackpot statistics in a parsable format.
- If no valid combinations are found, try a different file or URL.

## License

This project is open source and free to use.
