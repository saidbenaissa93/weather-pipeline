from fetch_weather import get_daily_weather
from db_utils import save_to_postgres

def main():
    df = get_daily_weather()
    save_to_postgres(df)

if __name__ == "__main__":
    main()