import json
import time
from datetime import datetime
from src.ui import console

class RPGSystem:
    RANKS = {
        1: "Initiate", 5: "Scout", 10: "Operative", 
        20: "Vanguard", 35: "Commander", 50: "Titan", 
        75: "Cyborg", 99: "Construct"
    }

    # --- 🧬 SKILL TREE ---
    SKILLS = {
        # TIER 1
        "cpu_overclock": {
            "name": "CPU Overclock", "cost": 1, "max": 5, 
            "desc": "+10% Chat XP per rank"
        },
        "kernel_hardening": {
            "name": "Kernel Hardening", "cost": 1, "max": 5, 
            "desc": "+15 Max HP per rank"
        },
        # TIER 2
        "ram_expansion": {
            "name": "RAM Expansion", "cost": 2, "max": 3, 
            "desc": "+20 Max Energy per rank"
        },
        "data_mining": {
            "name": "Data Mining", "cost": 2, "max": 3, 
            "desc": "+15% Bonus XP from Quests"
        },
        # TIER 3
        "firewall": {
            "name": "Active Firewall", "cost": 5, "max": 1, 
            "desc": "Protects Streak if you miss 1 day"
        },
        "neural_plasticity": {
            "name": "Neural Plasticity", "cost": 5, "max": 1, 
            "desc": "Unlocks Creative Temperature Controls"
        }
    }

    def __init__(self, config):
        self.path = config.get_path('user')
        self.stats = {
            "level": 1, "xp": 0, "sp": 0, "streak": 0,
            "last_login": None, "rank": "Initiate",
            "hp": 100, "max_hp": 100, "energy": 100, "max_energy": 100,
            "skills": {} 
        }
        self.load()
        self.process_login()

    def add_xp(self, amount, reason="Unknown"):
        # Skill: CPU Overclock (Bonus XP)
        if "Chat" in reason:
            bonus = self.get_skill_level("cpu_overclock") * 0.10
            amount = int(amount * (1 + bonus))

        self.stats['xp'] += amount
        console.print(f"[bold green]✨ +{amount} XP[/] [dim]({reason})[/]")
        
        req = self.get_next_level_xp()
        if self.stats['xp'] >= req:
            self._level_up(req)
        self.save()

    def _level_up(self, req):
        self.stats['level'] += 1
        self.stats['xp'] -= req
        self.stats['sp'] += 1 
        self._recalc_stats()
        self.stats['hp'] = self.stats['max_hp']
        self._update_rank()
        console.print(f"[bold yellow]⚡ LEVEL UP! Rank: {self.stats['rank']} (+1 SP)[/]")

    def unlock_skill(self, skill_id):
        if skill_id not in self.SKILLS: return False
        
        meta = self.SKILLS[skill_id]
        current_rank = self.stats['skills'].get(skill_id, 0)
        
        if current_rank >= meta['max']:
            console.print("[red]Skill Maxed Out![/]")
            return False
        
        if self.stats['sp'] >= meta['cost']:
            self.stats['sp'] -= meta['cost']
            self.stats['skills'][skill_id] = current_rank + 1
            self._recalc_stats()
            self.save()
            console.print(f"[bold cyan]Upgrade Installed: {meta['name']} (Rank {current_rank + 1})[/]")
            return True
        else:
            console.print("[red]Insufficient Skill Points[/]")
            return False

    def get_skill_level(self, skill_id):
        return self.stats['skills'].get(skill_id, 0)

    def _recalc_stats(self):
        base_hp = 100 + (self.stats['level'] * 5)
        base_energy = 100
        
        hp_bonus = self.get_skill_level("kernel_hardening") * 15
        en_bonus = self.get_skill_level("ram_expansion") * 20
        
        self.stats['max_hp'] = base_hp + hp_bonus
        self.stats['max_energy'] = base_energy + en_bonus

    def get_next_level_xp(self):
        return (self.stats['level'] * 150) + (self.stats['level'] ** 2 * 20)

    def _update_rank(self):
        current = "Initiate"
        for lvl, name in sorted(self.RANKS.items()):
            if self.stats['level'] >= lvl: current = name
        self.stats['rank'] = current

    def process_login(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if self.stats['last_login'] != today:
            if self.stats['last_login']:
                last = datetime.strptime(self.stats['last_login'], "%Y-%m-%d")
                diff = (datetime.now() - last).days
                
                if diff == 1:
                    self.stats['streak'] += 1
                    console.print(f"[bold green]🔥 STREAK: {self.stats['streak']} DAYS[/]")
                elif diff > 1:
                    # Skill: Firewall (Save Streak)
                    if self.get_skill_level("firewall") > 0 and diff == 2:
                         console.print("[bold yellow]🛡️ FIREWALL ACTIVE: Streak Saved![/]")
                    else:
                        self.stats['streak'] = 1
                        console.print("[red]💔 STREAK LOST[/]")
            else:
                self.stats['streak'] = 1
            
            self.stats['last_login'] = today
            self.stats['hp'] = self.stats['max_hp']
            self.stats['energy'] = self.stats['max_energy']
            self.add_xp(50, "Daily Login")
            self.save()

    def load(self):
        if self.path.exists():
            with open(self.path) as f: self.stats.update(json.load(f))
    
    def save(self):
        with open(self.path, 'w') as f: json.dump(self.stats, f)

class QuestSystem:
    def __init__(self, config, rpg):
        self.path = config.get_path('quests')
        self.rpg = rpg
        self.quests = []
        if self.path.exists(): self.quests = json.load(open(self.path))

    def add_quest(self, title, category="Side Quest"):
        xp_map = {"Main Quest": 200, "Side Quest": 100, "Daily": 50}
        self.quests.append({
            "id": int(time.time()),
            "title": title,
            "category": category,
            "reward": xp_map.get(category, 50),
            "status": "active"
        })
        self.save()
        console.print(f"[cyan]New Objective: {title}[/]")

    def complete(self, q_title):
        for q in self.quests:
            if q['title'] == q_title and q['status'] == "active":
                q['status'] = "complete"
                
                # Skill: Data Mining (Bonus Quest XP)
                bonus_mult = 1 + (self.rpg.get_skill_level("data_mining") * 0.15)
                final_xp = int(q['reward'] * bonus_mult)
                
                self.rpg.add_xp(final_xp, f"Completed {q['category']}")
                self.save()
                return True
        return False

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.quests, f)

