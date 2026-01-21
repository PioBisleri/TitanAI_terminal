import sys
import time
import questionary
from rich.panel import Panel
from rich.table import Table
from rich import box

# Internal Module Imports
from src.config import Config
from src.rpg import RPGSystem, QuestSystem
from src.ai import NeuralCore
from src.ui import console, draw_dashboard, boot_sequence, draw_skill_tree
from src.utils import suppress_c_logs

class TitanTerminal:
    def __init__(self):
        suppress_c_logs()
        self.cfg = Config()
        self.rpg = RPGSystem(self.cfg)
        self.quests = QuestSystem(self.cfg, self.rpg)
        self.core = NeuralCore(self.cfg)

    def run(self):
        boot_sequence()
        while True:
            draw_dashboard(self.rpg, self.quests, self.core.model_name, len(self.core.rag_chunks))
            
            action = questionary.select(
                "SELECT MODULE:",
                choices=[
                    "💬 Neural Chat",
                    "📜 Quest Log",
                    "🧠 Memory Bank",
                    "🧬 Neural Upgrades",
                    "🔌 Load Model",
                    "⚙️ Settings",
                    "❌ Shutdown"
                ],
                style=questionary.Style([('answer', 'fg:cyan bold')])
            ).ask()

            if action == "❌ Shutdown": sys.exit(0)
            elif action == "🔌 Load Model": self.menu_load_model()
            elif action == "💬 Neural Chat": self.menu_chat()
            elif action == "📜 Quest Log": self.menu_quests()
            elif action == "🧠 Memory Bank": self.menu_memory()
            elif action == "🧬 Neural Upgrades": self.menu_skills()
            elif action == "⚙️ Settings": self.menu_settings()

    # --- 🧠 MEMORY BANK ---
    def menu_memory(self):
        while True:
            console.clear()
            mem_text = "\n".join([f"• {m['text']}" for m in self.core.ltm]) if self.core.ltm else "[dim]No long-term data found.[/dim]"
            
            console.print(Panel(mem_text, title="[bold magenta]LONG TERM MEMORY STORAGE[/]", border_style="magenta"))
            
            act = questionary.select("Memory Action:", choices=["Inject New Data", "Clear Last Entry", "Back"]).ask()
            
            if act == "Back": break
            elif act == "Inject New Data":
                t = questionary.text("Enter Fact/Data:").ask()
                if t: 
                    self.core.ltm.append({"text": t, "ts": time.time()})
                    self.core._save_mem()
                    console.print("[green]Data written to core.[/]")
                    time.sleep(1)
            elif act == "Clear Last Entry":
                if self.core.ltm:
                    self.core.ltm.pop()
                    self.core._save_mem()
                    console.print("[yellow]Last entry wiped.[/]")
                    time.sleep(1)

    # --- ⚙️ SETTINGS MENU ---
    def menu_settings(self):
        while True:
            console.clear()
            console.print(Panel("[bold]SYSTEM CONFIGURATION[/]", style="white"))
            
            c = self.cfg.data
            console.print(f"Temperature: {c['temperature']}")
            console.print(f"Context Win: {c['n_ctx']}")
            console.print(f"Threads:     {c['n_threads']}")
            console.print(f"RAG Enabled: {c['rag_enabled']}")
            console.print("-" * 20)

            opt = questionary.select("Modify Parameter:", 
                choices=["Set Temperature", "Set Context Window", "Set Thread Count", "Toggle RAG", "Back"]
            ).ask()

            if opt == "Back": break
            
            elif opt == "Set Temperature":
                try:
                    val = float(questionary.text("Value (0.1 - 1.5):", default=str(c['temperature'])).ask())
                    self.cfg.update('temperature', val)
                except: console.print("[red]Invalid Number[/]")

            elif opt == "Set Context Window":
                val = questionary.select("Size:", choices=["2048", "4096", "8192"]).ask()
                self.cfg.update('n_ctx', int(val))
                console.print("[yellow]Restart required to apply context changes.[/]")
                time.sleep(2)

            elif opt == "Set Thread Count":
                try:
                    val = int(questionary.text("Threads (1-8):", default=str(c['n_threads'])).ask())
                    self.cfg.update('n_threads', val)
                    console.print("[yellow]Restart required to apply thread changes.[/]")
                    time.sleep(2)
                except: console.print("[red]Invalid Number[/]")  # <--- FIXED: Added missing except block

            elif opt == "Toggle RAG":
                self.cfg.update('rag_enabled', not c['rag_enabled'])

    # --- 🧬 SKILL TREE ---
    def menu_skills(self):
        while True:
            draw_skill_tree(self.rpg)
            choices = []
            for sid, meta in self.rpg.SKILLS.items():
                curr = self.rpg.get_skill_level(sid)
                if curr < meta['max']:
                    choices.append(f"{meta['name']} ({meta['cost']} SP)")
            
            choices.append("Back")
            sel = questionary.select("Select Upgrade Module:", choices=choices).ask()
            
            if sel == "Back": break
            
            target_name = sel.split(" (")[0]
            target_id = next(k for k, v in self.rpg.SKILLS.items() if v['name'] == target_name)
            
            self.rpg.unlock_skill(target_id)
            time.sleep(1.5)

    # --- 🔌 LOAD MODEL ---
    def menu_load_model(self):
        m_dir = self.cfg.root / self.cfg.data['models_dir']
        models = list(m_dir.glob("*.gguf"))
        if not models:
            console.print("[red]No .gguf models found in /models[/]")
            time.sleep(2)
            return

        sel = questionary.select("Select Model:", choices=[m.name for m in models] + ["Back"]).ask()
        if sel == "Back": return
        
        path = next(m for m in models if m.name == sel)
        console.print(f"[cyan]Initializing {sel}...[/]")
        
        res = self.core.load_model(path)
        if res is True:
            console.print("[green]System Ready.[/]")
        else:
            console.print(f"[red]Error: {res}[/]")
        time.sleep(1)

    # --- 📜 QUESTS ---
    def menu_quests(self):
        while True:
            console.clear()
            console.print(Panel("[bold]MISSION LOG[/]", style="cyan"))
            active = [q for q in self.quests.quests if q['status'] == "active"]
            
            table = Table(box=box.SIMPLE)
            table.add_column("Type", width=12)
            table.add_column("Mission")
            table.add_column("Reward", justify="right")
            
            for q in active:
                c = "yellow" if q['category'] == "Main Quest" else "white"
                table.add_row(f"[{c}]{q['category']}[/]", q['title'], f"{q['reward']} XP")
            
            console.print(table)
            
            act = questionary.select("Action:", choices=["Add Mission", "Complete Mission", "Back"]).ask()
            if act == "Back": break
            elif act == "Add Mission":
                cat = questionary.select("Type:", choices=["Main Quest", "Side Quest", "Daily"]).ask()
                title = questionary.text("Objective:").ask()
                if title: self.quests.add_quest(title, cat)
            elif act == "Complete Mission":
                if not active: continue
                sel = questionary.select("Complete:", choices=[q['title'] for q in active]).ask()
                if sel: 
                    self.quests.complete(sel)
                    console.print("[bold green]MISSION ACCOMPLISHED[/]")
                    time.sleep(1)

    # --- 💬 CHAT ---
    def menu_chat(self):
        if not self.core.llm:
            console.print("[red]⚠️ Neural Link Offline (Load Model First)[/]")
            time.sleep(2)
            return

        console.clear()
        console.print(Panel("Chat Active. Type /exit to return, /quest <txt> to add task.", style="blue"))

        while True:
            try:
                user_in = console.input("\n[bold green]OP ➤ [/]").strip()
                if not user_in: continue
                if user_in == "/exit": break
                
                # Chat Commands
                if user_in.startswith("/quest "):
                    self.quests.add_quest(user_in[7:], "Side Quest")
                    continue
                if user_in.startswith("/save "):
                    self.core.ltm.append({"text": user_in[6:], "ts": time.time()})
                    self.core._save_mem()
                    console.print("[dim]Memory saved.[/]")
                    continue

                # Context Build
                rag_txt = self.core.search(user_in)
                mem_txt = "\n".join([m['text'] for m in self.core.ltm])
                
                # Dynamic System Prompt
                sys_prompt = f"""You are Titan V1.
                [USER STATS] Rank: {self.rpg.stats['rank']} | Energy: {self.rpg.stats['energy']}
                [MEMORY] {mem_txt}
                [DATA] {rag_txt}
                """

                console.print(f"[bold cyan]V1 ➤ [/]", end="")
                for chunk in self.core.chat_stream(user_in, sys_prompt):
                    print(chunk, end="", flush=True)
                print()
                
            except KeyboardInterrupt: break
