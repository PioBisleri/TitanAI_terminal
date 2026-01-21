from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box
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
[/bold cyan][dim]   V1.1 NEURAL EDITION | SYSTEM ONLINE[/dim]
"""

def boot_sequence():
    console.clear()
    console.print(Align.center(ASCII_ART))
    time.sleep(0.5)
    steps = ["Initializing Kernel", "Loading User Profile", "Mounting RAG Systems", "Syncing Neural Cortex"]
    
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
            if _ % 25 == 0 and steps: 
                p.update(task, description=steps.pop(0))

def draw_dashboard(rpg, quests, model_name, doc_count):
    console.clear()
    
    # --- Calc Stats ---
    xp_req = rpg.get_next_level_xp()
    xp_pct = (rpg.stats['xp'] / xp_req) * 100
    
    # --- User Panel ---
    user_grid = Table.grid(expand=True)
    user_grid.add_column()
    
    # Top Row: Rank | Level | SP
    user_grid.add_row(
        f"[bold white]{rpg.stats['rank']}[/] | Lvl {rpg.stats['level']} | [bold yellow]SP: {rpg.stats['sp']}[/]"
    )
    
    # Health Bar
    hp_pct = rpg.stats['hp'] / rpg.stats['max_hp']
    hp_blocks = "█" * int(hp_pct * 20)
    hp_color = "green" if hp_pct > 0.5 else "red"
    user_grid.add_row(f"[{hp_color}]HP: {int(rpg.stats['hp'])}/{int(rpg.stats['max_hp'])} {hp_blocks}[/]")

    # Energy Bar
    en_pct = rpg.stats['energy'] / rpg.stats['max_energy']
    en_blocks = "█" * int(en_pct * 20)
    user_grid.add_row(f"[blue]EN: {int(rpg.stats['energy'])}/{int(rpg.stats['max_energy'])} {en_blocks}[/]")

    # XP Bar
    xp_blocks = "━" * int((xp_pct/100)*20)
    user_grid.add_row(f"[yellow]XP: {int(rpg.stats['xp'])}/{int(xp_req)} {xp_blocks}[/]")
    
    # --- Quest Snippet ---
    active_q = [q for q in quests.quests if q['status'] == "active"]
    q_txt = f"[bold cyan]![/] {active_q[0]['title']}" if active_q else "[dim]No active directives.[/]"
    if len(active_q) > 1: q_txt += f" [dim](+{len(active_q)-1} more)[/]"

    # --- Main Layout ---
    layout = Table.grid(expand=True)
    layout.add_row(
        Panel(user_grid, title="[bold cyan]OPERATOR STATUS[/]", border_style="cyan"),
        Panel(f"Model: {model_name}\nDocs: {doc_count}\nRAM: Stable", title="[bold cyan]SYSTEM[/]", border_style="blue")
    )
    
    console.print(layout)
    console.print(Panel(q_txt, title="CURRENT OBJECTIVE", border_style="white", style="italic"))
    console.print()

def draw_skill_tree(rpg):
    console.clear()
    
    # Header
    console.print(Panel(f"[bold]NEURAL UPGRADES[/]\nAvailable Skill Points (SP): [bold yellow]{rpg.stats['sp']}[/]", style="magenta"))
    
    # Tree Structure
    tree = Tree("📂 [bold white]CORTEX ROOT[/]")
    
    for sid, meta in rpg.SKILLS.items():
        curr = rpg.get_skill_level(sid)
        max_lvl = meta['max']
        cost = meta['cost']
        
        # Determine Color/Status
        if curr >= max_lvl:
            style = "dim green"
            status = "[MAXED]"
            icon = "🔒"
        elif rpg.stats['sp'] >= cost:
            style = "bold cyan"
            status = f"[UPGRADE: {cost} SP]"
            icon = "🔓"
        else:
            style = "dim white"
            status = f"[LOCKED: {cost} SP]"
            icon = "🔒"
            
        # Add Node
        label = f"{icon} [{style}]{meta['name']} (Rank {curr}/{max_lvl})[/]\n   [dim]└─ {meta['desc']} {status}[/]"
        tree.add(label)
        
    console.print(tree)
    console.print()

