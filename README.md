# 🏛️ Patrimoine360 — pilotage et fiabilisation des données foncières et immobilières

**Projet de démonstration personnel — Khadidiatou Kenewy DIALLO**

> **Données 100 % synthétiques.** Ce dépôt est indépendant de Montpellier Méditerranée Métropole et **n'utilise ni ses bases patrimoniales, ni son environnement AS-TECH**. Les communes sont réelles, mais les actifs, valeurs, coordonnées et coûts sont fictifs.

## Pourquoi ce projet ?

Prototype réalisé à partir des **missions publiées** pour le poste « Chargé de mission pilotage et fiabilisation des données foncières et immobilières » (référence GRH4-2026-130) : référentiel foncier et immobilier, fiabilité et actualisation, tableaux de bord, schéma directeur immobilier, remontée des anomalies, transversalité entre outils métiers et SIG.

**Source de la fiche de poste :** https://www.emploi-territorial.fr/offre/o034260811000699-charge-mission-pilotage-fiabilisation-donnees-foncieres-immobilieres

## Fonctionnalités effectivement présentes

| Besoin | Démonstration |
|---|---|
| Gestion d'un inventaire | 1 500 actifs simulés, 12 communes, sites / bâtiments / lots / références parcellaires |
| Contrôles qualité automatisés | 10 règles, gravité, ligne d'origine, calcul du taux d'actifs conformes |
| Vision stratégique | 5 KPI, distributions par commune / type / statut, surfaces et coûts |
| SIG | Carte des coordonnées simulées et export CSV |
| Suivi des anomalies | Registre exportable avec actions recommandées et priorités |
| Schéma directeur immobilier | Analyse exploratoire coût/m², sous-occupation et besoins d'étude |
| Portabilité | Import d'un fichier CSV de même schéma ; exports CSV UTF-8 |
| Reproductibilité | Générateur avec seed fixe et anomalies injectées ; tests pytest / CI GitHub Actions |

## Architecture

```text
Patrimoine360/
├── app.py                      # Interface Streamlit multi-vues
├── src/
│   ├── generate.py             # Générateur déterministe de données fictives
│   └── quality.py              # Moteur de contrôle, indicateurs et plan d'action
├── data/patrimoine_demo.csv   # Inventaire fictif, 1 500 lignes
├── tests/test_quality.py      # Tests unitaires
├── docs/                      # Documentation projet et cas d'usage
├── .github/workflows/tests.yml
├── .streamlit/config.toml
└── requirements.txt
```

## Installation Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```

L'application s'ouvre à `http://localhost:8501`.

## Déploiement gratuit Streamlit Community Cloud

1. Créer un **nouveau dépôt public** GitHub `patrimoine360-pilotage-foncier`.
2. Extraire l'archive du projet et déposer **le contenu du dossier `Patrimoine360` à la racine** du dépôt (pas le dossier parent).
3. Sur https://share.streamlit.io : *Create app → From existing repo*, choisir ce dépôt, branche `main`, fichier principal `app.py`.
4. Déployer, ouvrir l'application, vérifier chaque onglet et copier son URL publique dans un mail.

L'application n'utilise aucun mot de passe, secret ou service externe.

## Gouvernance et réserves importantes

- **AS-TECH** : aucune intégration réelle. Un mapping et les accès officiels seraient nécessaires, avec validations métiers, sécurité et DSI.
- **Cadastre** : références parcellaires simulées ; aucune jointure cadastrale de production ni contrôle topologique réel.
- **SIG** : points de démonstration seulement, sans parcelles ou emprises bâtimentaires réelles.
- **Qualité** : règles pédagogiques à adapter aux référentiels, seuils et définitions des gestionnaires.
- **Scoring** : indicateur de dossier à instruire, jamais une recommandation de cession automatique.
- **Production** : il faudrait ajouter RBAC / habilitations, journal d'audit, sécurisation, actualisation ETL, PostgreSQL/PostGIS, journalisation, plan de recette et gouvernance RGPD selon les données traitées.

## Ressources d'inspiration (pas de code repris)

- Contrôle cadastral géospatial : https://github.com/andresdiaz2411/cadastral-data-quality-control
- Cartographie sur Streamlit : https://github.com/opengeos/streamlit-geospatial
- Source officielle sur le poste : https://www.emploi-territorial.fr/offre/o034260811000699-charge-mission-pilotage-fiabilisation-donnees-foncieres-immobilieres

## Présenter ce projet en entretien (60 secondes)

> « J'ai préparé un démonstrateur indépendant pour traduire concrètement ma compréhension du poste. Il articule un référentiel d'actifs, dix contrôles automatiques de fiabilité, une vision cartographique et un tableau de bord de pilotage. Les anomalies sont transformées en pistes d'action à qualifier avec les référents métiers. J'ai utilisé des données entièrement synthétiques ; mon objectif n'était pas de reproduire vos outils internes, mais de montrer comment je structurerais une démarche progressive de fiabilisation, de gouvernance et de restitution, en lien avec les utilisateurs et le Pôle numérique. »
