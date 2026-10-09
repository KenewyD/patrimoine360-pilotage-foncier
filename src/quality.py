import pandas as pd
import numpy as np
RULES={
 'ID_DUPLIQUE':('Critique','Identifiant d’actif dupliqué'),
 'COMMUNE_MANQUANTE':('Élevée','Commune non renseignée'),
 'PARCELLE_MANQUANTE':('Élevée','Référence parcellaire absente'),
 'SURFACE_INVALIDE':('Critique','Surface nulle ou négative'),
 'SURFACE_UTILE_INCOHERENTE':('Élevée','Surface utile supérieure à surface totale'),
 'OCCUPATION_INVALIDE':('Élevée','Taux d’occupation hors [0,1]'),
 'COUT_NEGATIF':('Élevée','Coût annuel négatif'),
 'COORDONNEES_INVALIDES':('Moyenne','Coordonnées manquantes ou hors métropole de démonstration'),
 'DONNEES_OBSOLETES':('Moyenne','Mise à jour vieille de plus de 18 mois'),
 'BATIMENT_MANQUANT':('Élevée','Bâtiment absent pour une unité bâtie'),
}
def validate(df, today='2026-10-09'):
 d=df.copy(); dt=pd.to_datetime(d['date_maj'],errors='coerce')
 masks={
 'ID_DUPLIQUE':d['actif_id'].duplicated(keep=False),
 'COMMUNE_MANQUANTE':d['commune'].isna()|d['commune'].astype(str).str.strip().eq(''),
 'PARCELLE_MANQUANTE':d['parcelle_id'].isna()|d['parcelle_id'].astype(str).str.strip().eq(''),
 'SURFACE_INVALIDE':pd.to_numeric(d['surface_m2'],errors='coerce').le(0)|d['surface_m2'].isna(),
 'SURFACE_UTILE_INCOHERENTE':d['surface_utile_m2']>d['surface_m2'],
 'OCCUPATION_INVALIDE':~d['taux_occupation'].between(0,1),
 'COUT_NEGATIF':d['cout_annuel_eur']<0,
 'COORDONNEES_INVALIDES':~d['latitude'].between(43.45,43.85)|~d['longitude'].between(3.65,4.15),
 'DONNEES_OBSOLETES':dt.lt(pd.Timestamp(today)-pd.DateOffset(months=18))|dt.isna(),
 'BATIMENT_MANQUANT':(d['type_actif']!='Terrain non bâti') & (d['batiment_id'].isna()|d['batiment_id'].astype(str).str.strip().eq('')),
 }
 events=[]
 for rule,mask in masks.items():
  sev,desc=RULES[rule]
  for ix in d.index[mask.fillna(False)]:events.append({'actif_id':str(d.at[ix,'actif_id']),'ligne':int(ix)+2,'regle':rule,'gravite':sev,'description':desc,'statut_ticket':'À qualifier','responsable':'Référent patrimoine','priorite':{'Critique':1,'Élevée':2,'Moyenne':3}[sev]})
 issues=pd.DataFrame(events,columns=['actif_id','ligne','regle','gravite','description','statut_ticket','responsable','priorite'])
 issue_rows=set(issues['ligne']) if len(issues) else set()
 metrics={'actifs':len(d),'anomalies':len(issues),'actifs_conformes':len(d)-len(issue_rows),'qualite_pct':round(100*(len(d)-len(issue_rows))/max(1,len(d)),1),'criticite':int((issues['gravite']=='Critique').sum()) if len(issues) else 0}
 return issues,metrics

def planning(issues):
 if issues.empty:return issues
 p=issues.copy();p['action_recommandee']=p['regle'].map({
 'ID_DUPLIQUE':'Contrôler le référentiel maître et fusionner après validation métier',
 'COMMUNE_MANQUANTE':'Faire confirmer la commune par le service foncier',
 'PARCELLE_MANQUANTE':'Réconcilier avec le SIG / référentiel parcellaire',
 'SURFACE_INVALIDE':'Vérifier plan, état de division ou mesurage',
 'SURFACE_UTILE_INCOHERENTE':'Vérifier la définition des surfaces et le plan',
 'OCCUPATION_INVALIDE':'Contrôler la convention et le relevé d’occupation',
 'COUT_NEGATIF':'Vérifier les charges et écritures sources',
 'COORDONNEES_INVALIDES':'Faire géocoder / confirmer la localisation',
 'DONNEES_OBSOLETES':'Solliciter le référent métier pour actualisation',
 'BATIMENT_MANQUANT':'Rapprocher le local du bâtiment dans le référentiel'})
 return p.sort_values(['priorite','actif_id','regle'])
