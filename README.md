# Gemini-DeepResearch-API

A replica of the Gemini Advanced DeepResearch Feature, but free with full customization & Open-source.

## Description

This project aims to replicate the advanced DeepResearch capabilities of Gemini, offering a free, customizable, and open-source alternative. The tool leverages the LangSearch API for web searches and the Gemini API for content generation, providing in-depth research reports on user-specified topics.

## Features

-   **Customizable Research:** Users can specify the topic, length, desired personality of the research, and the number of search results to use.
-   **Deep Web Search:** Utilizes the LangSearch API to perform comprehensive web searches, gathering relevant information for analysis.
-   **AI-Powered Content Generation:** Employs the Gemini API to generate detailed research reports based on the search results, adhering to specified length and personality traits.
-   **Output Formatting:** Generates output in both Markdown (.md) and PDF formats, ensuring readability and ease of sharing.
-   **Open-Source:** Fully open-source, allowing for community contributions and customization to fit specific needs.
-   **Line Numbering:** Every line will be numbered, for better formating purposes.

## Requirements

-   Python 3.6+
-   `requests`
-   `json`
-   `os`
-   `google.genai`
-   `python-dotenv`
-   `re`
-   `markdown`
-   `pdfkit`
-   wkhtmltopdf (for PDF conversion)

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/YoussefElsafi/Gemini-DeepResearch-API
    cd Gemini-DeepResearch-API
    ```

2.  Install the required Python packages:

    ```bash
    pip install requests google-generativeai python-dotenv markdown pdfkit
    ```

3.  Install wkhtmltopdf:

    -   ### **Windows:**
    -    Already Built-in
          

    -   ### **macOS:**

       *   Not Supported Yet.
         


    -   ### **Linux (Debian/Ubuntu):**

       *   Not Supported Yet.
         

4.  Obtain API keys:

    -   Get a LangSearch API key from [LangSearch](https://langsearch.com/api-keys).
    -   Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

5.  Create a `.env` file in the project directory with the following content:

    ```
    search_api_key="Your_LangSearch_API_Key"
    gemini_api="Your_Gemini_API_Key"
    ```

## Configuration

-   **API Keys:** Store your LangSearch and Gemini API keys in the `.env` file to keep them secure.
-   **wkhtmltopdf Path (Windows):** If `pdfkit` fails to find `wkhtmltopdf.exe`, manually specify the path in the script:

    ```python
    path_wkhtmltopdf = r'Convert/wkhtmltopdf.exe'  # Replace with the actual path
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_file(temp_html, pdf_filename, configuration=config)
    ```

## Usage

1.  Run the script:

    ```bash
    python DeepResearch.py
    ```

2.  The script will prompt you for:
    -   The topic you want to research.
    -   The desired length of the research (number of lines).
    -   The desired personality tone (e.g., Professional, Casual, Friendly).
    -   The number of search results to use (max 100).

3.  The script will then:
    -   Perform a web search using the LangSearch API.
    -   Analyze the search results.
    -   Generate a research report using the Gemini API.
    -   Save the report in Markdown and PDF formats in a folder named `Researches/{title}`.

## Example

```
What topic do you want to research?: Artificial Intelligence
How many lines do you want the research to be? (1-1000): 500
What personality do you want the research to be in? (Professional, Casual, Friendly, etc..): Professional
How many search results do you want to use? (1-100 Max): 50
```

The script will then generate a detailed, 500-line research report on Artificial Intelligence, written in a professional tone, using the top 50 search results.

## Code Structure

-   `DeepResearch.py`: The main script containing the logic for web search, content generation, and output formatting.
-   `Researches/`: A directory where the generated research reports are saved.
-   `.env`: A file containing the API keys.

## Functions

-   `analyze_search_results(json_string)`: Analyzes search results from a JSON string to count sites with summaries.
-   `generate()`: Generates content using the Gemini API based on search results and user inputs.
-   `remove_line_numbers(text)`: Removes line numbers from a text that has been previously numbered.

## Error Handling

-   The script includes error handling for JSON decoding issues and PDF creation failures.
-   If PDF creation fails, the research report will still be saved in Markdown format.

## Disclaimer

This project is intended for educational and research purposes. Please use it responsibly and respect the terms of service of the LangSearch and Gemini APIs.
