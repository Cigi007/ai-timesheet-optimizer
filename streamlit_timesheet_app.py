import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje AI generování aktivit pro prázdná místa"""
    common_activities = [
        "Email komunikace a koordinace",
        "Plánování a organizace úkolů", 
        "Konzultace s kolegy",
        "Dokumentace a zápisy",
        "Code review a kontrola kvality",
        "Schůzka týmu",
        "Analýza požadavků",
        "Testování a debugging",
        "Administrativa a reporty",
        "Studium a vzdělávání",
        "Příprava na prezentaci",
        "Synchronizace s klientem"
    ]
    
    # Jednoduché AI - vybírá na základě času a kontextu
    suggestions = []
    for gap in gaps:
        duration = gap['duration_minutes']
        if duration <= 15:
            activity = np.random.choice([
                "Email komunikace", 
                "Rychlá konzultace",
                "Administrativa"
            ])
        elif duration <= 30:
            activity = np.random.choice([
                "Plánování úkolů",
                "Dokumentace",
                "Code review"
            ])
        else:
            activity = np.random.choice([
                "Schůzka týmu",
                "Analýza požadavků", 
                "Příprava prezentace"
            ])
        
        suggestions.append(f"{activity} ({duration} min)")
    
    return suggestions

def parse_time_duration(start_time: str, end_time: str) -> int:
    """Vypočítá délku v minutách mezi dvěma časy"""
    try:
        start = pd.to_datetime(start_time, format='%H:%M')
        end = pd.to_datetime(end_time, format='%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def split_long_entry(entry: Dict, max_minutes: int, min_words: int) -> List[Dict]:
    """Rozdělí dlouhý záznam na menší části"""
    description = str(entry.get('description', ''))
    words = description.split()
    
    if len(words) < min_words:
        return [entry]
    
    duration = parse_time_duration(entry.get('time_start', ''), entry.get('time_end', ''))
    if duration <= max_minutes:
        return [entry]
    
    # Počet částí
    num_chunks = max(1, duration // max_minutes)
    if duration % max_minutes > 0:
        num_chunks += 1
    
    chunks = []
    words_per_chunk = max(1, len(words) // num_chunks)
    
    start_time = pd.to_datetime(entry.get('time_start', ''), format='%H:%M')
    
    for i in range(num_chunks):
        chunk_start_word = i * words_per_chunk
        chunk_end_word = min((i + 1) * words_per_chunk, len(words))
        
        chunk_duration = min(max_minutes, duration - (i * max_minutes))
        chunk_end_time = start_time + timedelta(minutes=chunk_duration)
        
        chunk_description = ' '.join(words[chunk_start_word:chunk_end_word])
        if num_chunks > 1:
            chunk_description += f" (část {i+1}/{num_chunks})"
        
        chunk = entry.copy()
        chunk['time_start'] = start_time.strftime('%H:%M')
        chunk['time_end'] = chunk_end_time.strftime('%H:%M')
        chunk['description'] = chunk_description
        chunk['is_split'] = True
        chunk['original_entry'] = i == 0
        
        chunks.append(chunk)
        start_time = chunk_end_time
    
    return chunks

# Hlavní obsah
tab1, tab2, tab3, tab4 = st.tabs(["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"])

with tab1:
    st.header("Nahrání souboru")
    
    uploaded_file = st.file_uploader(
        "Vyberte CSV nebo Excel soubor",
        type=['csv', 'xlsx', 'xls'],
        help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\n"""
    )

<rewritten_file>
```
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple

# Konfigurace stránky
st.set_page_config(
    page_title="Timesheet Analyzer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hlavní nadpis
st.title("🧠 Timesheet Analyzer AI")
st.markdown("*Inteligentní analýza a optimalizace pracovních záznamů*")

# Inicializace session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Postranní panel - nastavení
st.sidebar.header("⚙️ Nastavení")

# Pracovní doba
st.sidebar.subheader("Pracovní doba")
work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())

# Nastavení rozdělování
st.sidebar.subheader("Rozdělování záznamů")
max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)

# AI nastavení
st.sidebar.subheader("AI generování")
fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

# Funkce pro simulaci AI generování
def generate_activity_suggestions(gaps: List[Dict], existing_activities: List[str]) -> List[str]:
    """Simuluje