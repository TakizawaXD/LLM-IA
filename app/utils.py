import logging
import sys
from datetime import datetime
from typing import Any, Dict
from config import config

def setup_logger(name: str) -> logging.Logger:
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File handler for transformations specifically is handled in tracking.py
    # But a general app log could go here if needed.
    
    return logger

def format_timestamp() -> str:
    """Returns a formatted current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app_logger = setup_logger("TitanicApp")

import urllib.request
import urllib.parse
import json
import streamlit as st

def get_et_url(raw_name: str, survived: int) -> str:
    """Genera la URL probable del pasajero en Encyclopedia Titanica basado en su nombre."""
    try:
        if "," in raw_name:
            parts = raw_name.split(",", 1)
            last = parts[0].strip().lower()
            rest = parts[1].strip().split()
            if len(rest) > 0 and rest[0].endswith("."):
                rest = rest[1:]
            
            firsts = []
            for p in rest:
                if p.startswith("("): break
                firsts.append(p.lower().replace('"', '').replace("'", ""))
            
            clean = "-".join(firsts) + "-" + last
            clean = clean.replace(" ", "-").replace("--", "-")
            status = "survivor" if survived == 1 else "victim"
            return f"https://www.encyclopedia-titanica.org/titanic-{status}/{clean}.html"
    except Exception:
        pass
    
    # Fallback search url if name parsing fails
    safe_name = urllib.parse.quote(raw_name)
    return f"https://www.encyclopedia-titanica.org/search.html?q={safe_name}"

@st.cache_data(show_spinner=False)
def fetch_wikipedia_photo(raw_name: str) -> str:
    """Intenta buscar una foto en Wikipedia usando el nombre del pasajero del Titanic."""
    try:
        search_query = raw_name
        if "," in raw_name:
            parts = raw_name.split(",", 1)
            last = parts[0].strip()
            rest = parts[1].strip().split()
            if len(rest) > 0 and rest[0].endswith("."):
                rest = rest[1:]
            firsts = []
            for p in rest:
                if p.startswith("("): break
                firsts.append(p)
            clean = " ".join(firsts) + " " + last
            search_query = clean
            
        # Buscamos en inglés ya que hay más resultados del Titanic
        req_url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=' + urllib.parse.quote(search_query + ' titanic passenger') + '&format=json'
        
        req = urllib.request.Request(req_url, headers={'User-Agent': 'TitanicAppDemo/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read())
            search_res = res.get('query', {}).get('search', [])
            if not search_res:
                return None
                
            # Extraer el titulo del primer resultado
            title = search_res[0]['title']
            
            # Consultar la imagen de ese articulo
            img_url = 'https://en.wikipedia.org/w/api.php?action=query&titles=' + urllib.parse.quote(title) + '&prop=pageimages&format=json&pithumbsize=400'
            req2 = urllib.request.Request(img_url, headers={'User-Agent': 'TitanicAppDemo/1.0 (test@example.com)'})
            with urllib.request.urlopen(req2, timeout=5) as res2_raw:
                res2 = json.loads(res2_raw.read())
                pages = res2.get('query', {}).get('pages', {})
                for k, v in pages.items():
                    if 'thumbnail' in v:
                        return v['thumbnail']['source']
    except Exception as e:
        app_logger.error(f"Error fetching wiki photo for {raw_name}: {e}")
    return None
