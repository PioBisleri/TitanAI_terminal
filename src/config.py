import json
from pathlib import Path

class Config:
    DEFAULTS = {
        "models_dir": "models",
        "docs_dir": "documents",
        "data_dir": "data",
        "n_ctx": 2048,           # Lowered for safety (was 4096)
        "n_threads": 4,
        "n_gpu_layers": 0,       # Default to 0 (CPU only) for stability
        "temperature": 0.7,
        "rag_enabled": False     # Default to False to save RAM on startup
    }
    
    def __init__(self):
        self.root = Path.cwd()
        self.data = self.DEFAULTS.copy()
        
        # Ensure directories exist
        (self.root / self.data['models_dir']).mkdir(exist_ok=True)
        (self.root / self.data['docs_dir']).mkdir(exist_ok=True)
        (self.root / self.data['data_dir']).mkdir(exist_ok=True)
        
        self.load()

    def get_path(self, key):
        """Helper to get full paths for data files"""
        if key in ['memory', 'quests', 'user']:
            return self.root / self.data['data_dir'] / f"v1_{key}.json"
        return self.root / self.data[key]

    def update(self, key, value):
        self.data[key] = value
        self.save()

    def load(self):
        p = self.root / "v1_config.json"
        if p.exists():
            try:
                with open(p) as f: self.data.update(json.load(f))
            except: pass
    
    def save(self):
        with open(self.root / "v1_config.json", 'w') as f: 
            json.dump(self.data, f, indent=4)

