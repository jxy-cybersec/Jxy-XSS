Here’s the updated `README.md` file reflecting the tool's renaming to **JXY-XSS**, along with the new changes and features added:

---

# JXY-XSS - Automated XSS Vulnerability Scanner

JXY-XSS is a Python-based tool designed to detect and exploit Cross-Site Scripting (XSS) vulnerabilities with near-zero false positives. The tool includes advanced payload management, WAF detection, accurate response analysis, and crawling capabilities to identify potential vulnerabilities in web applications.

---

## Features
- DOM-Based XSS Detection
- WAF Detection and Adaptive Payloads
- Form and URL Parameter Scanning
- Context-Aware Payload Injection
- Accurate Reflection Validation to Reduce False Positives

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
```

### Step 2: Create and Activate a Virtual Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

### Step 3: Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 4: Install `wafw00f` (For WAF Detection)
Ensure `wafw00f` is installed to enable WAF detection:
```bash
pip install wafw00f
```

---

## Usage

### Basic Command
Run the tool by specifying the target URL:
```bash
python main.py -u https://example.com
```

### Workflow
1. **Crawling**: The tool crawls the target URL to identify links, query parameters, and forms.
2. **WAF Detection**: If a WAF is detected, the tool selects specific payloads to bypass its protections.
3. **Payload Injection**: The tool injects payloads into discovered parameters and forms.
4. **Response Analysis**: Analyzes the responses for signs of successful XSS execution.

---

## Payloads

### Default Payloads
- General-purpose payloads used when no WAF is detected:
  - `<script>alert('XSS')</script>`
  - `"><svg onload=alert('XSS')>`
  - `<img src=x onerror=alert('XSS')>`

### WAF-Specific Payloads
- **CloudFront Payloads**:
  - `<script>alert('CloudFront Bypass')</script>`
  - `<svg onload=alert('CloudFront')>`
- **Akamai Payloads**:
  - `<script>alert('Akamai Bypass')</script>`
  - `"><img src=x onerror=alert('Akamai')>`

You can add more payload files for different WAFs in the `payloads.py` module.

---

## Dependencies

- **`requests`**: For sending HTTP requests.
- **`beautifulsoup4`**: For parsing HTML.
- **`lxml`**: XML parser used by BeautifulSoup.
- **`wafw00f`**: For detecting Web Application Firewalls (WAFs).

To install all dependencies, use:
```bash
pip install -r requirements.txt
```

---

## Example Output
### When a WAF is Detected:
```
[2024-11-21 10:30:53,335] [JXY-XSS] [INFO]: Starting scan for: https://example.com/
[*] Detecting WAF...
[+] Detected WAF: CloudFront
[*] Using payloads from: payloads_cloudfront.txt
[2024-11-21 10:30:53,335] [JXY-XSS] [INFO]: Crawling target for injection points...
[2024-11-21 10:30:55,940] [JXY-XSS] [INFO]: Testing endpoint: https://example.com/search
[+] Vulnerable parameter found: q with payload: <script>alert('XSS')</script>
```

### When No WAF is Detected:
```
[2024-11-21 10:30:53,335] [JXY-XSS] [INFO]: Starting scan for: https://example.com/
[*] Detecting WAF...
[!] No WAF detected. Proceeding with default payloads.
[*] Using payloads from: payloads_default.txt
[2024-11-21 10:30:53,335] [JXY-XSS] [INFO]: Crawling target for injection points...
[2024-11-21 10:30:55,940] [JXY-XSS] [INFO]: Testing endpoint: https://example.com/search
[+] Vulnerable parameter found: q with payload: <script>alert('XSS')</script>
```

---

## Future Enhancements
- Add support for DOM-based XSS detection.
- Integrate multi-threaded crawling for faster scans.
- Expand payload library with advanced obfuscation techniques.

---

## Acknowledgments
- [OWASP](https://owasp.org/) for XSS documentation and examples.
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) for their comprehensive payload library.