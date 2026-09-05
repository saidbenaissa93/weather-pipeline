import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="Météo Villemomble", page_icon="🌤️", layout="wide")
st.title("🌤️ Météo — Villemomble")

@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM daily_weather_snapshots ORDER BY date"
    df = pd.read_sql(query, engine)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

if df.empty:
    st.warning("Aucune donnée disponible.")
else:
    # Garde uniquement les 5 prochains jours à partir d'aujourd'hui
    today = pd.Timestamp.now(tz="UTC").normalize()
    upcoming = df[df["date"] >= today].head(5)

    if upcoming.empty:
        upcoming = df.tail(5)  # fallback si pas de données futures

    st.caption("Prévisions sur les 5 prochains jours")

    cols = st.columns(len(upcoming))

    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    for col, (_, row) in zip(cols, upcoming.iterrows()):
        with col:
            jour_nom = jours_fr[row["date"].weekday()]
            st.markdown(f"**{jour_nom}**")
            st.caption(row["date"].strftime("%d/%m"))
            st.metric("Max", f"{row['temperature_max']:.0f} °C")
            st.metric("Min", f"{row['temperature_min']:.0f} °C")
            st.write(f"🌧️ {row['precipitation_sum']:.1f} mm")

    st.caption("⚠️ Ces valeurs sont des prévisions enregistrées au moment du dernier passage du pipeline, pas une mesure en temps réel.")