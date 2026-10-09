# Note de cadrage — Patrimoine360

## Contexte

Un inventaire de patrimoine immobilier se caractérise par de nombreuses entités liées (sites, bâtiments, locaux, lots, parcelles), des sources hétérogènes et des exigences d'actualisation.

## Objectif

1. Consolider un référentiel minimal avec identifiants et provenance.
2. Identifier des anomalies traçables, mesurables et priorisées.
3. Produire des indicateurs décisionnels compréhensibles.
4. Organiser la correction à la source, pas seulement dans les tableaux de bord.

## MVP réalisé

Tableau de bord Streamlit interactif, inventaire synthétique 1 500 lignes, dix règles automatisées, carte des actifs fictifs, vue de stratégie immobilière, registre exportable de tickets, tests unitaires et automatisation GitHub Actions.

## Roadmap réelle à proposer, pas réalisée

- Phase 1 : ateliers avec métiers et DSI (règles, nomenclature, responsabilités, fréquence d'actualisation, indicateurs).
- Phase 2 : dictionnaire et schéma de données validés, imports réglementés, contrôles versionnés, suivi des corrections.
- Phase 3 : connexion autorisée aux applications internes, PostGIS et solution BI existante.
- Phase 4 : documentation, formation et suivi des indicateurs de qualité dans la durée.

## Risques

Attention aux jeux de données personnels ou contractuels, aux habilitations, aux définitions différentes des surfaces, à la validité des géocodages, au traitement de la domanialité et à la confusion entre signal métier et décision politique.
