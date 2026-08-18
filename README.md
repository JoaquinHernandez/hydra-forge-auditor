# hydra-forge-auditor
This project provides a unified orchestration engine that analyzes password lists for compliance (NIST SP 800-63B),

# ⚡ Hydra-Forge: Password Policy Auditor & Cracking Bridge

An auditing and wordlist optimization utility designed to evaluate credential corpuses against enterprise security standards (NIST SP 800-63B) and automatically generate attack masks for **Hashcat**, **John the Ripper**, and **THC-Hydra**.

---

## ✨ Features
- **Entropy Quantification**: Computes Shannon entropy bits based on character set complexity.
- **Automated Mask Extraction**: Generates optimal Hashcat/John mask representations (`?u?l?l?d?s`) directly from sample candidate lists.
- **CLI Bridge Syntax Generator**: Pre-populates ready-to-run penetration testing commands for Hydra and Hashcat.
- **Zero Dependencies**: Pure Python standard library implementation.

---

## 🚀 Usage
```bash
# Run against the sample wordlist
python3 hydra_forge.py target_passwords.txt
