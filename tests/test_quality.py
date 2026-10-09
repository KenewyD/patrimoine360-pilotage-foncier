import pandas as pd
from src.quality import validate,planning

def row(**kwargs):
 d={'site_id':'S1','actif_id':'A1','batiment_id':'B1','lot_id':'L1','parcelle_id':'123AB0012','commune':'Montpellier','type_actif':'Bureaux','surface_m2':100.,'surface_utile_m2':80.,'taux_occupation':.8,'cout_annuel_eur':300.,'latitude':43.6,'longitude':3.87,'date_maj':'2026-09-01'}
 d.update(kwargs);return d

def test_valid():
 issues,m=validate(pd.DataFrame([row()])); assert issues.empty and m['qualite_pct']==100

def test_bad_surface():
 issues,_=validate(pd.DataFrame([row(surface_m2=-10)])); assert 'SURFACE_INVALIDE' in set(issues.regle)

def test_duplicate():
 issues,_=validate(pd.DataFrame([row(),row()])); assert (issues.regle=='ID_DUPLIQUE').sum()==2

def test_stale():
 issues,_=validate(pd.DataFrame([row(date_maj='2020-01-01')])); assert 'DONNEES_OBSOLETES' in set(issues.regle)

def test_action():
 issues,_=validate(pd.DataFrame([row(cout_annuel_eur=-1)])); assert planning(issues).iloc[0]['action_recommandee']
