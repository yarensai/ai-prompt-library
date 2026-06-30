# 🧠 AI Prompt Library

A production-grade, version-controlled archive of AI System Instructions, Personas, and customized **Gemini Gems**. This repository treats AI prompts as structured, testable software artifacts using standardized **Markdown + YAML Frontmatter**.

---

## 🏗️ Repository Architecture

This repository uses a **Canonical + Archive Hybrid Pattern** to maintain clean discovery while preserving historical prompt iterations:

```text
ai-prompt-library/
├── models/
│   └── gemini-gems/               # Canonical prompt definitions (Always points to latest version)
│       ├── archive/               # Historical snapshots (e.g., v1.0.0, v2.0.0)
│       ├── hpc-expert.md          # Canonical file (Current: v4.0.0)
│       ├── it-expert.md           # Canonical file (Current: v3.0.0)
│       └── ...
├── scripts/
│   ├── convert_takeout_to_gems.py # Parser for Google Takeout HTML/JSON exports
│   └── consolidate_versions.py    # Automated semantic versioning and consolidation script
└── README.md
```

---

## 💎 Canonical Prompt Catalog (`models/gemini-gems/`)

Below is the directory index of active canonical prompts available in this library:

| Prompt / Persona | Domain Focus | Current Version |
| :--- | :--- | :--- |
| **[HPC Expert](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/hpc-expert.md)** | Bare-metal hardware, Slurm/MPI, Lustre/GPFS, cluster automation | `v4.0.0` |
| **[IT Expert](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/it-expert.md)** | Enterprise system administration, network topology, cloud infrastructure | `v3.0.0` |
| **[Tech Troubleshooter](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/tech-troubleshooter.md)** | Deep diagnostic debugging, log analysis, root cause resolution | `v3.0.0` |
| **[Prompt Engineer](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/prompt-engineer.md)** | Advanced prompt design, LLM agent architecture, RAG optimization | `v2.0.0` |
| **[IT Architect](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/it-architect.md)** | Enterprise cloud design, Zero Trust security, distributed systems | `v2.0.0` |
| **[Master Tianji](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/master-tianji.md)** | Strategic analysis and ancient wisdom framework | `v2.0.0` |
| **[Cyber Security](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/cyber-security.md)** | Threat hunting, vulnerability mitigation, DevSecOps practices | `v1.0.0` |
| **[Automation Architect](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/automation-architect.md)** | Infrastructure-as-Code (IaC), CI/CD pipelines, enterprise scripting | `v1.0.0` |
| **[Quantitative Architect](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/quantitative-architect.md)** | Algorithmic trading infrastructure, high-frequency execution engines | `v1.0.0` |
| **[Software Engineer](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/software-engineer.md)** | Full-stack architecture, clean code principles, system design | `v1.0.0` |
| **[Robotic Engineer](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/robotic-engineer.md)** | ROS, embedded systems, kinematics, IoT automation | `v1.0.0` |
| **[Pine Script Developer](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/pine-script-developer.md)** | TradingView custom indicators and automated trading strategy design | `v1.0.0` |
| **[Data Engineering Architect](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/lead-data-analyst-data-engineering-architect.md)** | Big data pipelines, ETL/ELT optimization, data warehousing | `v1.0.0` |
| **[Linux Script Developer](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/linux-script-developer.md)** | Advanced Bash/Shell utilities, kernel tuning, cron workflows | `v1.0.0` |
| **[First Principles Architect](file:///wsl.localhost/Ubuntu-24.04/home/yungcuan/ai-prompt-library/models/gemini-gems/first-principles-architect.md)** | Deconstructing complex engineering problems from ground truth | `v1.0.0` |

---

## 📜 Standard Prompt Schema

All prompts follow a structured **YAML Frontmatter** metadata block followed by standard Markdown instruction headers:

```markdown
---
name: "Expert Persona Name"
description: "High-level summary of the persona's core function."
version: "1.0.0"
date_imported: "2026-07-01"
---

## Identity & Instructions

Detailed system prompt, knowledge boundaries, operating rules, and guardrails.
```

---

## 🛠️ Automation Tooling

This repository comes equipped with custom automation scripts located in `scripts/`:

### 1. Extracting Gems from Google Takeout
If you create new custom Gems in the Google Gemini web interface, export them via [Google Takeout](https://takeout.google.com/) and run the parser:

```bash
python3 scripts/convert_takeout_to_gems.py --input /path/to/Takeout/Gemini --output models/gemini-gems
```
*Parses both HTML (`gemini_gems_data.html`) and JSON exports into formatted markdown files.*

### 2. Consolidating Versions
If multiple files exist with version suffixes (e.g., `hpc-expert-v4.md` and `hpc-expert-v2.md`), run the consolidation utility to promote the latest version to canonical status and archive older snapshots:

```bash
python3 scripts/consolidate_versions.py --dir models/gemini-gems
```

---

## 🔄 Version Control Best Practices

When modifying existing prompts:
1. **Edit the Canonical File Directly**: Do not create a new file named `my-prompt-v2.md`. Instead, update `models/gemini-gems/my-prompt.md`.
2. **Bump the YAML Version**: Increment the `version: "X.Y.Z"` string inside the file's frontmatter.
3. **Commit with Descriptive Messages**:
   ```bash
   git add models/gemini-gems/my-prompt.md
   git commit -m "feat(hpc-expert): add slurm memory binding guardrails to v4.1.0"
   git push origin main
   ```
