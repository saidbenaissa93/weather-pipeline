import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def save_to_postgres(df, table_name="daily_weather_snapshots"):
    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        # Crée la table avec une contrainte d'unicité sur la date si elle n'existe pas
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                date TIMESTAMPTZ PRIMARY KEY,
                temperature_max FLOAT,
                temperature_min FLOAT,
                precipitation_sum FLOAT
            )
        """))

        # Upsert : insère, ou met à jour si la date existe déjà
        for _, row in df.iterrows():
            conn.execute(text(f"""
                INSERT INTO {table_name} (date, temperature_max, temperature_min, precipitation_sum)
                VALUES (:date, :tmax, :tmin, :precip)
                ON CONFLICT (date) DO UPDATE SET
                    temperature_max = EXCLUDED.temperature_max,
                    temperature_min = EXCLUDED.temperature_min,
                    precipitation_sum = EXCLUDED.precipitation_sum
            """), {
                "date": row["date"],
                "tmax": row["temperature_max"],
                "tmin": row["temperature_min"],
                "precip": row["precipitation_sum"],
            })

    print(f"{len(df)} lignes traitées (upsert) dans '{table_name}'")