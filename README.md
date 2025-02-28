# JXY-XSS - Automated XSS Vulnerability Scanner

JXY-XSS is a Python-based tool designed to detect and exploit Cross-Site Scripting (XSS) vulnerabilities with near-zero false positives. The tool includes advanced payload management, WAF detection, accurate response analysis, and crawling capabilities to identify potential vulnerabilities in web applications.

---

## 🚀 Features
- ✅ Accurate Reflection Detection  
- 🎭 Payload Mutation and Analysis  
- 🔎 Endpoint Crawling and Parameter Testing  
- 🛡️ WAF Detection and Adaptive Payload Selection  
- 📂 Supports **Single URL & File-Based Scanning**  
- ⚡ **Fast and Efficient** Server-Side XSS Analysis (No Browser Required)  
- 🏗️ **Automated Updates** via `--update` Command  

---

## 🔧 Prerequisites
- Python **3.8 or later** installed on your system.  
- Pip package manager to handle Python dependencies.  

---

## 📌 Installation

1️⃣ Clone the Repository
Clone the repository to your local machine:  
```bash
git clone https://github.com/jxy-cybersec/Jxy-XSS.git
cd JXY-XSS


2️⃣ Create and Activate a Virtual Environment

Create a virtual environment:
python -m venv venv


Activate the virtual environment:

  Windows:
    venv\Scripts\activate

  macOS/Linux:
    source venv/bin/activate


3️⃣ Install Dependencies

Install the required Python libraries:

pip install -r requirements.txt

__________________________________________________

🛠️ Usage
🔍 Basic Scanning
✅ Scan a Single URL:

python main.py -u https://example.com

📂 Scan Multiple URLs from a File:

python3 main.py -uf urls.txt

(Each line in urls.txt should contain a new URL)
🔄 Update the Tool:

Upgrade to the latest version directly from the terminal:

python main.py --update

__________________________________________________

🏗️ Workflow

1️⃣ Crawling: The tool crawls the target URL to identify links, query parameters, and forms.
2️⃣ WAF Detection: If a WAF is detected, the tool selects specific payloads to bypass its protections.
3️⃣ Payload Injection: The tool injects mutated payloads into discovered parameters and forms.
4️⃣ Response Analysis: Analyzes the responses for XSS execution signs and detects reflected/stored XSS.

__________________________________________________

📦 Dependencies

    📨 requests → For sending HTTP requests.
    🕵️‍♂️ beautifulsoup4 → For parsing HTML during crawling.
    ⚡ lxml → XML parser used by BeautifulSoup.
    🎨 termcolor → For colored terminal output.

Install all dependencies via:

pip install -r requirements.txt

__________________________________________________

🔬 Example Output
🛡️ When a WAF is Detected:

[INFO] Detected WAF: Cloudflare
[INFO] Using WAF-specific payloads.

✅ When No WAF is Detected:

[INFO] No WAF detected. Proceeding with default payloads.
[INFO] Injected payload: <script>alert(1)</script>
[INFO] [+] Vulnerable to XSS with payload: <script>alert(1)</script>

__________________________________________________

🎯 Future Enhancements

    🖥️ Improved DOM-Based XSS Detection
    ⚡ Multi-threaded Payload Injection for Faster Scanning
    🎭 More Advanced XSS Obfuscation Techniques

__________________________________________________

🙌 Acknowledgments

    🛡️ OWASP for XSS documentation and examples.
    🎭 PayloadsAllTheThings for their extensive payload library.