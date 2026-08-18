import os
import sys
import json
import math
import re

# ANSI Terminal Color Tokens
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[38;5;196m"
GREEN  = "\033[38;5;48m"
CYAN   = "\033[38;5;51m"
AMBER  = "\033[38;5;214m"
MAGENTA= "\033[38;5;201m"
GRAY   = "\033[38;5;242m"

BANNER = f"""{CYAN}{BOLD}
 ██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗      ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
 ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗     ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
 ███████║ ╚████╔╝ ██║  ██║██████╔╝███████║     █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
 ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║     ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
 ██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║     ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
 ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{RESET}{AMBER} » UNIFIED CREDENTIAL AUDITOR & HASHCAT / JOHN / HYDRA BRIDGE «{RESET}
"""

class HydraForgeAuditor:
    def __init__(self, policy_path="policy_rules.json"):
        if not os.path.exists(policy_path):
            print(f"{RED}[-] Config file '{policy_path}' not found.{RESET}")
            sys.exit(1)

        with open(policy_path, "r") as f:
            self.policy = json.load(f)

    def calculate_entropy(self, password):
        """Calculates Shannon bits of entropy."""
        charset_size = 0
        if re.search(r'[a-z]', password): charset_size += 26
        if re.search(r'[A-Z]', password): charset_size += 26
        if re.search(r'[0-9]', password): charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', password): charset_size += 32

        if charset_size == 0 or len(password) == 0:
            return 0.0
        return round(len(password) * math.log2(charset_size), 2)

    def generate_hashcat_mask(self, password):
        """Converts raw password into a Hashcat/John mask syntax (?u?l?d?s)."""
        mask = []
        for char in password:
            if char.isupper(): mask.append("?u")
            elif char.islower(): mask.append("?l")
            elif char.isdigit(): mask.append("?d")
            else: mask.append("?s")
        return "".join(mask)

    def audit_passwords(self, wordlist_path):
        if not os.path.exists(wordlist_path):
            print(f"{RED}[-] Target wordlist '{wordlist_path}' not found.{RESET}")
            return

        print(BANNER)
        print(f"{BOLD}Auditing Target Wordlist:{RESET} {CYAN}{wordlist_path}{RESET}")
        print("=" * 85)

        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]

        total_passwords = len(passwords)
        compliant_count = 0
        masks = set()

        print(f"{'PASSWORD':<28} {'ENTROPY':<10} {'HASHCAT MASK':<24} {'POLICY STATUS'}")
        print("-" * 85)

        for pwd in passwords:
            entropy = self.calculate_entropy(pwd)
            mask = self.generate_hashcat_mask(pwd)
            masks.add(mask)

            # Audit checks
            failures = []
            if len(pwd) < self.policy.get("min_length", 12):
                failures.append("Too Short")
            if any(b.lower() in pwd.lower() for b in self.policy.get("blacklisted_substrings", [])):
                failures.append("Blacklisted Pattern")
            if not re.search(r'[^a-zA-Z0-9]', pwd):
                failures.append("Missing Symbol")

            if not failures:
                status = f"{GREEN}✓ COMPLIANT{RESET}"
                compliant_count += 1
            else:
                status = f"{RED}✕ {', '.join(failures)}{RESET}"

            display_pwd = (pwd[:24] + "...") if len(pwd) > 27 else pwd
            print(f"{display_pwd:<28} {str(entropy) + ' bits':<10} {mask:<24} {status}")

        print("=" * 85)
        print(f"\n{BOLD}Audit Results:{RESET} {compliant_count}/{total_passwords} Passed Policy Standards.")
        print(f"{BOLD}Extracted Unique Attack Masks ({len(masks)}):{RESET} {', '.join(list(masks)[:4])}")

        # Provide CLI command generators for industry tools
        print(f"\n{AMBER}{BOLD}[🛠️ AUTOMATED TOOL SYNTAX GENERATOR]{RESET}")
        print(f"  {CYAN}▸ John the Ripper:{RESET}  john --wordlist={wordlist_path} --format=raw-sha256 target_hashes.txt")
        print(f"  {CYAN}▸ Hashcat Mask Mode:{RESET} hashcat -m 0 -a 3 target_hashes.txt {' '.join(list(masks)[:2])}")
        print(f"  {CYAN}▸ Hydra Network Spray:{RESET} hydra -L users.txt -P {wordlist_path} ssh://192.168.1.50 -t 4\n")

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "target_passwords.txt"
    auditor = HydraForgeAuditor()
    auditor.audit_passwords(target_file)
