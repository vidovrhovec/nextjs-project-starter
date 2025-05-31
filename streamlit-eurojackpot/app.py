import streamlit as st
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

def parse_pdf(uploaded_file):
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
        return text
    except Exception as e:
        st.error(f"Error processing the PDF: {e}")
        return None

def scrape_statistics(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # This is a generic extraction; user may need to adjust based on actual page structure
        data = soup.get_text(separator=" ")
        return data
    except Exception as e:
        st.error(f"Error fetching the URL: {e}")
        return None

def analyze_statistics(data):
    try:
        # Regex pattern to find combinations of 5 to 7 numbers separated by commas or spaces
        pattern = r"(\d{1,2}(?:[,\s]\d{1,2}){4,6})"
        combinations = re.findall(pattern, data)
        if not combinations:
            st.error("No valid number combinations found.")
            return None

        # Normalize combinations by removing spaces and sorting numbers to count unique sets
        normalized = []
        for comb in combinations:
            nums = re.split(r"[,\s]+", comb.strip())
            nums = sorted([int(n) for n in nums])
            normalized.append(",".join(str(n) for n in nums))

        df = pd.DataFrame(normalized, columns=['Combination'])
        freq = df['Combination'].value_counts().reset_index()
        freq.columns = ['Combination', 'Frequency']
        return freq.head(4)
    except Exception as e:
        st.error(f"Error during analysis: {e}")
        return None

def fetch_models_openai(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get("https://api.openai.com/v1/models", headers=headers)
        response.raise_for_status()
        models = response.json().get("data", [])
        return [model["id"] for model in models]
    except Exception as e:
        st.error(f"Error fetching OpenAI models: {e}")
        return []

def fetch_models_custom(api_endpoint, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        url = api_endpoint.rstrip("/") + "/v1/models"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        models = response.json().get("data", [])
        return [model["id"] for model in models]
    except Exception as e:
        st.error(f"Error fetching models from custom API: {e}")
        return []

def main():
    st.set_page_config(page_title="Eurojackpot Statistics Analyzer", layout="centered")
    st.title("Eurojackpot Statistics Analyzer")
    st.markdown(
        """
        Analyze Eurojackpot number statistics from a PDF document or a web page.
        Upload a PDF or enter a URL containing Eurojackpot draw data to find the most frequently drawn combinations.
        """
    )

    st.sidebar.header("API Configuration")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    custom_api_endpoint = st.sidebar.text_input("Custom API Endpoint (OpenAI compatible)")
    custom_api_key = st.sidebar.text_input("Custom API Key", type="password")

    openai_models = []
    custom_models = []

    if openai_api_key:
        with st.spinner("Fetching OpenAI models..."):
            openai_models = fetch_models_openai(openai_api_key)

    if custom_api_endpoint and custom_api_key:
        with st.spinner("Fetching models from custom API..."):
            custom_models = fetch_models_custom(custom_api_endpoint, custom_api_key)

    all_models = list(set(openai_models + custom_models))
    selected_model = None
    if all_models:
        selected_model = st.sidebar.selectbox("Select Model", all_models)

    input_mode = st.sidebar.radio("Select input mode:", ("Upload PDF", "Enter URL"))

    data = None
    if input_mode == "Upload PDF":
        uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Processing PDF..."):
                data = parse_pdf(uploaded_file)
    else:
        url = st.sidebar.text_input("Enter the URL of the statistics page")
        if url:
            with st.spinner("Fetching data from URL..."):
                data = scrape_statistics(url)

    if data:
        with st.spinner("Analyzing data..."):
            results = analyze_statistics(data)
        if results is not None and not results.empty:
            st.subheader("Top 4 Most Frequently Drawn Combinations")
            st.table(results)
            csv = results.to_csv(index=False)
            st.download_button("Download Results as CSV", data=csv, file_name="eurojackpot_stats.csv", mime="text/csv")
        else:
            st.warning("No results to display.")

if __name__ == "__main__":
    main()
