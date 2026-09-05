import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def save_to_postgres(df, table_name="daily_weather_snapshots"):
    engine = create_engine(DATABASE_URL)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"{len(df)} lignes insérées dans '{table_name}'")