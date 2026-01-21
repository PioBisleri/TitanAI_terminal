import json
import time
import numpy as np
from pathlib import Path
from llama_cpp import Llama
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.ui import console

class NeuralCore:
    def __init__(self, config):
        self.cfg = config
        self.mem_path = config.get_path('memory')
        self.history = []
        self.ltm = []
        self.rag_chunks = []
        self.llm = None
        self.model_name = "Offline"
        self._load_mem()

    def load_model(self, model_path):
        try:
            # Check if we need embeddings (High RAM usage)
            use_embeddings = self.cfg.data.get('rag_enabled', False)

            self.llm = Llama(
                model_path=str(model_path),
                n_ctx=self.cfg.data['n_ctx'],
                n_threads=self.cfg.data['n_threads'],
                n_gpu_layers=self.cfg.data['n_gpu_layers'],
                embedding=use_embeddings,  # Dynamic switch
                verbose=True # Keep verbose on to see health checks
            )
            self.model_name = model_path.name
            
            # Only index if enabled
            if use_embeddings:
                self._index_docs()
            else:
                self.rag_chunks = [] # Clear old chunks
                
            return True
        except Exception as e:
            return str(e)

    def _index_docs(self):
        if not self.cfg.data['rag_enabled']: return
        
        # Safety check: Llama must be loaded with embedding=True
        if not self.llm: return

        files = list((self.cfg.root / self.cfg.data['docs_dir']).glob("*.txt"))
        self.rag_chunks = []
        
        if not files: return

        with Progress(SpinnerColumn(), TextColumn("[cyan]Indexing Knowledge..."), transient=True) as p:
            task = p.add_task("", total=len(files))
            for fpath in files:
                txt = fpath.read_text(errors='ignore')
                for i in range(0, len(txt), 500):
                    chunk = txt[i:i+500]
                    if len(chunk) < 50: continue
                    try:
                        emb = self.llm.create_embedding(chunk)['data'][0]['embedding']
                        self.rag_chunks.append({"txt": chunk, "vec": emb, "src": fpath.name})
                    except: pass # Skip chunk if embedding fails
                p.advance(task)

    def search(self, query):
        if not self.rag_chunks or not self.llm: return ""
        if not self.cfg.data['rag_enabled']: return ""
        
        try:
            q_vec = self.llm.create_embedding(query)['data'][0]['embedding']
            scores = []
            for c in self.rag_chunks:
                score = np.dot(q_vec, c['vec'])
                scores.append((score, c))
            scores.sort(key=lambda x: x[0], reverse=True)
            return "\n".join([f"- {x[1]['txt']}" for x in scores[:2]])
        except: return ""

    def chat_stream(self, user_in, sys_prompt):
        self.history.append({"role": "user", "content": user_in})
        msgs = [{"role": "system", "content": sys_prompt}] + self.history[-5:]
        
        full_response = ""
        try:
            for chunk in self.llm.create_chat_completion(
                msgs, 
                stream=True, 
                temperature=self.cfg.data['temperature']
            ):
                delta = chunk['choices'][0]['delta']
                if 'content' in delta:
                    yield delta['content']
                    full_response += delta['content']
            
            self.history.append({"role": "assistant", "content": full_response})
            self._save_mem()
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _load_mem(self):
        if self.mem_path.exists():
            d = json.load(open(self.mem_path))
            self.history = d.get('history', [])
            self.ltm = d.get('ltm', [])

    def _save_mem(self):
        with open(self.mem_path, 'w') as f:
            json.dump({"history": self.history[-20:], "ltm": self.ltm}, f)

