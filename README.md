# 🌤️ Weather Pipeline — Villemomble

## 🎯 Objectif

Pipeline de données automatisé qui récupère quotidiennement les prévisions météo de Villemomble, les stocke dans une base de données cloud, et les affiche sur un dashboard web public — sans aucune intervention manuelle, même lorsque la machine de développement est éteinte.

Ce projet illustre un flux de données de bout en bout : ingestion automatisée, stockage persistant, et restitution visuelle, avec une infrastructure entièrement hébergée dans le cloud (gratuite).

## 🛠️ Outils et technologies

| Catégorie | Outil | Rôle |
|---|---|---|
| Langage | Python 3.13 | Logique du pipeline et du dashboard |
| Source de données | API Open-Meteo | Fournit les prévisions météo (température, précipitations) |
| Manipulation de données | pandas | Normalisation des réponses API en tables structurées |
| Base de données | PostgreSQL (hébergé sur Neon) | Stockage persistant des snapshots météo quotidiens |
| ORM / accès base | SQLAlchemy + psycopg2 | Connexion et requêtes vers PostgreSQL |
| Automatisation | GitHub Actions | Exécution planifiée quotidienne (cron) du pipeline |
| Visualisation | Streamlit | Dashboard web interactif |
| Hébergement dashboard | Streamlit Community Cloud | Mise à disposition publique du dashboard |
| Gestion des secrets | python-dotenv + GitHub/Streamlit Secrets | Protection des identifiants de connexion |

## 🏗️ Architecture
                ┌─────────────────────┐
                │   GitHub Actions     │
                │  (planificateur,     │
                │   tous les jours)     │
                └──────────┬───────────┘
                           │ déclenche
                           ▼
                ┌─────────────────────┐
                │      main.py         │
                │   (orchestrateur)     │
                └──────────┬───────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                            ▼
  ┌─────────────────────┐    ┌─────────────────────┐
  │  fetch_weather.py     │    │     db_utils.py       │
  │  Appelle l'API         │    │  Écrit/met à jour      │
  │  Open-Meteo et          │───▶│  les données dans       │
  │  normalise en            │    │  PostgreSQL (upsert)    │
  │  DataFrame                │    │                          │
  └─────────────────────┘    └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   PostgreSQL (Neon)    │
                              │  Table: daily_weather_  │
                              │  snapshots               │
                              └──────────┬──────────┘
                                         │ lecture
                                         ▼
                              ┌─────────────────────┐
                              │    dashboard.py         │
                              │  (Streamlit, hébergé     │
                              │   sur Streamlit Cloud)   │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              Dashboard public accessible
                              24h/24, sans dépendance
                              à une machine locale

## 📦 Composants du projet

- **`fetch_weather.py`** — Interroge l'API Open-Meteo pour les prévisions à 5 jours (température max/min, précipitations) et reconstruit les données en DataFrame pandas.
- **`db_utils.py`** — Gère la connexion à PostgreSQL et insère les données via une logique d'*upsert* (insertion ou mise à jour si la date existe déjà), garantissant l'absence de doublons.
- **`main.py`** — Point d'entrée du pipeline, orchestrant la récupération puis le stockage des données.
- **`dashboard.py`** — Application Streamlit qui lit les données en base et affiche les prévisions des 5 prochains jours sous forme de cartes.
- **`.github/workflows/daily_weather.yml`** — Configuration GitHub Actions déclenchant automatiquement le pipeline chaque jour.

## ☁️ Pourquoi une architecture 100% cloud

L'ensemble du pipeline fonctionne sans dépendre d'une machine physique allumée :
- **GitHub Actions** exécute le script d'ingestion sur une machine virtuelle temporaire.
- **Neon** héberge la base PostgreSQL en continu.
- **Streamlit Community Cloud** héberge le dashboard, accessible publiquement à tout moment.

Cette approche reproduit, à petite échelle, les principes d'un pipeline de données en production : automatisation, stockage centralisé, et restitution continue.