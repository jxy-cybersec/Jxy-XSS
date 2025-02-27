import os
from modules.mutators import generate_mutations
from modules.utils import logger

def load_payloads(payload_dir="payloads"):
    """Load all payloads from files in the payloads directory."""
    payloads = []
    try:
        for file in os.listdir(payload_dir):
            file_path = os.path.join(payload_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                file_payloads = [line.strip() for line in f if line.strip()]
                logger.info(f"[+] Loaded {len(file_payloads)} payloads from {file}.")
                payloads.extend(file_payloads)

        # Add mutations to payloads
        mutated_payloads = []
        for payload in payloads:
            mutations = generate_mutations(payload)
            mutated_payloads.extend(mutations.values())
        logger.info(f"[+] Total payloads including mutations: {len(mutated_payloads)}.")
        return mutated_payloads
    except Exception as e:
        logger.error(f"[-] Error loading payloads: {e}")
        return []
