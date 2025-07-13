import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import re
from typing import List, Dict, Tuple
import sys
import openai
import requests

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

    # Sidebar - Zdroj AI
    st.sidebar.markdown("---")
    st.sidebar.header("🧠 Zdroj AI")
    ai_source = st.sidebar.radio("Vyberte zdroj AI", ["OpenAI (cloud)", "Ollama (lokální)"])
    ollama_model = "llama3"
    if ai_source == "Ollama (lokální)":
        ollama_model = st.sidebar.selectbox(
            "Ollama model",
            ["llama3", "mistral", "gemma", "phi", "deepseek"],
            index=0,
            help="Pokud model nemáte, Ollama ho automaticky stáhne."
        )
        st.sidebar.markdown('<span style="font-size: 0.85em; color: #888;">'
                            'Ollama je open-source AI, kterou si můžete zdarma nainstalovat na svůj počítač. '
                            'Návod: <a href="https://ollama.com/download" target="_blank">ollama.com/download</a>'
                            '</span>', unsafe_allow_html=True)

    # Sidebar - OpenAI API klíč (jen pokud je vybrán OpenAI)
    openai_api_key = None
    if ai_source == "OpenAI (cloud)":
        st.sidebar.header("🔑 OpenAI API klíč")
        openai_api_key = st.sidebar.text_input("Zadejte svůj OpenAI API klíč", type="password", key="openai_api_key")
        st.sidebar.markdown('<span style="font-size: 0.85em; color: #888;">'
                            'Kde najdu API klíč? <a href="https://platform.openai.com/api-keys" target="_blank">Získat klíč zde</a>'
                            '</span>', unsafe_allow_html=True)

    # Sidebar - Nastavení
    st.sidebar.header("⚙️ Nastavení")
    st.sidebar.subheader("Pracovní doba")
    work_start = st.sidebar.time_input("Začátek", value=pd.to_datetime("09:00").time())
    work_end = st.sidebar.time_input("Konec", value=pd.to_datetime("17:00").time())
    st.sidebar.subheader("Rozdělování záznamů")
    max_chunk_minutes = st.sidebar.slider("Max. délka bloku (min)", 5, 120, 15)
    ignore_meetings = False
    if max_chunk_minutes == 15:
        ignore_meetings = st.sidebar.checkbox("Automaticky ignoruj schůzky", value=True)
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
        st.sidebar.success(f"Aplikace ti ušetřila: {saved_money:,.0f} Kč")
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

    def split_long_entry(entry: Dict, max_minutes: int, min_words: int, ignore_meetings: bool = False) -> List[Dict]:
        """Rozdělí dlouhý záznam na menší části, případně ignoruje schůzky"""
        description = str(entry.get('description', ''))
        words = description.split()
        # Pravidlo: blok musí mít více než min_words slov
        if len(words) < min_words:
            return [entry]
        # Pokud je aktivní ignorování schůzek a popis obsahuje 'schůzka', nerozděluj
        if ignore_meetings and 'schůzka' in description.lower():
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

    def call_openai_gpt(prompt, api_key):
        if not api_key:
            return "Nebyl zadán OpenAI API klíč."
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Chyba při volání OpenAI API: {str(e)}"

    def call_ollama_gpt(prompt, model="llama3"):
        url = "http://localhost:11434/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Chyba při volání Ollama API: {str(e)}"

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
                            # --- Automatické mapování sloupců ---
                            auto_map = {
                                "Projekt": ["projekt", "project"],
                                "Úkol": ["úkol", "task"],
                                "Popisek": ["popis", "popisek", "description", "desc"],
                                "Od kdy": ["od", "od kdy", "start", "from", "begin"],
                                "Do kdy": ["do", "do kdy", "end", "to", "finish"]
                            }
                            columns_mapping = {col: "Nepoužít" for col in df.columns}
                            for col in df.columns:
                                col_lower = col.lower()
                                for target, variants in auto_map.items():
                                    if any(variant in col_lower for variant in variants):
                                        columns_mapping[col] = target
                                        break
                            st.session_state.columns_mapping = columns_mapping
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
        if st.session_state.data is not None:
            df = st.session_state.data.copy()
            st.write("Klikněte na tlačítko pro spuštění AI zpracování (doplnění hluchých míst a rozpad dlouhých úkolů):")
            if st.button("Spustit AI zpracování", use_container_width=True):
                # Vylepšený prompt pro AI
                settings = f"""
Nastavení:
- Maximální délka bloku: {max_chunk_minutes} minut
- Minimální počet slov pro rozdělení: {min_words_split}
- Ignorovat schůzky: {'ano' if ignore_meetings else 'ne'}
- Vyplnit prázdná místa: {'ano' if fill_gaps else 'ne'}
- Pracovní doba: {work_start.strftime('%H:%M')} - {work_end.strftime('%H:%M')}
"""
                chunk_size = 10
                n_rows = len(df)
                n_chunks = (n_rows + chunk_size - 1) // chunk_size
                progress = st.progress(0, text="Probíhá optimalizace dat pomocí AI...")
                ai_results = []
                for i in range(n_chunks):
                    chunk_df = df.iloc[i*chunk_size:(i+1)*chunk_size]
                    # Zjisti časový rozsah chunku
                    time_cols = [col for col in chunk_df.columns if 'od' in col.lower() or 'start' in col.lower() or 'do' in col.lower() or 'end' in col.lower()]
                    min_time, max_time = None, None
                    if time_cols:
                        try:
                            min_time = pd.to_datetime(chunk_df[time_cols[0]].min())
                            max_time = pd.to_datetime(chunk_df[time_cols[-1]].max())
                        except Exception:
                            min_time, max_time = None, None
                    prompt = f"""Jsi asistent pro optimalizaci timesheetů. Pracuj pouze s časovým rozsahem, který je v nahraných datech – nikdy negeneruj záznamy mimo tento rozsah (od {min_time} do {max_time}).\n1. Pokud je mezi dvěma záznamy mezera (prázdné místo v čase), navrhni vhodnou aktivitu a označ ji jako is_generated=True.\n2. Pokud má popis více než {min_words_split} slov a trvá déle než {max_chunk_minutes} minut, rozděl jej na menší bloky (každý max {max_chunk_minutes} minut) a označ nové bloky is_split=True.\n3. Pokud je popis schůzka a je nastaveno ignorovat schůzky, nerozděluj.\n4. Výstup vrať jako CSV se stejnými sloupci jako vstup + sloupce is_generated, is_split.\n{settings}\nData:\n{chunk_df.to_csv(index=False)}"""
                    if ai_source == "OpenAI (cloud)":
                        ai_result = call_openai_gpt(prompt, openai_api_key)
                    else:
                        ai_result = call_ollama_gpt(prompt, model=ollama_model)
                    ai_results.append(ai_result)
                    progress.progress((i+1)/n_chunks, text=f"Optimalizováno {min((i+1)*chunk_size, n_rows)}/{n_rows} řádků...")
                # Pokus o spojení výsledků
                try:
                    df_ai = pd.concat([pd.read_csv(io.StringIO(res)) for res in ai_results], ignore_index=True)
                    # Kontrola: odstraň řádky mimo časový rozsah původních dat
                    if time_cols and min_time and max_time:
                        for col in time_cols:
                            try:
                                df_ai = df_ai[(pd.to_datetime(df_ai[col]) >= min_time) & (pd.to_datetime(df_ai[col]) <= max_time)]
                            except Exception:
                                pass
                    st.session_state.processed_data = df_ai
                except Exception:
                    st.session_state.processed_data = df
                st.session_state.ai_result = "\n---\n".join(ai_results)
                st.success("AI zpracování dokončeno. Výsledek najdete v záložce Výsledky.")
                st.session_state.active_tab = 3
                st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
                return False
            if 'ai_result' in st.session_state:
                st.info(f"AI výstup (náhled):\n{st.session_state.ai_result}")
        else:
            st.warning("Nejsou k dispozici žádná data ke zpracování.")

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
            # Podbarvení nových řádků
            def highlight_rows(row):
                if row['Typ řádku'] == 'Dovyplněný':
                    return ['background-color: #fff3cd'] * len(row)
                elif row['Typ řádku'] == 'Rozdělený':
                    return ['background-color: #cce5ff'] * len(row)
                else:
                    return [''] * len(row)
            st.dataframe(df.style.apply(highlight_rows, axis=1))
            # Tlačítko pro stažení CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Stáhnout CSV",
                data=csv,
                file_name="optimalizovany_vykaz.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Zatím nejsou k dispozici žádné výsledky ke zobrazení.")

if __name__ == "__main__":
    result = main()
    if result is False:
        sys.exit()
