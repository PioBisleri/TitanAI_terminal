# 🌌 TITAN AI TERMINAL

```
████████╗██╗████████╗ █████╗ ███╗   ██╗
╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
   ██║   ██║   ██║   ███████║██╔██╗ ██║
   ██║   ██║   ██║   ██╔══██║██║╚██╗██║
   ██║   ██║   ██║   ██║  ██║██║ ╚████║
   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
```

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-purple?style=for-the-badge&logo=github)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Termux Compatible](https://img.shields.io/badge/termux-compatible-green?style=for-the-badge&logo=android)](https://termux.com/)
[![Local AI](https://img.shields.io/badge/local--ai-llama.cpp-orange?style=for-the-badge&logo=cpu)](https://github.com/ggerganov/llama.cpp)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=git)](CONTRIBUTING.md)

**Version 1.1 Neural Edition**

*Evolve your workflow. Gamify your terminal. Own your data.*

[Features](#-features) • [Installation](#%EF%B8%8F-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

TITAN is a privacy-first terminal assistant that combines local AI with RPG-style progression mechanics. Designed for Termux (Android) and Linux environments, it transforms your command-line workflow into an engaging, gamified experience while keeping all your data completely offline.

### Why TITAN?

- **🎮 Gamified Productivity** - Earn XP for tasks, maintain streaks, and level up your terminal skills
- **🧠 Local AI** - Run powerful language models offline using llama.cpp
- **🔒 Privacy First** - Zero data leaves your device. All memories, stats, and conversations stay local
- **🌳 Skill Tree System** - Unlock permanent upgrades like CPU Overclock and Active Firewall
- **📚 Knowledge Base** - Built-in RAG system indexes your documents for instant AI-powered retrieval

---

## ✨ Features

### 🧠 Neural Core (Local AI)

- **Offline Intelligence** - Runs GGUF models (Llama 3, Mistral, Phi-3) via llama.cpp
- **RAG System** - Drop `.txt` files into `documents/` for automatic knowledge indexing
- **Memory Bank** - Manage long-term memories (LTM) through dedicated menu interface
- **Contextual Awareness** - AI maintains conversation history and user preferences

### 🧬 Neural Upgrades (Skill Tree)

Earn **Skill Points (SP)** by leveling up and unlock powerful perks:

| Upgrade | Effect | Cost |
|---------|--------|------|
| **CPU Overclock** | +10% XP from chats (stackable to Rank 5) | 1 SP per rank |
| **Kernel Hardening** | Increases maximum HP | 2 SP |
| **Active Firewall** | Protects login streak if you miss a day | 5 SP |
| **Data Mining** | Boosts XP rewards from completed quests | 3 SP |

### ⚔️ RPG Progression

- **Character Stats** - Track HP (Health), Energy, and XP
- **Ranking System** - Progress from Initiate (Lvl 1) → Titan (Lvl 50) → Construct (Lvl 99)
- **Daily Streaks** - Login rewards heal your character and grant bonus XP
- **Quest System** - Create and complete Main Quests, Side Quests, and Dailies

### ⚙️ Advanced Configuration

- **Dynamic Settings** - Adjust temperature, context window (2k/4k/8k), and thread count
- **Model Management** - Easy switching between different GGUF models
- **Performance Tuning** - Optimize AI responses for your hardware

---

## 🛠️ Installation

### Prerequisites

| Platform | Requirements |
|----------|-------------|
| **Android** | Termux (F-Droid version recommended) |
| **Linux/macOS** | Python 3.10+, build-essential, cmake |
| **Windows** | WSL2 with Ubuntu 22.04+ |

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/titan-terminal.git
cd titan-terminal

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create necessary directories
mkdir -p models documents data

# 4. Download a GGUF model (example: Phi-3 Mini)
# Place it in the models/ folder
```

### Platform-Specific Setup

#### Termux (Android)

```bash
# Install system dependencies
pkg update && pkg upgrade
pkg install clang cmake python rust git

# Install Python packages (disable CUDA for mobile)
CMAKE_ARGS="-DLLAMA_CUBLAS=off" pip install -r requirements.txt
```

#### Linux/macOS

```bash
# Ensure build tools are installed
sudo apt-get install build-essential cmake  # Ubuntu/Debian
# or
brew install cmake  # macOS

pip install -r requirements.txt
```

### Recommended Models

Download one of these GGUF models and place it in `models/`:

- **Phi-3 Mini** (3.8GB) - Best for mobile/low-resource systems
- **Llama 3 8B** (4.7GB) - Balanced performance
- **Mistral 7B** (4.1GB) - Great for general tasks

Find models at [Hugging Face](https://huggingface.co/models?search=gguf)

---

## 🎮 Usage

### Starting TITAN

```bash
python main.py
```

### Navigation

#### Main Menu
- Use **↑/↓ arrow keys** to navigate
- Press **Enter** to select
- Press **Esc** or **q** to exit

#### Chat Mode Commands

| Command | Description |
|---------|-------------|
| `/quest <task>` | Create a new quest |
| `/save <fact>` | Store information in memory bank |
| `/memory` | View stored memories |
| `/stats` | Display character stats |
| `/exit` | Return to main menu |

### Example Workflow

```
1. Start TITAN → Main Menu appears
2. Select "Chat with AI" → Neural Core initializes
3. Ask questions or give commands
4. Complete tasks to earn XP
5. Level up → Earn Skill Points
6. Visit Skill Tree → Unlock upgrades
7. Maintain daily login streak for bonuses
```

---

## 📁 Project Structure

```
titan-terminal/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── app.py            # Main application logic
│   ├── rpg.py            # Leveling & skill systems
│   ├── ai.py             # RAG & neural core
│   └── ui.py             # Rich TUI components
│
├── models/               # GGUF model files (.gitignore'd)
│   └── .gitkeep
│
├── documents/            # RAG knowledge base
│   └── .gitkeep
│
└── data/                 # User save data
    ├── stats.json        # Character progression
    ├── memory.json       # Long-term memory
    └── quests.json       # Quest log
```

---

## 🧬 Skill Tree Preview

```
📂 CORTEX ROOT
│
├── 🔓 CPU Overclock (Rank 0/5)
│   ├─ Effect: +10% Chat XP per rank
│   └─ Cost: 1 SP per rank
│
├── 🔒 Active Firewall (Rank 0/1)
│   ├─ Effect: Protects streak if you miss 1 day
│   ├─ Cost: 5 SP
│   └─ Requires: Level 10
│
├── 🔒 Kernel Hardening (Rank 0/3)
│   ├─ Effect: +20 Max HP per rank
│   └─ Cost: 2 SP per rank
│
└── 🔒 Data Mining (Rank 0/3)
    ├─ Effect: +15% Quest XP per rank
    ├─ Cost: 3 SP per rank
    └─ Requires: Level 15
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how to get involved:

### Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/titan-terminal.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** and commit: `git commit -m 'Add amazing feature'`
5. **Push** to your fork: `git push origin feature/amazing-feature`
6. **Open a Pull Request** with a clear description

### Contribution Ideas

- 🎨 New skill tree upgrades
- 🤖 Additional AI model integrations
- 📊 Enhanced statistics tracking
- 🎮 New quest types and mechanics
- 🐛 Bug fixes and performance improvements
- 📚 Documentation improvements

### Guidelines

- Follow existing code style and structure
- Add tests for new features when possible
- Update documentation for user-facing changes
- Include `.gitkeep` files when adding empty directories
- Test on Termux if modifying Android-specific code

---

## 🐛 Troubleshooting

### Common Issues

**Model not loading**
- Ensure the `.gguf` file is in the `models/` directory
- Check file permissions: `chmod +r models/*.gguf`
- Verify model compatibility with llama.cpp

**Low performance on mobile**
- Reduce context window in Settings
- Lower thread count to 2-4
- Use smaller quantized models (Q4_K_M or smaller)

**Memory errors**
- Close background apps to free RAM
- Use smaller models (Phi-3 Mini recommended for <6GB RAM)
- Reduce context window size

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💜 Acknowledgments

- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal formatting
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** - Efficient local LLM inference
- **[Termux](https://termux.com/)** - Linux environment for Android
- **The open-source community** - For making privacy-respecting AI accessible

---

<div align="center">

**SYSTEM STATUS: ONLINE • NEURAL CORE: ACTIVE • V1.1 GENESIS**

Made with 💜 by the TITAN community

[Report Bug](https://github.com/yourusername/titan-terminal/issues) • [Request Feature](https://github.com/yourusername/titan-terminal/issues) • [Documentation](https://github.com/yourusername/titan-terminal/wiki)

</div>
