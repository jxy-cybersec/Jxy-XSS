from modules.mutators import generate_mutations

def load_payloads(file_paths=None):
    """
    Load payloads from multiple specified files and apply mutations.
    """
    if file_paths is None:
        file_paths = [
            "payloads/payloads_default.txt",
            "payloads/payloads_js.txt",
            "payloads/payloads_html.txt",
            "payloads/payloads_attributes.txt",
            "payloads/payloads_blind.txt",
            "payloads/custom_payloads.txt"
        ]

    payloads = set()  # To avoid duplicates
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        mutations = generate_mutations(line.strip())
                        payloads.update(mutations.values())
        except Exception as e:
            raise RuntimeError(f"Failed to load payloads from {file_path}: {e}")

    return list(payloads)
