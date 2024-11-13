# Amy's Crawler

## Description

Amy's Crawler automates the process of gathering academic and research-related content across multiple sources. By simply providing a keyword, users can search Wikipedia, arXiv, Google Scholar, and PubMed for relevant pages. The crawler extracts useful data, indexes it for easy search, and handles common HTTP errors like 404 (page not found) and 429 (too many requests) gracefully with retry mechanisms.

## Features

- **Keyword Search**: Allows searching for a specific keyword across multiple platforms such as Wikipedia, arXiv, Google Scholar, and PubMed.
- **Content Indexing**: Collects and stores the content of pages where the keyword is found, including keyword occurrences and links to related pages.
- **Error Handling**: Gracefully handles 404 errors with retries and 429 errors by waiting and retrying after a delay, ensuring the crawler works reliably.
- **Link Extraction**: Extracts up to 20 related links from each page containing the searched keyword.
- **Search Results**: Displays the pages where the keyword was found, including title, URL, and the number of keyword occurrences on each page.

## Installation

### Clone the repository:

To get started with Amy's Crawler, first clone the repository to your local machine:

```bash
git clone https://github.com/komyl/Amys_Crawler.git
cd Amys_Crawler
```

## Install Requirements

Before running the project, ensure you have the required dependencies installed. You can do this by installing the dependencies listed in the `requirements.txt` file.

Run the following command to install the required libraries:

  ```bash
  pip install -r requirements.txt
 ```

## Usage

To run the search engine, use the following command in your terminal:

```bash
python Amys_Crawler.py
```

## Project Structure

The project structure for the Amy's Crawler is as follows:  

- **Amys_Crawler.py**: Main Python file containing all scraping functions.
- **requirements.txt**: File containing the required libraries to run the script.


## Dependencies

The following Python libraries are required to run Amy's Crawler:

- `requests`: For sending HTTP requests to websites.
- `beautifulsoup4`: For parsing HTML content and extracting useful data.
- `re`: For regular expression operations to search for keywords and process links.
- `time`: For handling retries and delays between requests.
- `collections`: For managing indexed words and related links efficiently.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


## Authors

This project was developed by **Komeyl Kalhorinia** and **Ameneh Zarebidoki**. You can reach us at [Komylfa@gmail.com](AmenehZarebidoki@gmail.com) for any inquiries or contributions.

## Made with ❤️ by Komeyl Kalhorinia and AmenehZarebidoki

