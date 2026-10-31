# hydra-forge-auditor
This project provides a unified orchestration engine that analyzes password lists for compliance (NIST SP 800-63B),

# ⚡ Hydra-Forge: Password Policy Auditor & Cracking Bridge

<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/4eaff9de-6a6c-40bf-826f-4dbf0bdaa25d" />


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
