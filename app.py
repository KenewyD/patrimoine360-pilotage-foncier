import io
import pandas as pd
import plotly.express as px
import streamlit as st
from src.quality import validate,planning
st.set_page_config(page_title='Patrimoine360 | Pilotage foncier',page_icon='🏛️',layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem;max-width:1450px}div[data-testid="stMetric"]{background:#f3f6fa;padding:18px;border-radius:13px;border:1px solid #dde5ef}h1,h2,h3{color:#172b49}</style>''',unsafe_allow_html=True)
st.title('🏛️ Patrimoine360')
st.caption('Démonstrateur indépendant — Pilotage & fiabilisation des données foncières et immobilières | Données 100 % synthétiques, non officielles')
st.info('Projet personnel conçu à partir des missions publiques du poste GRH4-2026-130. Aucune connexion à AS-TECH ni aux systèmes de la Métropole.')
@st.cache_data
def data():return pd.read_csv('data/patrimoine_demo.csv',dtype={'parcelle_id':str,'actif_id':str})
original=data()
upload=st.sidebar.file_uploader('📥 Import CSV patrimoine (schéma modèle)',type=['csv'])
if upload:
 try:
  df=pd.read_csv(upload)
  missing=set(original.columns)-set(df.columns)
  if missing:st.sidebar.error('Colonnes manquantes : '+', '.join(sorted(missing)));st.stop()
 except Exception as e:st.sidebar.error(str(e));st.stop()
else:df=original.copy()
st.sidebar.header('🔎 Périmètre')
communes=st.sidebar.multiselect('Commune',sorted(df['commune'].dropna().unique()),default=[])
types=st.sidebar.multiselect('Type de bien',sorted(df['type_actif'].dropna().unique()),default=[])
statuses=st.sidebar.multiselect('Statut',sorted(df['statut'].dropna().unique()),default=[])
filtered=df.copy()
if communes:filtered=filtered[filtered['commune'].isin(communes)]
if types:filtered=filtered[filtered['type_actif'].isin(types)]
if statuses:filtered=filtered[filtered['statut'].isin(statuses)]
issues,quality=validate(filtered)
view=st.sidebar.radio('Navigation',['📊 Vue exécutive','✅ Fiabilisation','🗺️ SIG & localisation','🏗️ Stratégie immobilière','🎫 Plan d’action & tickets','📁 Référentiel et exports'])
valid_area=filtered.loc[filtered['surface_m2']>0,'surface_m2'].sum()
cols=st.columns(5)
for col,(label,value) in zip(cols,[('Actifs',f"{quality['actifs']:,}"),('Qualité',f"{quality['qualite_pct']} %"),('Anomalies',f"{quality['anomalies']:,}"),('Surface valide',f"{valid_area:,.0f} m²"),('Coût annuel positif',f"{filtered.loc[filtered.cout_annuel_eur>=0,'cout_annuel_eur'].sum()/1e6:.1f} M€")]):col.metric(label,value)
st.divider()
if view=='📊 Vue exécutive':
 st.subheader('Vue consolidée du patrimoine')
 a,b=st.columns(2)
 with a:st.plotly_chart(px.bar(filtered.groupby('type_actif',as_index=False)['surface_m2'].apply(lambda x:x[x>0].sum()),x='type_actif',y='surface_m2',title='Surfaces par catégorie d’actif'),use_container_width=True)
 with b:st.plotly_chart(px.pie(filtered,names='statut',title='Répartition du statut des actifs',hole=.47),use_container_width=True)
 a,b=st.columns(2)
 with a:st.plotly_chart(px.bar(filtered.groupby('commune',as_index=False).size().sort_values('size',ascending=False).head(12),x='commune',y='size',title='Nombre d’actifs par commune'),use_container_width=True)
 with b:
  if not issues.empty:st.plotly_chart(px.bar(issues.groupby(['regle','gravite'],as_index=False).size(),x='regle',y='size',color='gravite',title='Anomalies par règle'),use_container_width=True)
 st.caption('Les coûts et surfaces sont des estimations de données simulées. Les chiffres ne décrivent pas le patrimoine réel de Montpellier.')
elif view=='✅ Fiabilisation':
 st.subheader('Contrôles qualité et traçabilité')
 st.write('10 règles de contrôle : unicité, référentiel, surfaces, occupation, coûts, géolocalisation et fraîcheur des données.')
 if not issues.empty:
  st.plotly_chart(px.bar(issues.groupby(['regle','gravite'],as_index=False).size(),x='regle',y='size',color='gravite',title='Répartition des non-conformités'),use_container_width=True)
  st.dataframe(issues,hide_index=True,use_container_width=True)
  st.download_button('⬇️ Export rapport d’anomalies CSV',issues.to_csv(index=False).encode('utf-8-sig'),'anomalies_patrimoine360.csv','text/csv')
 else:st.success('Aucune anomalie détectée dans le périmètre filtré.')
elif view=='🗺️ SIG & localisation':
 st.subheader('Carte interactive des actifs')
 valid=filtered[filtered.latitude.between(43.45,43.85)&filtered.longitude.between(3.65,4.15)].copy()
 st.map(valid,latitude='latitude',longitude='longitude',size=35)
 st.dataframe(valid[['actif_id','commune','type_actif','surface_m2','latitude','longitude']],hide_index=True,use_container_width=True)
 st.caption('Coordonnées fictives autour des centres communaux, non localisations de bâtiments réels.')
elif view=='🏗️ Stratégie immobilière':
 st.subheader('Aide à la décision — scénario exploratoire')
 st.warning('Scoring illustratif et non décision administrative. Toute décision nécessite validation métier, réglementaire et budgétaire.')
 work=filtered[(filtered.surface_m2>0)&filtered.taux_occupation.between(0,1)&(filtered.cout_annuel_eur>=0)].copy()
 work['cout_m2']=work.cout_annuel_eur/work.surface_m2
 work['priorite_etude']=(work['taux_occupation'].le(.35).astype(int)*2+work['cout_m2'].ge(work['cout_m2'].quantile(.75)).astype(int)*2+work.statut.eq('Vacant').astype(int)*2+work.classe_energie.isin(['F','G']).astype(int))
 st.dataframe(work.sort_values('priorite_etude',ascending=False)[['actif_id','commune','type_actif','statut','surface_m2','taux_occupation','cout_m2','classe_energie','priorite_etude']].head(100),hide_index=True,use_container_width=True)
 st.plotly_chart(px.scatter(work,x='taux_occupation',y='cout_m2',size='surface_m2',color='type_actif',hover_name='actif_id',title='Occupation et coût annuel au m² — pistes d’analyse'),use_container_width=True)
 st.caption('Le score signale uniquement des dossiers à examiner : il ne propose pas de vendre, fermer ou céder automatiquement des biens.')
elif view=='🎫 Plan d’action & tickets':
 st.subheader('Registre de traitement des anomalies')
 tickets=planning(issues)
 if not tickets.empty:
  st.dataframe(tickets,hide_index=True,use_container_width=True)
  st.download_button('⬇️ Export tickets CSV',tickets.to_csv(index=False).encode('utf-8-sig'),'tickets_actions.csv','text/csv')
  st.info('Processus cible : détection → qualification métier → affectation → correction dans le SI source → nouveau contrôle → clôture. Le registre ne synchronise pas AS-TECH.')
 else:st.success('Aucune anomalie à traiter.')
else:
 st.subheader('Dictionnaire du référentiel')
 st.write('Modèle simplifié : **Site → Bâtiment → Lot / actif**, relié à une référence parcellaire et à des attributs métiers. Le modèle réel devra être validé avec les propriétaires des données.')
 st.dataframe(filtered,hide_index=True,use_container_width=True)
 st.download_button('⬇️ Export données filtrées',filtered.to_csv(index=False).encode('utf-8-sig'),'referentiel_patrimoine.csv','text/csv')
 st.markdown('**Interopérabilité proposée (non connectée)** : exports normalisés CSV ; mapping à spécifier avec AS-TECH, SIG et référentiels existants.')
st.caption('© 2026 — Démonstration portfolio : Khadidiatou Kenewy DIALLO | Non affilié à Montpellier Méditerranée Métropole.')
