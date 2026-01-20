from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time

console = Console()

ASCII_ART = """
[bold cyan]
████████╗██╗████████╗ █████╗ ███╗   ██╗
╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
   ██║   ██║   ██║   ███████║██╔██╗ ██║
   ██║   ██║   ██║   ██╔══██║██║╚██╗██║
   ██║   ██║   ██║   ██║  ██║██║ ╚████║
   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
[/bold cyan][dim]   V1 GENESIS EDITION | SYSTEM ONLINE[/dim]
"""

def boot_sequence():
    console.clear()
    console.print(Align.center(ASCII_ART))
    time.sleep(0.5)
    steps = ["Initializing Kernel", "Loading User Profile", "Mounting RAG Systems"]
    
    with Progress(
        SpinnerColumn("dots", style="cyan"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=None, style="blue", complete_style="cyan"),
        console=console,
        transient=True
    ) as p:
        task = p.add_task("Booting...", total=100)
        for _ in range(100):
            time.sleep(0.01)
            p.update(task, advance=1)
            if _ % 33 == 0 and steps: 
                p.update(task, description=steps.pop(0))

def draw_dashboard(rpg, quests, model_name, doc_count):
    console.clear()
    
    # Calc XP
    xp_req = rpg.get_next_level_xp()
    xp_pct = (rpg.stats['xp'] / xp_req) * 100
    
    # User Panel
    user_panel = Table.grid(expand=True)
    user_panel.add_column()
    user_panel.add_row(f"[bold white]{rpg.stats['rank']}[/] | Lvl {rpg.stats['level']}")
    
    hp_bar = "█" * int((rpg.stats['hp']/rpg.stats['max_hp'])*20)
    xp_bar = "━" * int((xp_pct/100)*20)
    
    user_panel.add_row(f"[red]HP: {rpg.stats['hp']}/{rpg.stats['max_hp']} {hp_bar}[/]")
    user_panel.add_row(f"[yellow]XP: {int(rpg.stats['xp'])}/{int(xp_req)} {xp_bar}[/]")
    
    # Quest Snippet
    active_q = [q for q in quests.quests if q['status'] == "active"]
    q_txt = f"[bold cyan]![/] {active_q[0]['title']}" if active_q else "[dim]No active directives.[/]"
    if len(active_q) > 1: q_txt += f" [dim](+{len(active_q)-1} more)[/]"

    layout = Table.grid(expand=True)
    layout.add_row(
        Panel(user_panel, title="[bold cyan]OPERATOR STATUS[/]", border_style="cyan"),
        Panel(f"Model: {model_name}\nDocs: {doc_count}", title="[bold cyan]SYSTEM[/]", border_style="blue")
    )
    
    console.print(layout)
    console.print(Panel(q_txt, title="CURRENT OBJECTIVE", border_style="white", style="italic"))
    console.print()
