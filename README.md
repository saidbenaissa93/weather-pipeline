# 🌤️ Weather Pipeline — Villemomble

Un pipeline automatisé de données météo qui récupère chaque jour les prévisions à 5 jours pour la ville de Villemomble, les stocke dans une base de données PostgreSQL et les affiche sur un dashboard Streamlit.

## 🔄 Architecture du Projet

1. **Extraction** : Récupération des données météo via l'API Open-Meteo (`fetch_weather.py`).
2. **Stockage** : Sauvegarde/Mise à jour (Upsert) dans PostgreSQL (`db_utils.py`).
3. **Automation** : Exécution automatique quotidienne à 6h00 UTC via GitHub Actions (`.github/workflows/daily_weather.yml`).
4. **Visualisation** : Dashboard web interactif développé avec Streamlit (`dashboard.py`).

---

## 🛠️ Installation & Configuration Locale

### Préréquis

- Python 3.10+
- Une instance PostgreSQL fonctionnelle

```text
.
├── .github/workflows/
│   └── daily_weather.yml  # Pipeline d'automatisation GitHub Actions
├── dashboard.py           # Interface Streamlit d'affichage météo
├── db_utils.py            # Logique d'interaction et Upsert PostgreSQL
├── fetch_weather.py       # Appel API Open-Meteo
├── main.py                # Script principal d'exécution du pipeline
└── requirements.txt       # Dépendances Python du projet
```