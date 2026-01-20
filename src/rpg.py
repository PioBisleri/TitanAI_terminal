import json
import time
from datetime import datetime
from src.ui import console

class RPGSystem:
    RANKS = {
        1: "Initiate", 5: "Scout", 10: "Operative", 
        20: "Vanguard", 35: "Commander", 50: "Titan"
    }

    def __init__(self, config):
        self.path = config.get_path('user')
        self.stats = {
            "level": 1, "xp": 0, "streak": 0, 
            "last_login": None, "rank": "Initiate",
            "hp": 100, "max_hp": 100
        }
        self.load()
        self.process_login()

    def add_xp(self, amount, reason="Unknown"):
        self.stats['xp'] += amount
        console.print(f"[bold green]✨ +{amount} XP[/] [dim]({reason})[/]")
        req = self.get_next_level_xp()
        if self.stats['xp'] >= req:
            self._level_up(req)
        self.save()

    def _level_up(self, req):
        self.stats['level'] += 1
        self.stats['xp'] -= req
        self.stats['max_hp'] += 10
        self.stats['hp'] = self.stats['max_hp']
        self._update_rank()
        console.print(f"[bold yellow]LEVEL UP! Rank: {self.stats['rank']}[/]")

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
            self.stats['hp'] = self.stats['max_hp']
            self.add_xp(50, "Daily Login")
            self.stats['last_login'] = today
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
                self.rpg.add_xp(q['reward'], f"Completed {q['category']}")
                self.save()
                return True
        return False

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.quests, f)
