import sys
import time
import questionary
from rich.panel import Panel
from rich.table import Table
from src.config import Config
from src.rpg import RPGSystem, QuestSystem
from src.ai import NeuralCore
from src.ui import console, draw_dashboard, boot_sequence
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
                choices=["💬 Neural Chat", "📜 Quest Log", "🔌 Load Model", "❌ Shutdown"],
                style=questionary.Style([('answer', 'fg:cyan bold')])
            ).ask()

            if action == "❌ Shutdown": sys.exit(0)
            elif action == "🔌 Load Model": self.menu_load_model()
            elif action == "📜 Quest Log": self.menu_quests()
            elif action == "💬 Neural Chat": self.menu_chat()

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

    def menu_quests(self):
        # (Simplified Quest UI logic here - similar to original script)
        # Use self.quests.add_quest / complete
        pass

    def menu_chat(self):
        if not self.core.llm:
            console.print("[red]⚠️ Neural Link Offline (Load Model First)[/]")
            time.sleep(2)
            return

        console.clear()
        console.print(Panel("Chat Active. Type /exit to return.", style="blue"))

        while True:
            try:
                user_in = console.input("\n[bold green]OP ➤ [/]").strip()
                if not user_in: continue
                if user_in == "/exit": break
                
                # Context Build
                rag_txt = self.core.search(user_in)
                mem_txt = "\n".join([m['text'] for m in self.core.ltm])
                
                sys_prompt = f"""You are Titan V1.
                [USER] Rank: {self.rpg.stats['rank']}
                [MEMORY] {mem_txt}
                [DATA] {rag_txt}"""

                console.print(f"[bold cyan]V1 ➤ [/]", end="")
                for chunk in self.core.chat_stream(user_in, sys_prompt):
                    print(chunk, end="", flush=True)
                print()
                
            except KeyboardInterrupt: break
