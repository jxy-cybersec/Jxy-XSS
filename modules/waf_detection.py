import subprocess
import shutil

def detect_waf(url):
    """
    Detect the WAF protecting the target URL using wafw00f.
    """
    if not shutil.which("wafw00f"):
        print("[!] wafw00f is not installed. Install it using: pip install wafw00f")
        return None

    try:
        print("[*] Detecting WAF...")
        result = subprocess.run(
            ["wafw00f", "-a", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print("[*] WAF Detection Result:")
            print(result.stdout)
            for line in result.stdout.splitlines():
                if "is behind" in line:
                    waf_name = line.split("is behind")[1].strip()
                    print(f"[+] Detected WAF: {waf_name}")
                    return waf_name
        else:
            print("[!] WAF detection failed.")
    except Exception as e:
        print(f"[!] WAF detection error: {e}")
    return None
