import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple
import sys

def main():
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

    # Sidebar - Navigace
    steps = ["📤 Nahrání", "🔗 Mapování", "⚡ Zpracování", "📊 Výsledky"]
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0

    st.sidebar.title("Navigace")
    selected_tab = st.sidebar.radio("Krok", steps, index=st.session_state.active_tab, key="step_radio")
    st.session_state.active_tab = steps.index(selected_tab)

    # Sidebar - Nastavení
    st.sidebar.header("⚙️ Nastavení")
    st.sidebar.subheader("Pracovní doba")
    work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
    work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())
    st.sidebar.subheader("Rozdělování záznamů")
    max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
    min_words_split = st.sidebar.slider("Min. slov pro rozdělení", 5, 50, 10)
    st.sidebar.subheader("AI generování")
    fill_gaps = st.sidebar.checkbox("Vyplnit prázdná místa", value=True)
    ai_creativity = st.sidebar.slider("Kreativita AI", 0.1, 1.0, 0.7)

    # Sidebar - Ušetřeno
    st.sidebar.markdown("---")
    st.sidebar.header("💸 Ušetřeno")
    hourly_rate = st.sidebar.number_input("Vaše hodinová sazba (Kč)", min_value=0, value=0, step=100)
    saved_hours = st.sidebar.number_input("Ušetřené hodiny", min_value=0.0, value=0.0, step=0.5, format="%.2f")
    if hourly_rate > 0 and saved_hours > 0:
        saved_money = hourly_rate * saved_hours
        st.sidebar.success(f"Ušetřeno: {saved_money:,.0f} Kč")
    else:
        st.sidebar.info("Zadejte sazbu a počet hodin.")

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

    if st.session_state.active_tab == 0:
        st.header("Nahrání souboru")
        max_file_size_mb = 10
        error_message = None
        uploaded_file = st.file_uploader(
            "Vyberte CSV nebo Excel soubor",
            type=['csv', 'xlsx', 'xls'],
            help="""Podporované formáty:\n- CSV (.csv)\n- Excel (.xlsx, .xls)\nMaximální velikost souboru: 10 MB"""
        )
        if uploaded_file is not None:
            # Validace velikosti
            uploaded_file.seek(0, 2)  # na konec souboru
            file_size = uploaded_file.tell()
            uploaded_file.seek(0)
            if file_size > max_file_size_mb * 1024 * 1024:
                error_message = f"Soubor je příliš velký (max {max_file_size_mb} MB)."
            else:
                # Validace obsahu
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(uploaded_file)
                    else:
                        error_message = "Nepodporovaný formát souboru."
                    if error_message is None:
                        if df.shape[0] == 0 or df.shape[1] == 0:
                            error_message = "Soubor neobsahuje žádná data."
                        else:
                            st.session_state.data = df
                            st.success("Soubor byl úspěšně nahrán a zvalidován.")
                            st.session_state.active_tab = 1
                            st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
                            return True
                except Exception as e:
                    error_message = f"Chyba při načítání souboru: {str(e)}"
            if error_message:
                st.error(error_message)

    if st.session_state.active_tab == 1 and st.session_state.data is not None:
        st.header("Mapování sloupců")
        df = st.session_state.data
        st.write("Namapujte sloupce z nahraného souboru na požadované položky:")
        mapping_options = [
            "Nepoužít",
            "Projekt",
            "Úkol",
            "Popisek",
            "Od kdy",
            "Do kdy"
        ]
        columns = list(df.columns)
        if 'columns_mapping' not in st.session_state or not st.session_state.columns_mapping:
            st.session_state.columns_mapping = {col: "Nepoužít" for col in columns}
        for col in columns:
            st.session_state.columns_mapping[col] = st.selectbox(
                f"{col}", mapping_options, index=mapping_options.index(st.session_state.columns_mapping.get(col, "Nepoužít")), key=f"mapping_{col}"
            )
        if st.button("Potvrdit mapování"):
            st.session_state.active_tab = 2
            st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
            return False
        st.info("Po namapování potvrďte tlačítkem.")

    if st.session_state.active_tab == 2:
        st.header("Zpracování dat")
        st.info("Zde bude logika zpracování dat podle mapování.")

    if st.session_state.active_tab == 3:
        st.header("Výsledky")
        if st.session_state.get('processed_data') is not None:
            df = st.session_state.processed_data.copy()
            def row_type(row):
                if row.get('is_generated', False):
                    return 'Dovyplněný'
                elif row.get('is_split', False):
                    return 'Rozdělený'
                else:
                    return 'Původní'
            df['Typ řádku'] = df.apply(row_type, axis=1)
            st.dataframe(df)
        else:
            st.info("Zatím nejsou k dispozici žádné výsledky ke zobrazení.")

if __name__ == "__main__":
    result = main()
    if result is False:
        sys.exit()
