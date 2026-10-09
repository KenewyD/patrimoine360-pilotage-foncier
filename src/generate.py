import numpy as np
import pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
CITIES={'Montpellier':(43.6108,3.8767),'Castelnau-le-Lez':(43.635,3.913),'Lattes':(43.567,3.903),'Juvignac':(43.616,3.811),'Pérols':(43.565,3.95),'Grabels':(43.647,3.8),'Saint-Jean-de-Védas':(43.575,3.826),'Clapiers':(43.658,3.89),'Le Crès':(43.647,3.941),'Vendargues':(43.658,3.969),'Jacou':(43.661,3.911),'Prades-le-Lez':(43.698,3.867)}
TYPES=['Bureaux','École','Équipement sportif','Local associatif','Commerce','Logement','Entrepôt','Terrain non bâti','Culturel','Technique']
USES=['Administratif','Éducation','Sport','Association','Commerce','Habitation','Logistique','Réserve foncière','Culture','Services techniques']
def generate(seed=2026,n=1500):
 rng=np.random.default_rng(seed)
 rows=[]
 for i in range(n):
  city=rng.choice(list(CITIES),p=np.array([.47,.11,.08,.06,.05,.05,.05,.035,.025,.025,.025,.025])/sum([.47,.11,.08,.06,.05,.05,.05,.035,.025,.025,.025,.025])); lat,lon=CITIES[city]
  typ=str(rng.choice(TYPES,p=[.14,.15,.11,.12,.07,.13,.06,.08,.06,.08])); area=round(float(rng.lognormal(6.4,0.8)),1)
  if typ=='Terrain non bâti':area*=3
  cap=float(np.round(area*rng.uniform(.35,1.05),1))
  occupation=round(float(rng.uniform(0.2,1.0)),2) if typ!='Terrain non bâti' else 0.
  annual=round(float(area*rng.uniform(8,135)),0)
  status=str(rng.choice(['Actif','En travaux','Vacant'],p=[.81,.09,.10]));
  if status=='Vacant':occupation=0.
  rows.append({'site_id':f'S-{i//3+1:04d}','actif_id':f'ACT-{i+1:05d}','batiment_id':f'BAT-{i//2+1:04d}' if typ!='Terrain non bâti' else '', 'lot_id':f'LOT-{i+1:05d}' if typ not in ['Terrain non bâti','Équipement sportif'] else '', 'parcelle_id':f'{rng.integers(100,999):03d}AB{rng.integers(1,9999):04d}', 'commune':city,'type_actif':typ,'usage':USES[TYPES.index(typ)],'statut':status,'surface_m2':round(area,1),'surface_utile_m2':cap,'taux_occupation':occupation,'cout_annuel_eur':annual,'valeur_estimee_eur':round(float(area*rng.uniform(750,3100)),0),'annee_construction':int(rng.integers(1950,2025)),'classe_energie':str(rng.choice(list('ABCDEFG'))),'latitude':round(float(lat+rng.normal(0,.012)),6),'longitude':round(float(lon+rng.normal(0,.013)),6),'date_maj':str(pd.Timestamp('2026-09-30')-pd.Timedelta(days=int(rng.integers(0,850))))[:10],'source':str(rng.choice(['Inventaire','SIG','Maintenance','Gestion locative','Import AS-TECH simulé'])),'referent':str(rng.choice(['Patrimoine','Service foncier','Gestion technique','Service immobilier']))})
 df=pd.DataFrame(rows)
 # Défauts intentionnels, reproductibles et documentés
 df.loc[[7,38,98,289,544,1011],'surface_m2']=-10
 df.loc[[23,129,399,520,800,990],'surface_utile_m2']=df.loc[[23,129,399,520,800,990],'surface_m2']*1.8
 df.loc[[18,78,215,620,1201],'taux_occupation']=1.35
 df.loc[[11,119,814,1214],'commune']=''
 df.loc[[31,450,1320],'parcelle_id']=''
 df.loc[[66,503,1100],'latitude']=0
 df.loc[[91,806,1422],'cout_annuel_eur']=-999
 df.loc[[45,156,959,1401],'date_maj']='2022-01-01'
 df.loc[[247,622],'actif_id']=df.loc[246,'actif_id']
 df.to_csv(DATA/'patrimoine_demo.csv',index=False)
 return df
if __name__=='__main__':
 print('Généré',len(generate()),'actifs de démonstration')
