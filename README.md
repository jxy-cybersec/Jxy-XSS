# JXY-XSS - Automated XSS Vulnerability Scanner

JXY-XSS is a Python-based tool designed to detect and exploit Cross-Site Scripting (XSS) vulnerabilities with near-zero false positives. The tool includes advanced payload management, WAF detection, accurate response analysis, and crawling capabilities to identify potential vulnerabilities in web applications.

---

## Features
- Accurate Reflection Detection
- Payload Mutation and Analysis
- Endpoint Crawling
- WAF Detection
- Supports URL and File-Based Scanning
- Server-Side XSS Analysis (No Browser Required)

---

## Prerequisites
- Python 3.8 or later installed on your system.
- Pip package manager to handle Python dependencies.

---

## Installation

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/jxy-cybersec/Jxy-XSS.git
cd JXY-XSS

### Step 2: Create and Activate a Virtual Environment

  Create a virtual environment:

    python -m venv venv

  Activate the virtual environment:

  Windows:

    venv\Scripts\activate

  macOS/Linux:

    source venv/bin/activate

### Step 3: Install Dependencies

  Install the required Python libraries:

    pip install -r requirements.txt


  Usage
  Basic Command

  Run the tool by specifying the target URL:

    python main.py -u https://example.com

  Update the Tool

  Update to the latest version directly from the terminal:

    python main.py -up


Workflow

    Crawling: The tool crawls the target URL to identify links, query parameters, and forms.
    WAF Detection: If a WAF is detected, the tool selects specific payloads to bypass its protections.
    Payload Injection: The tool injects payloads into discovered parameters and forms.
    Response Analysis: Analyzes the responses for signs of successful XSS execution.

Dependencies

    requests: For sending HTTP requests.
    beautifulsoup4: For parsing HTML.
    lxml: XML parser used by BeautifulSoup.

Example Output
When a WAF is Detected:

  [INFO] Detected WAF: Cloudflare
  [INFO] Using WAF-specific payloads.

When No WAF is Detected:

  [INFO] No WAF detected. Proceeding with default payloads.

Acknowledgments

    OWASP for XSS documentation and examples.
    PayloadsAllTheThings for their comprehensive payload library.

