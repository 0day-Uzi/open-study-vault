"""
open-study-vault — Auto README Updater
Run this script before every git push.
It scans your vault, detects new files, and updates README.md automatically.
"""

import os
import re
from datetime import datetime
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────
VAULT_ROOT = Path(__file__).parent  # script lives in vault root
README_PATH = VAULT_ROOT / "README.md"

# Subject folder descriptions (add new subjects here as you expand)
SUBJECT_DESCRIPTIONS = {
    "1.Networking_Concepts_and_Cyber_Security": {
        "name": "Networking & Cyber Security",
        "emoji": "🔐",
        "topics": "CIA Triad · Threat Actors · Risk Assessment · Network Attacks · Malware · Defence in Depth · Ethical Hacking"
    },
    "2.Networking_Concepts_and_Cyber_Security_Tools": {
        "name": "Cyber Security Tools",
        "emoji": "🛠️",
        "topics": "Nmap · Wireshark · Maltego · Shodan · Metagoofil · theHarvester · Kali Linux"
    },
    "3.Digital_Technologies": {
        "name": "Digital Technologies",
        "emoji": "💻",
        "topics": "Hardware · OSI Model · Storage & RAID · Cloud Computing · AI/ML · DevOps"
    },
    "4.Cisco_Networking": {
        "name": "Cisco Networking",
        "emoji": "📡",
        "topics": "IOS Modes · DHCP · Device Security · VLANs · VTP · Troubleshooting"
    },
    "5.IP_Addressing": {
        "name": "IP Addressing & Subnetting",
        "emoji": "🌐",
        "topics": "IPv4 Classes · Subnetting · CIDR · Worked Examples"
    },
    "6.Software_Development_and_Application_Modelling": {
        "name": "Software Development & Application Modelling",
        "emoji": "🐍",
        "topics": "Python · Data Types · Control Flow · Functions · OOP"
    },
    "7.Web_Development_and_Operating_Systems": {
        "name": "Web Development & Operating Systems",
        "emoji": "🌍",
        "topics": "HTML · Static vs Dynamic · Linux CLI · File Permissions"
    },
}

# ── SCAN VAULT ────────────────────────────────────────────────
def scan_vault():
    """Scan all subject folders and return structured data."""
    subjects = []
    total_pdfs = 0

    for folder in sorted(VAULT_ROOT.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name.startswith('.') or folder.name == '__pycache__':
            continue

        pdfs = sorted([f for f in folder.iterdir() if f.suffix.lower() == '.pdf'])
        if not pdfs:
            continue

        desc = SUBJECT_DESCRIPTIONS.get(folder.name, {
            "name": folder.name.replace('_', ' ').replace('.', '. '),
            "emoji": "📁",
            "topics": "Various topics"
        })

        subjects.append({
            "folder": folder.name,
            "name": desc["name"],
            "emoji": desc["emoji"],
            "topics": desc["topics"],
            "files": [f.name for f in pdfs],
            "count": len(pdfs)
        })
        total_pdfs += len(pdfs)

    return subjects, total_pdfs


# ── BUILD README SECTIONS ─────────────────────────────────────
def build_directory_tree(subjects):
    lines = ["```", "open-study-vault/", "│"]
    for i, subj in enumerate(subjects):
        is_last = i == len(subjects) - 1
        connector = "└──" if is_last else "├──"
        lines.append(f"{connector} 📁 {subj['folder']}/")
        for j, f in enumerate(subj['files']):
            file_connector = "    └──" if j == len(subj['files']) - 1 else "    ├──"
            if is_last:
                file_connector = "    " + ("└──" if j == len(subj['files']) - 1 else "├──")
            lines.append(f"{file_connector} {f}")
        if not is_last:
            lines.append("│")
    lines.append("```")
    return "\n".join(lines)


def build_topics_table(subjects):
    lines = [
        "| # | Subject | Topics |",
        "|---|---------|--------|"
    ]
    for i, subj in enumerate(subjects, 1):
        num = str(i).zfill(2)
        lines.append(f"| {num} | {subj['emoji']} **{subj['name']}** | {subj['topics']} |")
    return "\n".join(lines)


def build_quick_access(subjects):
    """Auto-generate quick access links for all PDFs."""
    lines = [
        "| Note | Subject | Link |",
        "|------|---------|------|"
    ]
    for subj in subjects:
        for f in subj['files']:
            clean_name = f.replace('.pdf', '').replace('_', ' ').lstrip('0123456789. ')
            link = f"./{subj['folder']}/{f}"
            lines.append(f"| 📄 {clean_name} | {subj['emoji']} {subj['name']} | [Open PDF]({link}) |")
    return "\n".join(lines)


def build_badges(total_pdfs, subject_count):
    updated = datetime.now().strftime("%Y--%m--%d")
    return (
        f"![Status](https://img.shields.io/badge/status-active-brightgreen) "
        f"![Notes](https://img.shields.io/badge/notes-{total_pdfs}%20PDFs-blue) "
        f"![Subjects](https://img.shields.io/badge/subjects-{subject_count}-orange) "
        f"![Updated](https://img.shields.io/badge/updated-{updated}-lightgrey) "
        f"![Licence](https://img.shields.io/badge/licence-MIT-black)"
    )


# ── GENERATE FULL README ──────────────────────────────────────
def generate_readme(subjects, total_pdfs):
    updated = datetime.now().strftime("%B %d, %Y")
    directory_tree = build_directory_tree(subjects)
    topics_table = build_topics_table(subjects)
    quick_access = build_quick_access(subjects)
    badges = build_badges(total_pdfs, len(subjects))

    readme = f"""# 📂 open-study-vault

```
░█████╗░██████╗░███████╗███╗░░██╗  ░██████╗████████╗██╗░░░██╗██████╗░██╗░░░██╗
██╔══██╗██╔══██╗██╔════╝████╗░██║  ██╔════╝╚══██╔══╝██║░░░██║██╔══██╗╚██╗░██╔╝
██║░░██║██████╔╝█████╗░░██╔██╗██║  ╚█████╗░░░░██║░░░██║░░░██║██║░░██║░╚████╔╝░
██║░░██║██╔═══╝░██╔══╝░░██║╚████║  ░╚═══██╗░░░██║░░░██║░░░██║██║░░██║░░╚██╔╝░░
╚█████╔╝██║░░░░░███████╗██║░╚███║  ██████╔╝░░░██║░░░╚██████╔╝██████╔╝░░░██║░░░
░╚════╝░╚═╝░░░░░╚══════╝╚═╝░░╚══╝  ╚═════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░░░░╚═╝░░░

                         V A U L T
```

> *"The quieter you become, the more you are able to hear."* — Kali Linux

---

## 🔐 INITIALISING VAULT ACCESS...

```bash
$ whoami
  > student | learner | future-professional

$ cat mission.txt
  > Free, clean, community-driven study notes.
  > No paywalls. No gatekeeping. Just knowledge.

$ ls -la /vault
  > Cybersecurity · Networking · Python · Cloud · DevOps · Web · Linux
```

---

## 📡 ABOUT THIS VAULT

**open-study-vault** is a free, open collection of university-level study notes covering Computer Science and IT — rebuilt from scratch into clean, readable, exam-ready PDFs.

Every note in this vault is:
- ✅ **Rewritten** — not copy-pasted, fully restructured
- ✅ **Formatted** — tables, flowcharts, code blocks, key concept boxes
- ✅ **Detailed** — full explanations with real examples
- ✅ **Topic-split** — modular, easy to add to over time
- ✅ **Free** — always, forever

> Built for students, by a student. Contributions welcome.

---

## 🗂️ VAULT DIRECTORY

{directory_tree}

---

## 🧠 TOPICS COVERED

{topics_table}

---

## ⚡ QUICK ACCESS — ALL NOTES

{quick_access}

---

## 🛠️ BUILT WITH

```python
tools = {{
    "note_rewriting"  : "Claude AI (Anthropic)",
    "pdf_generation"  : "ReportLab (Python)",
    "version_control" : "Git + GitHub CLI",
    "source_format"   : "RemNote exports + lecture materials",
    "theme"           : "Professional Black & White",
    "structure"       : "Flowcharts · Tables · Code Blocks · Key Concepts",
}}
```

---

## 🤝 CONTRIBUTING

This vault grows with the community. If you want to add notes:

```bash
# 1. Fork this repo
# 2. Add your notes in the correct subject folder
# 3. Follow the naming convention: ##_Topic_Name.pdf
# 4. Submit a pull request with a short description
```

All subjects welcome — the vault has no limits.

---

## 📜 LICENCE

```
MIT Licence — free to use, share, and build upon.
All notes are original works. Not affiliated with any institution.
```

---

## 📊 VAULT STATUS

{badges}

*Last updated: {updated} — {total_pdfs} notes across {len(subjects)} subjects.*

---

<div align="center">

**⭐ Star this repo if it helped you — it helps others find it too.**

*More notes incoming. The vault is always open.*

</div>
"""
    return readme


# ── DETECT CHANGES ────────────────────────────────────────────
def detect_changes(subjects):
    """Compare current files against last known state."""
    state_file = VAULT_ROOT / ".vault_state"
    current_files = set()
    for subj in subjects:
        for f in subj['files']:
            current_files.add(f"{subj['folder']}/{f}")

    new_files = []
    if state_file.exists():
        previous_files = set(state_file.read_text().strip().splitlines())
        new_files = sorted(current_files - previous_files)
    
    # Save current state
    state_file.write_text("\n".join(sorted(current_files)))
    return new_files


# ── MAIN ──────────────────────────────────────────────────────
def main():
    print("\n🔍 Scanning vault...")
    subjects, total_pdfs = scan_vault()

    print(f"   Found {len(subjects)} subjects, {total_pdfs} PDFs total")

    # Detect new files
    new_files = detect_changes(subjects)
    if new_files:
        print(f"\n🆕 New files detected:")
        for f in new_files:
            print(f"   + {f}")
    else:
        print("   No new files since last update")

    # Generate and write README
    print("\n📝 Updating README.md...")
    readme_content = generate_readme(subjects, total_pdfs)
    README_PATH.write_text(readme_content, encoding='utf-8')
    print("   ✓ README.md updated successfully")

    # Summary
    print(f"\n{'='*50}")
    print(f"  ✅ Vault scan complete")
    print(f"  📁 Subjects : {len(subjects)}")
    print(f"  📄 Total PDFs: {total_pdfs}")
    if new_files:
        print(f"  🆕 New files : {len(new_files)}")
    print(f"{'='*50}")
    print("\n  Run these commands to push to GitHub:")
    print("  > git add .")
    print('  > git commit -m "Update vault — new notes added"')
    print("  > git push\n")


if __name__ == "__main__":
    main()
