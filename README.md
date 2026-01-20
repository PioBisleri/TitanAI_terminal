
### 🌌 TITAN AI TERMINAL | V1 Genesis Edition
![Python]([https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white))  
![License]([https://img.shields.io/badge/License-MIT-green?style=for-the-badge](https://img.shields.io/badge/License-MIT-green?style=for-the-badge))  
![Status]([https://img.shields.io/badge/System-Stable-00f2ea?style=for-the-badge](https://img.shields.io/badge/System-Stable-00f2ea?style=for-the-badge))  
![Platform]([https://img.shields.io/badge/Backend-llama.cpp-ff69b4?style=for-the-badge](https://img.shields.io/badge/Backend-llama.cpp-ff69b4?style=for-the-badge))
<div align="center">
████████╗██╗████████╗ █████╗ ███╗   ██╗
╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
   ██║   ██║   ██║   ███████║██╔██╗ ██║
   ██║   ██║   ██║   ██╔══██║██║╚██╗██║
   ██║   ██║   ██║   ██║  ██║██║ ╚████║
   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
   [V1 GENESIS EDITION | SYSTEM ONLINE]

</div>
> "Turn your terminal into a Cyberpunk RPG powered by Local AI."
> 
🚀 Introduction
Welcome to TITAN V1, a terminal-based productivity suite that doesn't just run commands—it gamifies your workflow.
Designed primarily for Android Termux (but running beautifully on Linux/macOS), TITAN turns your device into a personal deck. It combines a local Large Language Model (LLM) with a deep RPG progression system. Every task you complete earns you XP. Every day you login builds your streak. Your AI assistant isn't just a chatbot; it's a companion that knows your rank, your stats, and your history.
No internet required. No data leaving your device. Just you, the code, and the grid.
✨ Features
🧠 Neural Core (Local AI)
 * Offline Intelligence: Runs .gguf models (Llama 3, Mistral, Gemma) locally using llama.cpp.
 * RAG System: Drop .txt files into the documents/ folder, and TITAN will index them for context-aware answers.
 * Memory Bank: Persistent long-term memory allows the AI to remember facts about you across sessions.
⚔️ RPG Gamification
 * Progression: Level up from Initiate (Lvl 1) to Titan (Lvl 50+).
 * Stats: Track your HP (Health), Energy, and XP.
 * Daily Streaks: Maintain login streaks to earn bonus XP and heal your character.
🖥️ Cyberpunk TUI
 * Immersive Dashboard: Built with Rich, featuring animated boot sequences, health bars, and ASCII art.
 * Menu System: Navigate with arrow keys—no complex command memorization required.
 * Hacker Aesthetic: Streaming text responses and terminal-green visuals.
📜 Quest Log
 * Task Management: Create Main Quests, Side Quests, and Dailies.
 * Rewards: Completing tasks grants XP based on difficulty.
🛠️ Installation
Prerequisites
 * Python 3.10 or higher.
 * Android Users: You need Termux.
 * Desktop Users: Linux or macOS (Windows requires WSL).
1. Clone the Repository
git clone https://github.com/yourusername/titan-terminal.git
cd titan-terminal

2. Install Dependencies
TITAN relies on rich for visuals and llama-cpp-python for AI.
For Desktop (Linux/Mac):
pip install -r requirements.txt

For Android (Termux):
Compiling llama-cpp-python on mobile can be tricky. Run these commands:
pkg install clang cmake build-essential
CMAKE_ARGS="-DLLAMA_METAL=off" pip install llama-cpp-python
pip install rich questionary numpy

3. Download a Model
TITAN requires a GGUF format model.
 * Go to HuggingFace.
 * Download a small model (recommended: Llama-3-8B-Instruct-Q4_K_M.gguf or Phi-3-Mini-4k-Instruct.gguf).
 * Place the file inside the models/ folder.
<!-- end list -->
# Example directory structure
titan_terminal/
├── main.py
├── models/
│   └── llama-3-8b-instruct.gguf  <-- Put model here
├── documents/                    <-- Put .txt files here

🕹️ Usage
Run the entry script:
python main.py

Controls
 * Arrow Keys: Navigate menus.
 * Enter: Select option.
 * Chat Mode:
   * Type normally to chat.
   * /quest <task>: Add a new side quest.
   * /save <text>: Save a fact to long-term memory.
   * /exit: Return to main menu.
📸 Screenshots
<div align="center">
<img src="https://placehold.co/600x300/1a1a1a/00ff00?text=Dashboard+View" alt="Dashboard" width="45%">
<img src="https://placehold.co/600x300/1a1a1a/00ffff?text=Quest+Log" alt="Quest Log" width="45%">
</div>
🤝 Contributing
Got an idea to make TITAN better? Maybe a new RPG class? A calendar integration?
 * Fork the repo.
 * Create your feature branch (git checkout -b feature/AmazingFeature).
 * Commit your changes (git commit -m 'Add some AmazingFeature').
 * Push to the branch (git push origin feature/AmazingFeature).
 * Open a Pull Request.
📜 License
Distributed under the MIT License. See LICENSE for more information.
💜 Acknowledgments
 * Rich Library: For making terminals beautiful.
 * Llama.cpp: For making local AI possible.
 * You: For keeping the cyberpunk dream alive.
<div align="center">
<i>System Status: Online. // Operator: Unidentified. // End of Line. █</i>
</div>
