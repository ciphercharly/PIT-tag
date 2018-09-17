# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import base64

import pandas as pd
import numpy as np

import csv 
import sys
import urllib
from datetime import datetime, date
import matplotlib.pyplot as plt
import matplotlib

reload(sys)
sys.setdefaultencoding('utf-8')

#---------------------------------------------------------------------------------------------------------------------
mapbox_access_token = 'pk.eyJ1IjoidXp6YXdhenphIiwiYSI6ImNqNGI2ODEzNDA3b2Yyd296YXc1ZWtoaWUifQ.O-H18RnFUOJKTmhg2KvcEA'
outdoors = 'mapbox://styles/uzzawazza/cjlakfyg92j1f2rmfp7oa9oxu'
dark = 'mapbox://styles/uzzawazza/cjlajufw14l0s2so55qw99c7v'
decimal = 'mapbox://styles/uzzawazza/cj5nglefb4ce42spgj3ztk1zi'
whaam = 'mapbox://styles/uzzawazza/cj5ch190n040o2rqzxkkckuxi'
northstar = 'mapbox://styles/uzzawazza/cj5du1vlq0ryn2rmfoud5eyy0'
standard = 'mapbox://styles/uzzawazza/cj5dtrheb0rod2rqllkpgmhfe'
moonlight = 'mapbox://styles/uzzawazza/cj5dhqder0gi22rnxrwiyy94e'
punk = 'mapbox://styles/uzzawazza/cj6530c5n5y4q2slorqtpto45'
terminal = 'mapbox://styles/uzzawazza/cj6530c5n5y4q2slorqtpto45'
desert = 'mapbox://styles/uzzawazza/cj7vkqbly0w172rn2aj3v3bnt'
ukiyoe = 'mapbox://styles/uzzawazza/cjb2fthg415bh2slkkc31p0c2'
leshine = 'mapbox://styles/uzzawazza/cjcw51z9z13u22rllhju07if1'
odyssey = 'mapbox://styles/uzzawazza/cj96leg9f0mu72rmt5u180qs9'
metropolis = 'mapbox://styles/uzzawazza/cjbi5od8o02z92ro9fklp3fnp'
headsup = 'mapbox://styles/uzzawazza/cjgz5z4jt009l2rogj9sawwrg'
labelmaker = 'mapbox://styles/uzzawazza/cjlaj81ot4kg72socnsht5jlt'
#----------------------------------------------------------------------------------------------------------------------

file1 = 'REEDITED-allrepingsbyALLantennas-vassdrag.csv'
mergeALLmarkingALLantennadf = pd.read_csv(file1,sep=';',encoding='latin-1',dtype=str)
mergeALLmarkingALLantennadf['Vassdrag'] = mergeALLmarkingALLantennadf['Vassdrag'].str.replace(u"\xc3",u"\xc5")
mergeALLmarkingALLantennadf['AntennaName'] = mergeALLmarkingALLantennadf['AntennaName'].str.replace(u"\xc3",u"\xc5")
mergeALLmarkingALLantennadf['Gruppe'] = mergeALLmarkingALLantennadf['Gruppe'].str.replace(u"\xc3",u"\xc5")
mergeALLmarkingALLantennadf['Utsett.sted'] = mergeALLmarkingALLantennadf['Utsett.sted'].str.replace(u"\xc3",u"\xc5")
mergeALLmarkingALLantennadf['Fangst.sted'] = mergeALLmarkingALLantennadf['Fangst.sted'].str.replace(u"\xc3",u"\xc5")
#-----------------------------------------------------------------------------------------------------------------------

file2 = 'REEDITED-MARKING-ALLYEARS.csv'
dfmarking = pd.read_csv(file2,sep=';',encoding='ISO-8859-1',dtype=str)

# ADDING NEW COLUMN Gr.størrelse TO MARKING DATABASE WITH GROUPS COUNTINGS
groupbygruppe = dfmarking.groupby(['Gruppe'])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()

dfmarking[u'Gr.størrelse']='NA'

for gr in groupbygruppe['Gruppe'].values:
    dfmarking.loc[dfmarking['Gruppe']==gr,u'Gr.størrelse']=groupbygruppe[groupbygruppe['Gruppe']==gr]['PIT.ID'].values

dfmarking['Utsett.sted'] = dfmarking['Utsett.sted'].str.replace(u"\xc3\xb8",u"\xf8")
dfmarking['Fangst.sted'] = dfmarking['Fangst.sted'].str.replace(u"\xc3\xb8",u"\xf8")
dfmarking = dfmarking[dfmarking['Utsett.sted']!=u'Død']


#----------------------------------------------------------------------------------------------------------------------

filecoord = 'LokalitetInformation-TEMPMIXFAKES.csv'
coordsdf = pd.read_csv(filecoord,sep=';',names=['name','lat','lon'],encoding='latin-1',dtype={'name':str,'lat':np.float64,'lon':np.float64})

#----------------------------------------------------------------------------------------------------------------------

# full date format %Y-%m-%d
dfformatdatefull = mergeALLmarkingALLantennadf.copy()
del mergeALLmarkingALLantennadf
dfformatdatefull["date"]= pd.to_datetime(dfformatdatefull["date"],format='%Y-%m-%d')#, format='%Y-%m-%d %H:%M:%S')
#dfformatdatefull = dfformatdatefull[dfformatdatefull > pd.to_datetime('2014-01-01')]# filter a priori dates previous to 2014, they are registering errors in the first place 
#dfformatdatefull = dfformatdatefull[dfformatdatefull < pd.to_datetime('2018-12-31')]# filter a priori dates in the future 
                                                                  # (this should be solved elsewhere, when merging the data, before dumping the final dataframe) 

print dfformatdatefull['AntennaName'].unique()

# format also Fangst.dato on which they want custom filtering too
dfformatdatefull["Fangst.dato"]= pd.to_datetime(dfformatdatefull["Fangst.dato"], errors='coerce')#, format='%Y-%m-%d %H:%M:%S')

#abs_min_fangstdato = dfformatdatefull['Fangst.dato'].min()
#abs_max_fangstdato = dfformatdatefull['Fangst.dato'].max()
abs_min_date = dfformatdatefull['date'].min()
abs_max_date = dfformatdatefull['date'].max()

# pre-filter vassdrag 
dfformatdatefullvosso = dfformatdatefull[dfformatdatefull['Vassdrag']=='Vosso']
dfformatdatefulldale = dfformatdatefull[dfformatdatefull['Vassdrag']=='Dale']
dfformatdatefulleidfjord = dfformatdatefull[dfformatdatefull['Vassdrag']=='Eidfjord']
dfformatdatefullmodalen = dfformatdatefull[dfformatdatefull['Vassdrag']=='Modalen']
dfformatdatefullapel = dfformatdatefull[dfformatdatefull['Vassdrag']=='Apeltun']
dfformatdatefullarna = dfformatdatefull[dfformatdatefull['Vassdrag']=='Arna']
dfformatdatefulleksi = dfformatdatefull[dfformatdatefull['Vassdrag']=='Eksingedal']
dfformatdatefullsjo = dfformatdatefull[dfformatdatefull['Vassdrag']==u'Sjø']
dfformatdatefullaroy = dfformatdatefull[dfformatdatefull['Vassdrag']==u'Årøy']
dfformatdatefullardal = dfformatdatefull[dfformatdatefull['Vassdrag']==u'Årdal']

vassdragdict = {'Apeltun': dfformatdatefullapel,'Arna':dfformatdatefullarna,'Eidfjord':dfformatdatefulleidfjord,'Vosso':dfformatdatefullvosso,'Dale':dfformatdatefulldale,'Eksingedal':dfformatdatefulleksi,'Sjø':dfformatdatefullsjo,'Modalen':dfformatdatefullmodalen,'Årdal':dfformatdatefullardal,'Årøy':dfformatdatefullaroy}

# pre-filter Antennae
dfformatdatefullOynaholenBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'ØynahølenBunnM']
dfformatdatefullOynaholenBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'ØynahølenBunnS']
dfformatdatefullAroyBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'ÅrøyBunnM']
dfformatdatefullAroyBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'ÅrøyBunnS']
dfformatdatefullArdalBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'ÅrdalBunnM']
dfformatdatefullArdalBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'ÅrdalBunnS']
dfformatdatefullVassendenBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'VassendenBunnM']
dfformatdatefullVassendenBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'VassendenBunnS']
dfformatdatefullStraumeBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'StraumeBunnM']
dfformatdatefullStraumeBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'StraumeBunnS']
dfformatdatefullSkorveBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'SkorveBunnM']
dfformatdatefullSkorveBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'SkorveBunnS']
dfformatdatefullModaltunnelBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'ModaltunnelBunnM']
dfformatdatefullModaltunnelBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'ModaltunnelBunnS']
dfformatdatefullTrengereid = dfformatdatefull[dfformatdatefull['AntennaName']==u'Trengereid']
dfformatdatefullModalenHellandBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'ModalenHellandBunn']
dfformatdatefullHerdlaRamme = dfformatdatefull[dfformatdatefull['AntennaName']==u'HerdlaRamme']
dfformatdatefullHerdlaBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'HerdlaBunn']
dfformatdatefullGeitleBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'GeitleBunn']
dfformatdatefullFurnesRammeS = dfformatdatefull[dfformatdatefull['AntennaName']==u'FurnesRammeS']
dfformatdatefullFurnesRammeM = dfformatdatefull[dfformatdatefull['AntennaName']==u'FurnesRammeM']
dfformatdatefullFurnesRamme = dfformatdatefull[dfformatdatefull['AntennaName']==u'FurnesRamme']
dfformatdatefullEksoBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'EksoBunnS']
dfformatdatefullEksoBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'EksoBunnM']
dfformatdatefullEioPensjonatBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'EioPensjonatBunn']
dfformatdatefullEioKjerrRamme = dfformatdatefull[dfformatdatefull['AntennaName']==u'EioKjerrRamme']
dfformatdatefullEioFlyteS = dfformatdatefull[dfformatdatefull['AntennaName']==u'EioFlyteS']
dfformatdatefullEioFlyteM = dfformatdatefull[dfformatdatefull['AntennaName']==u'EioFlyteM']
dfformatdatefullEioBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'EioBunnS']
dfformatdatefullEioBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'EioBunnM']
dfformatdatefullDalevagenBunnS = dfformatdatefull[dfformatdatefull['AntennaName']==u'DalevågenBunnS']
dfformatdatefullDalemunningBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'DalemunningBunn']
dfformatdatefullDalevagenBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'DalevågenBunnM']
dfformatdatefullDalevagenBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'DalevågenBunn']
dfformatdatefullDaleelvBunnS2 = dfformatdatefull[dfformatdatefull['AntennaName']==u'DaleelvBunnS2']
dfformatdatefullDaleelvBunnS1 = dfformatdatefull[dfformatdatefull['AntennaName']==u'DaleelvBunnS1']
dfformatdatefullDaleelvBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'DaleelvBunnM']
dfformatdatefullDaleRevebruaBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'DaleRevebruaBunn']
dfformatdatefullBolstadFlyteS = dfformatdatefull[dfformatdatefull['AntennaName']==u'BolstadFlyteS']
dfformatdatefullBolstadFlyteM = dfformatdatefull[dfformatdatefull['AntennaName']==u'BolstadFlyteM']
dfformatdatefullBolstadBunnS2 = dfformatdatefull[dfformatdatefull['AntennaName']==u'BolstadBunnS2']
dfformatdatefullBolstadBunnS1 = dfformatdatefull[dfformatdatefull['AntennaName']==u'BolstadBunnS1']
dfformatdatefullBolstadBunnM = dfformatdatefull[dfformatdatefull['AntennaName']==u'BolstadBunnM']
dfformatdatefullBjoreioFlyte = dfformatdatefull[dfformatdatefull['AntennaName']==u'BjoreioFlyte']
dfformatdatefullBjoreioBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'BjoreioBunn']
dfformatdatefullArnaBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'ArnaBunn']
dfformatdatefullApeltunVannetRamme = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunVannetRamme']
dfformatdatefullApeltunS = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunS']
dfformatdatefullApeltunFToppeRamme = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunFToppeRamme']
dfformatdatefullApeltunFTnedeRamme = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunFTnedeRamme']
dfformatdatefullApeltunA4 = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunA4']
dfformatdatefullApeltunA3 = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunA3']
dfformatdatefullApeltunA2 = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunA2']
dfformatdatefullApeltunA1 = dfformatdatefull[dfformatdatefull['AntennaName']==u'ApeltunA1']
dfformatdatefullArdalSchmidtholenBunn = dfformatdatefull[dfformatdatefull['AntennaName']==u'ÅrdalSchmidthølenBunn']



antennaedict = {'ApeltunA1':dfformatdatefullApeltunA1,'ApeltunA2':dfformatdatefullApeltunA2,'ApeltunA3':dfformatdatefullApeltunA3,'ApeltunA4':dfformatdatefullApeltunA4,
'ApeltunFTnedeRamme':dfformatdatefullApeltunFTnedeRamme,'ApeltunFToppeRamme':dfformatdatefullApeltunFToppeRamme,'ApeltunS':dfformatdatefullApeltunS,'ApeltunVannetRamme':dfformatdatefullApeltunVannetRamme,
'ArnaBunn':dfformatdatefullArnaBunn,'BjoreioBunn':dfformatdatefullBjoreioBunn,'BjoreioFlyte':dfformatdatefullBjoreioFlyte,'BolstadBunnM':dfformatdatefullBolstadBunnM,
'BolstadBunnS1':dfformatdatefullBolstadBunnS1,'BolstadBunnS2':dfformatdatefullBolstadBunnS2,'BolstadFlyteM':dfformatdatefullBolstadFlyteM,'BolstadFlyteS':dfformatdatefullBolstadFlyteS,
'DaleRevebruaBunn':dfformatdatefullDaleRevebruaBunn,'DaleelvBunnM':dfformatdatefullDaleelvBunnM,'DaleelvBunnS1':dfformatdatefullDaleelvBunnS1,'DaleelvBunnS2':dfformatdatefullDaleelvBunnS2,
'DalemunningBunn':dfformatdatefullDalemunningBunn,'DalevågenBunn':dfformatdatefullDalevagenBunn,'DalevågenBunnM':dfformatdatefullDalevagenBunnM,'DalevågenBunnS':dfformatdatefullDalevagenBunnS,
u'Dalev\xe5genBunn':dfformatdatefullDalevagenBunn,u'Dalev\xe5genBunnM':dfformatdatefullDalevagenBunnM,u'Dalev\xe5genBunnS':dfformatdatefullDalevagenBunnS,
'EioBunnM':dfformatdatefullEioBunnM,'EioBunnS':dfformatdatefullEioBunnS,'EioFlyteM':dfformatdatefullEioFlyteM,'EioFlyteS':dfformatdatefullEioFlyteS,'EioKjerrRamme':dfformatdatefullEioKjerrRamme,
'EioPensjonatBunn':dfformatdatefullEioPensjonatBunn,'EksoBunnM':dfformatdatefullEksoBunnM,'EksoBunnS':dfformatdatefullEksoBunnS,'FurnesRamme':dfformatdatefullFurnesRamme,
'FurnesRammeM':dfformatdatefullFurnesRammeM,'FurnesRammeS':dfformatdatefullFurnesRammeS,'GeitleBunn':dfformatdatefullGeitleBunn,'HerdlaBunn':dfformatdatefullHerdlaBunn,
'HerdlaRamme':dfformatdatefullHerdlaRamme,'ModalenHellandBunn':dfformatdatefullModalenHellandBunn,'ModaltunnelBunnM':dfformatdatefullModaltunnelBunnM,'ModaltunnelBunnS':dfformatdatefullModaltunnelBunnS,
'SkorveBunnM':dfformatdatefullSkorveBunnM,'SkorveBunnS':dfformatdatefullSkorveBunnS,'StraumeBunnM':dfformatdatefullStraumeBunnM,'StraumeBunnS':dfformatdatefullStraumeBunnS,
'Trengereid':dfformatdatefullTrengereid,'VassendenBunnM':dfformatdatefullVassendenBunnM,'VassendenBunnS':dfformatdatefullVassendenBunnS,
'ÅrdalBunnM':dfformatdatefullArdalBunnM,'ÅrdalBunnS':dfformatdatefullArdalBunnS,u'\xc5rdalBunnM':dfformatdatefullArdalBunnM,u'\xc5rdalBunnS':dfformatdatefullArdalBunnS,
'ÅrdalSchmidthølenBunn':dfformatdatefullArdalSchmidtholenBunn,u'\xc5rdalSchmidth\xf8lenBunn':dfformatdatefullArdalSchmidtholenBunn,
'ÅrøyBunnM':dfformatdatefullAroyBunnM,'ÅrøyBunnS':dfformatdatefullAroyBunnS,u'\xc5r\xf8yBunnM':dfformatdatefullAroyBunnM,u'\xc5r\xf8yBunnS':dfformatdatefullAroyBunnS,
'ØynahølenBunnM':dfformatdatefullOynaholenBunnM,'ØynahølenBunnS':dfformatdatefullOynaholenBunnS,u'\xd8ynah\xf8lenBunnM':dfformatdatefullOynaholenBunnM,u'\xd8ynah\xf8lenBunnS':dfformatdatefullOynaholenBunnS,}

## date format yyyy-Month
#dfformatdate = dfformatdatefull.copy()
#dfformatdate["date"] = dfformatdate["date"].apply(lambda x: x.strftime('%Y-%m') if pd.notnull(x) else 'NaN') # format the date by dropping the day and keeping yyyy-Month

#-----------------------------------------------------------------------------------------
# limiting Arter to Salmo salar or Salmo trutta

def get_arter(arter):
    mydf = dfformatdatefull[dfformatdatefull["Arter"]==arter]
    return mydf

#-----------------------------------------------------------------------------------------
# limiting Arter to Salmo salar or Salmo trutta and chosen vassdrag

def get_arter_vassdrag(arter,vassdrag):
    mydf = vassdragdict[vassdrag]
    mydf = mydf[mydf["Arter"]==arter]
    return mydf

#-----------------------------------------------------------------------------------------
# limiting Arter to Salmo salar or Salmo trutta and chosen antenna, needed for the dynamically generated charts

def get_arter_antenna(arter,antenna):
    mydf = antennaedict[antenna]
    mydf = mydf[mydf["Arter"]==arter]
    return mydf

#--------------------------------------------------------------------------------------------------
# functions for groups/antennas/genericfield lists required by the dropdown menu 
# of the chart where you can select antennas/groups one by one

def get_groups_byarter(arter):
    dfdatefullarter = dfformatdatefull[dfformatdatefull["Arter"]==arter]
    groups = dfdatefullarter.groupby(["Gruppe"])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()["Gruppe"].tolist()
    del dfdatefullarter
    return groups

def get_antennas_byarter(arter):
    dfdatefullarter = dfformatdatefull[dfformatdatefull["Arter"]==arter]
    antennas = dfdatefullarter.groupby(["AntennaName"])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()["AntennaName"].tolist()
    del dfdatefullarter
    return antennas

def get_genericfield_byarter(arter,genericfield):
    dfdatefullarter = dfformatdatefull[dfformatdatefull["Arter"]==arter]
    genfieldlist = dfdatefullarter.groupby([genericfield])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()[genericfield].tolist()
    del dfdatefullarter
    return genfieldlist

#--------------------------------------------------------------------------------------------------
# functions for groups/antennas lists required by the dropdown menu 
# of the chart where you can select antennas/groups one by one + VASSDRAG

def get_groups_byartervassdrag(arter,vassdrag):
    mydf = vassdragdict[vassdrag]
    mydf = mydf[mydf["Arter"]==arter]
    groups = mydf.groupby(["Gruppe"])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()["Gruppe"].tolist()
    del mydf
    return groups

def get_antennas_byartervassdrag(arter,vassdrag):
    mydf = vassdragdict[vassdrag]
    mydf = mydf[mydf["Arter"]==arter]
    antennas = mydf.groupby(["AntennaName"])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()["AntennaName"].tolist()
    del mydf
    return antennas


#print groups
#--------------------------------------------------------------------------------------------------
# grouped dataframes for the map scatter, added latitude, longitude and label

def get_groupby_formap(arter,column):
    mydf = dfformatdatefull[dfformatdatefull["Arter"]==arter]
    groupby = mydf.groupby([column])['PIT.ID'].agg(lambda x:len(x.unique()))
    groupby = groupby.reset_index()
    del mydf
    inventedlats = np.random.uniform(low=60.3023381, high=61.397863,size=groupby.shape[0])
    inventedlons = np.random.uniform(low=4.9524332, high=7.552244,size=groupby.shape[0])
    groupby["lat"]=inventedlats
    groupby["lon"]=inventedlons
    groupby["label"] = groupby[column] + ", counts: " + groupby['PIT.ID'].map(str)
    # true coordinates when available
    for n in groupby[column].values: 
        if n in coordsdf['name'].values:
            #print n
            groupby.ix[groupby[column]==n,'lat']=coordsdf.ix[coordsdf['name']==n,'lat'].values
            groupby.ix[groupby[column]==n,'lon']=coordsdf.ix[coordsdf['name']==n,'lon'].values
    return groupby

#----------------------------------------------------------------------------------------------------------------------
# function for generative html native tables (alternative could be plotly image tables)

def generate_table(dataframe, max_rows=500):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(0,min(len(dataframe), max_rows))], style={'align-self': 'center'}
    )

############################################################################################################################
############################################################################################################################

def generate_callback(antennaname):
    @app.callback(
        dash.dependencies.Output('countsbyday-wselection-'+antennaname, 'figure'),
        [dash.dependencies.Input('arter-dropdown-day-'+antennaname, 'value'),
        dash.dependencies.Input('field-dropdown-day-'+antennaname, 'value'),
        dash.dependencies.Input('yaxis-type-day-'+antennaname, 'value'),
        dash.dependencies.Input('retain-data-'+antennaname, 'value'),
        dash.dependencies.Input('max-date-'+antennaname, 'value'),
        dash.dependencies.Input('min-date-'+antennaname, 'value')])
    def update_graph_antenna(selected_arter,selected_column, yaxis_type,retain_data, max_date, min_date):

        dfdatefull = get_arter_antenna(selected_arter,antennaname)
    
        #--------------------------------------------------------------------------
        # filter to remove duplicated PIT.IDs and retain only the FIRST recording
        if (retain_data!='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'):
            dfdatefull = dfdatefull.drop_duplicates(subset='PIT.ID', keep="first")
        #---------------------------------------------------------------------------

        min_date = pd.to_datetime(min_date)
        max_date = pd.to_datetime(max_date)
        if (min_date < dfdatefull['date'].min()) :
            min_date = dfdatefull['date'].min()
        if (max_date > dfdatefull['date'].max()) :
            max_date = dfdatefull['date'].max()
        dfdatefull = dfdatefull[dfdatefull['date'] < max_date]
        finaldf = dfdatefull[dfdatefull['date'] > min_date]
        del dfdatefull

        groupbyselectedcol = finaldf.groupby([selected_column])['PIT.ID'].agg(lambda x:len(x.unique()))     
        #print groupbyselectedcol 
        unstacked = finaldf.groupby(["date",selected_column])['PIT.ID'].agg(lambda x:len(x.unique())).unstack().reset_index()
        del finaldf

        cmap = plt.cm.get_cmap('gist_rainbow', groupbyselectedcol.shape[0]) 
        colors = []
        for i in range(cmap.N):
            rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
            colors.append(matplotlib.colors.rgb2hex(rgb))
    
        listoftraces = []
        for i in range(0,groupbyselectedcol.shape[0]) :
            value = groupbyselectedcol.reset_index()[selected_column][i]
            trace = go.Bar(x=unstacked["date"],y=unstacked[value],name=value,marker=dict(color = colors[i]))
            listoftraces.append(trace)

        return {
            'data': listoftraces,
            'layout': go.Layout(
                height=700,
                plot_bgcolor = appcolors['background'],
                paper_bgcolor = appcolors['background'],
                barmode='stack',
                font=dict(
                    family='Cabin, monospace',
                    color='#7f7f7f'
                ),
                xaxis=dict(
                    title='date',
                    tickangle = 30,
                    type='date',
                    tickformat='%Y-%m-%d',
                    titlefont=dict(
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title='PIT.IDs counts',
                    titlefont=dict(
                        size=18,
                        color='#7f7f7f'
                    ),
                    type=yaxis_type,
                ),
                margin=go.Margin(
                    b=150,
                    t=100,
                    l=100
                )
            )# end layout
        }
        return fig
############################################################################################################################


app = dash.Dash()
app.config.supress_callback_exceptions=True


appcolors = {
    'background': '#fff',
    'text': '#333',
    'grey': '#F5F5F5',
}

myfont = "Cabin"
#Londrina Shadow
fancyfont = "Days One"#"Righteous"#"Bungee Inline"#"Orbitron" #Fredoka One # Monoton #Audiowide #Fugaz One #Baloo #Titan One #Days One

#image_filename_banner = 'salmon-opaque.png'
#encoded_image_banner = base64.b64encode(open(image_filename_banner, 'rb').read())
image_filename = 'UniLogoVisRgb-transp-resized.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename2 = 'norcelogo-resized.png'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
base_page = html.Div(children=[

    html.Div([
        html.H1([
            html.Div('Fjord-Wizard',style={'textAlign': 'center', 'color': appcolors['text'], 'font-family': fancyfont,'font-size':'12rem'}),
            #html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image)),style={'float':'right','width': '15%','padding':'10px','display':'inline-block'}),
            #html.Div('FJORD-WIZARD',style={'textAlign': 'center', 'color': appcolors['text'], 'font-family': fancyfont,'font-size':'12rem'}),
            #html.Div('PIT-tag repings visualizations for you guys!',style={'textAlign': 'center','color': appcolors['text'],'font-family': fancyfont}),
        ]),
    #],style={'background-image': 'url("https://raw.githubusercontent.com/carlottanegri/PIT-TAG-database/master/salmon-opaque.png"),url()', # hosting of the file must be changed
    ],style={'background-image': 'url("https://github.com/ciphercharly/PIT-tag/blob/master/salmon-opaque.png"),url()', 
             'height': '300px',
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center',
             'padding':'10px'
             }
    ),

    ##html.Img(src='https://raw.githubusercontent.com/carlottanegri/PIT-TAG-database/master/fish.png'),
    
   
    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image),style={'float':'left','hight': '200px','padding':'10px','display':'inline-block'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image2),style={'float':'right','hight': '200px','padding':'10px','display':'inline-block'}), 
    ]),

    html.H2(children='visualizations for fish PIT tagging and tracking system',style={
        'textAlign': 'center',
        'color': appcolors['text'],
        'background':appcolors['background'],
        'font-family': myfont,'margin-top': '0.5cm','margin-bottom': '0.5cm','align-items': 'center'
    }),  


    html.Div([
        dcc.Link('Go to page 2 with extra charts and features', href='/page-2'),
    ],style={'textAlign': 'center','color': appcolors['text'],'font-family': myfont,'font-size': '2rem','padding':'10px'}),
#
#-----------------------------------------------------------------------------------------------------------
# PLOT BY DAY:  CHOOSE COLUMNS, CHOOSE ANTENNAS, text input FOR DATE RANGE, CHOOSE LINEAR OR LOG
#-----------------------------------------------------------------------------------------------------------

    html.H2(children='Counts of repings by day',style={
        'textAlign': 'center',
        'color': appcolors['background'],
        'background':appcolors['text'],
        'font-family': myfont,'padding':'10px'
    }),    
    
    html.H3(children='select the vassdrag and the arter, choose the way of grouping the data, filter the antennae and the time range',style={
        'textAlign': 'center',
        'color': appcolors['text'],
        'background':appcolors['background'],
        'font-family': myfont,'padding':'10px'
    }),    


    #
    #html.Div([
    #        html.P('select the vassdrag and the arter, choose the way of grouping the data, filter the antennae and the time range'),
    #    ],style={'textAlign': 'center','color': appcolors['text'],'font-family': myfont,'margin-top': '0.5cm','margin-bottom': '1cm'}
    #),


    html.Div([


        html.Div([
            html.Label('Choose the vassdrag:'),
            dcc.Dropdown(
                 id='vassdrag-dropdown-day-3',
                 options=[
                     {'label': 'Vosso', 'value': 'Vosso'},
                     {'label': 'Dale', 'value': 'Dale'},
                     {'label': 'Apeltun', 'value': 'Apeltun'},
                     {'label': 'Eidfjord', 'value': 'Eidfjord'},
                     {'label': 'Eksingedal', 'value': 'Eksingedal'},
                     {'label': 'Modalen', 'value': 'Modalen'},
                     {'label': 'Arna', 'value': 'Arna'},
                     {'label': 'Årdal', 'value': u'Årdal'},
                     {'label': 'Årøy', 'value': u'Årøy'},
                     {'label': 'Sjø', 'value': u'Sjø'},
                 ],
                 value='Dale',
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            html.Label('Choose arter:'),
            dcc.Dropdown(
                 id='arter-dropdown-day-3',
                 options=[
                     {'label': 'Salmo salar', 'value': 'Salmo salar'},
                     {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
                 ],
                 value='Salmo salar',
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            html.Label('Choose category for grouping the data:'),
            dcc.Dropdown(
                id='field-dropdown-day-3',
                options=[
                    {'label': 'gruppe', 'value': 'Gruppe'},
                    {'label': 'utsett sted', 'value': 'Utsett.sted'},
                    {'label': 'oppdrett', 'value': 'Opp.oppr'},
                ],
                value='Gruppe'
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            dcc.RadioItems(
                id='yaxis-type-day-3',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            dcc.RadioItems(
                id='retain-data-3',
                options=[{'label': i, 'value': i} for i in ['keep only the earliest reping for each PIT.ID (later repings won\'t show up)', 'keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'] ],
                value='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)',
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'font-weight':'bold','width': '100%','padding':'10px'}),


        html.Div([
            html.Label('Filter Antennas:'),
            dcc.Dropdown(
                id='antennas-dropdown',
                multi=True,
                #options=[{'label': i, 'value': i} for i in antennassalmo],
                #value=antennassalmo[0],
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'width': '70%','padding':'10px'}),

        html.Div([
            html.Label('text input of start and end dates to filter data format yyyy-mm-dd'),
            dcc.Input(id='min-date-3',value=abs_min_date, type='text'),
            dcc.Input(id='max-date-3',value=abs_max_date, type='text'),
            ],style={'font-family': myfont,'width': '30%','padding':'10px'}
        ),

        
    ]),
    dcc.Graph(id='countsbyday-wselection-3'),    

#-----------------------------------------------------------------------------------------------------------
# CUMULATIVE PLOT BY DAY:  CHOOSE COLUMNS, text input FOR DATE RANGE, CHOOSE LINEAR OR LOG
#-----------------------------------------------------------------------------------------------------------

    html.H2(children='Cumulative sum of counts by day',style={
        'textAlign': 'center',
        'color': appcolors['background'],
        'background':appcolors['text'],
        'font-family': myfont,'padding':'10px'
    }),    

    html.H3(children='select the vassdrag and the arter, choose the way of grouping the data, filter the antennae and the time range',style={
        'textAlign': 'center',
        'color': appcolors['text'],
        'background':appcolors['background'],
        'font-family': myfont,'padding':'10px'
    }),    



    html.Div([


        html.Div([
            html.Label('Choose the vassdrag:'),
            dcc.Dropdown(
                 id='vassdrag-dropdown-day-cum',
                 options=[
                     {'label': 'Vosso', 'value': 'Vosso'},
                     {'label': 'Dale', 'value': 'Dale'},
                     {'label': 'Apeltun', 'value': 'Apeltun'},
                     {'label': 'Eidfjord', 'value': 'Eidfjord'},
                     {'label': 'Eksingedal', 'value': 'Eksingedal'},
                     {'label': 'Modalen', 'value': 'Modalen'},
                     {'label': 'Arna', 'value': 'Arna'},
                     {'label': 'Årdal', 'value': u'Årdal'},
                     {'label': 'Årøy', 'value': u'Årøy'},
                     {'label': 'Sjø', 'value': u'Sjø'},
                 ],
                 value='Dale',
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            html.Label('Choose arter:'),
            dcc.Dropdown(
                 id='arter-dropdown-day-cum',
                 options=[
                     {'label': 'Salmo salar', 'value': 'Salmo salar'},
                     {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
                 ],
                 value='Salmo salar',
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            html.Label('Choose category for grouping the data:'),
            dcc.Dropdown(
                id='field-dropdown-day-cum',
                options=[
                    {'label': 'gruppe', 'value': 'Gruppe'},
                    {'label': 'utsett sted', 'value': 'Utsett.sted'},
                    {'label': 'oppdrett', 'value': 'Opp.oppr'},
                ],
                value='Gruppe'
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            dcc.RadioItems(
                id='retain-data-cum',
                options=[{'label': i, 'value': i} for i in ['keep only the first PIT.ID ping for all fish in the database', 'keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'] ],
                value='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)',
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'font-weight':'bold','width': '100%','padding':'10px'}),


        html.Div([
            html.Label('Filter Antennas:'),
            dcc.Dropdown(
                id='antennas-dropdown-cum',
                multi=True,
                #options=[{'label': i, 'value': i} for i in antennassalmo],
                #value=antennassalmo[0],
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'width': '70%','padding':'10px'}),

        html.Div([
            #html.Label('text input of start and end PINGING dates to filter data, format yyyy-mm-dd'),
            dcc.Markdown('''text input of start and end **PINGING** dates to filter data, format yyyy-mm-dd '''),
            dcc.Input(id='min-date-cum',value=abs_min_date, type='text'),
            dcc.Input(id='max-date-cum',value=abs_max_date, type='text'),
            ],style={'font-family': myfont,'width': '30%','padding':'10px'}
        ),
        html.Div([
            #html.Label('text input of start and end MARKING dates (based on Fangst.dato) to filter data ,format yyyy-mm-dd'),
            dcc.Markdown('''text input of start and end **MARKING** dates (based on Fangst.dato) to filter data, format yyyy-mm-dd '''),
            dcc.Input(id='min-date-fangst-cum',value=dfformatdatefull['Fangst.dato'].min(), type='text'),
            dcc.Input(id='max-date-fangst-cum',value=dfformatdatefull['Fangst.dato'].max(), type='text'),
            ],style={'font-family': myfont,'width': '50%','padding':'10px'}
        ),

        
    ]),
    dcc.Graph(id='cumulative-countsbyday-wselection'),   


#-----------------------------------------------------------------------------------------------------------
# ATTEMPT TO PUT IN EXTRA CHARTS DYNAMICALLY
#-----------------------------------------------------------------------------------------------------------
    html.H2(children='Individual charts for each antenna',style={
        'textAlign': 'center',
        'color': appcolors['background'],
        'background':appcolors['text'],
        'font-family': myfont,'padding':'10px'
    }),  

    html.Div([
            html.Label('Choose the vassdrag:'),
            dcc.Dropdown(
                 id='vassdrag-dropdown',
                 options=[
                     {'label': 'Vosso', 'value': 'Vosso'},
                     {'label': 'Dale', 'value': 'Dale'},
                     {'label': 'Apeltun', 'value': 'Apeltun'},
                     {'label': 'Eidfjord', 'value': 'Eidfjord'},
                     {'label': 'Eksingedal', 'value': 'Eksingedal'},
                     {'label': 'Modalen', 'value': 'Modalen'},
                     {'label': 'Arna', 'value': 'Arna'},
                     {'label': 'Årdal', 'value': u'Årdal'},
                     {'label': 'Årøy', 'value': u'Årøy'},
                     {'label': 'Sjø', 'value': u'Sjø'},
                 ],
                 value='Vosso',
            ),
    ],style={'font-family': myfont,'width': '20%'}),
   
    html.Div([
        html.Div(id='container'),
        html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'}),
    ],style={'font-family': myfont}),
#-----------------------------------------------------------------------------------------------------------
# MAP
#-----------------------------------------------------------------------------------------------------------
    html.H2('Map of the locations of the antennae with relative counts of pinged IDs',
            style={'font-family':myfont,'textAlign': 'center','color': appcolors['background'],'background':appcolors['text'],'padding':'10px'}
            ),
    html.Div([
        html.Label('Choose arter:'),
        dcc.Dropdown(
            id='arter-dropdown-map',
            options=[
                {'label': 'Salmo salar', 'value': 'Salmo salar'},
                {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
            ],
            value='Salmo salar'
        ),
        html.Label('Choose map style:'),
        dcc.Dropdown(
            id='mapstyle-dropdown',
            options=[
                {'label': 'dark', 'value': dark},
                {'label': 'outdoors', 'value': 'outdoors'},
                {'label': 'north star', 'value': northstar},
                {'label': 'labelmaker', 'value': labelmaker},
                {'label': 'le shine', 'value': leshine},
                {'label': 'nightly', 'value': decimal},
                {'label': 'terminal', 'value': terminal},
                {'label': 'ukiyo-e', 'value': ukiyoe},
                {'label': 'odyssey', 'value': odyssey},
            ],
            value=leshine
        ),
        ],style={'font-family': myfont,'width': '20%','margin-bottom':'1cm'}
    ),
    html.Div([
        dcc.Graph(id='map-graph'),
        ],style={'font-family': myfont,'width':'100%','margin':'0 auto'}
    ),


    #html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image)),html.Img(src='data:image/png;base64,{}'.format(encoded_image2)) ],style={'float':'center','hight': '200px','padding':'10px'}),
    #html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image2))],style={'hight': '200px','padding':'10px','display':'inline-block'}),


]) # end base-page layout
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

page_2_layout = html.Div(children=[

    html.Div([
        dcc.Link('Go back', href='/'),
    ],style={'textAlign': 'center','color': appcolors['text'],'font-family': myfont,'padding':'10px','font-size': '3rem'}),

    #-----------------------------------------------------------------------------------------------------------
    # PLOT BY DAY:  CHOOSE COLUMNS, text input FOR DATE RANGE, CHOOSE LINEAR OR LOG
    #-----------------------------------------------------------------------------------------------------------

    html.H2(children='counts by day with custom date range and custom grouping category',style={
        'textAlign': 'center',
        'color': appcolors['background'],
        'background':appcolors['text'],
        'font-family': myfont,'padding':'10px'
    }),    

    html.Div([

        html.Div([
            html.Label('Choose arter:'),
            dcc.Dropdown(
                id='arter-dropdown-day-p2',
                options=[
                    {'label': 'Salmo salar', 'value': 'Salmo salar'},
                    {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
                ],
                value='Salmo salar'
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            html.Label('Choose category for grouping:'),
            dcc.Dropdown(
                id='field-dropdown-day-p2',
                options=[
                    {'label': 'antenna name', 'value': 'AntennaName'},
                    {'label': 'vassdrag', 'value': 'Vassdrag'},
                    {'label': 'utsett sted', 'value': 'Utsett.sted'},
                    {'label': 'oppdrett', 'value': 'Opp.oppr'},
                    {'label': 'gruppe', 'value': 'Gruppe'}
                ],
                value='AntennaName'
            ),
        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            dcc.RadioItems(
                id='yaxis-type-day-p2',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='log',
                labelStyle={'display': 'inline-block'}
            )

        ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

        html.Div([
            dcc.RadioItems(
                id='retain-data-p2',
                options=[{'label': i, 'value': i} for i in ['keep only the earliest reping for each PIT.ID (later repings won\'t show up)', 'keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'] ],
                value='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)',
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'font-weight':'bold','width': '100%','padding':'10px'}),

        html.Div([
            html.Label('text input of start and end dates to filter data format yyyy-mm-dd'),
            dcc.Input(id='min-date-p2',value=abs_min_date, type='text'),
            dcc.Input(id='max-date-p2',value=abs_max_date, type='text'),
            ],style={'font-family': myfont,'width': '30%','padding':'10px'}
        ),

        
    ]),
    dcc.Graph(id='countsbyday-wselection-p2'),


    #-------------------------------------------------------------------------------------------------------------
    # DOWNLOAD INFO ON CHOSEN IDs
    #-------------------------------------------------------------------------------------------------------------
    html.H2('download database data in a csv format for chosen list of PIT.IDs ',style={'font-family':myfont,'textAlign': 'center','color': appcolors['background'],'background':appcolors['text'],'margin-top': '2cm','padding':'10px'}),
    html.Div([
        html.Label('Choose database:'),
        dcc.Dropdown(
            id='database-dropdown-download',
            options=[
                    {'label': 'marking', 'value': 'marking database'},
                    {'label': 'repings', 'value': 'repings database'},
            ],
            value='marking database'
        ),
    ],style={'font-family': myfont,'width': '20%','padding': '10px'}),

    html.Div([
            html.Label('text input of PIT.IDs separated by whitespace, e.g 982_000411521298 900_148001035916 900_228000181688'),
            dcc.Input(id='pitids-list',value='982_000411521298 900_148001035916 900_228000181688', type='text'),
    ],style={'font-family': myfont,'width': '80%','padding':'10px'}),

    html.Div([
        html.A(children='download data for selected PIT.IDs' , id='download-PITID-chosen',download="chosenPITIDinfo.csv", href="",target="_blank"),
        ],style={'textAlign': 'center','color': appcolors['text'],'font-family': myfont,'font-size': '3rem'} 
    ),
    
    html.Div([
        html.Div(children='',id='pitids-table',style={'display': 'flex','textAlign': 'center','align-items': 'center','justify-content': 'center'}), #'display': 'flex','width': '90%','padding':'10px'
    ],style={'font-family': myfont,'left': '20px','right':'20px'}),

    #-----------------------------------------------------------------------------------------------------------
    # PLOT BY AntennaName:  CHOOSE OTHER AXIS
    #-----------------------------------------------------------------------------------------------------------

    html.H2(children='simple count of repings by AntennaName',style={
        'textAlign': 'center',
        'color': appcolors['background'],
        'background':appcolors['text'],
        'font-family': myfont,'padding':'10px'
    }),

    html.Div([
        html.Label('Choose arter:'),
        dcc.Dropdown(
            id='arter-dropdown-byantennaname-p2',
            options=[
                {'label': 'Salmo salar', 'value': 'Salmo salar'},
                {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
            ],
            value='Salmo salar'
        ),
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

    html.Div([
        html.Label('Choose category for grouping:'),
        dcc.Dropdown(
            id='field-dropdown-byantennaname-p2',
            options=[
                {'label': 'utsett sted', 'value': 'Utsett.sted'},
                {'label': 'oppdrett', 'value': 'Opp.oppr'},
                {'label': 'gruppe', 'value': 'Gruppe'}
            ],
            value='Gruppe'
        ),
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

    html.Div([
        dcc.RadioItems(
                id='yaxis-type-byantennaname-p2',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='log',
                labelStyle={'display': 'inline-block'}
            )
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

    html.Div([
            dcc.RadioItems(
                id='retain-data-byantennaname-p2',
                options=[{'label': i, 'value': i} for i in ['keep only one reping for each PIT.ID', 'keep all repings, filter the unique repings by antenna (the same PIT.ID can show up for more than one antenna)'] ],
                value='keep all repings, filter the unique repings by antenna (the same PIT.ID can show up for more than one antenna)',
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'font-weight':'bold','width': '100%','padding':'10px'}),

    html.Div([
        dcc.Graph(
            id='countsbyantennaname-graph-p2',
            #animate=True
        ),
        ],style={'width':'80%','height':'90%','margin':'0 auto'}
    ),

    #-----------------------------------------------------------------------------------------------------------
    # SIMPLE COUNTS BY CHOSEN COLUMN
    #-----------------------------------------------------------------------------------------------------------
    html.H2(children='simple count of repings by a chosen field',style={
        'textAlign': 'center',
        'color': appcolors['background'],
        'background':appcolors['text'],
        'margin-top': '2cm',
        'font-family': myfont,
        'padding':'10px'
    }),

    html.Div([
        html.Label('Choose arter:'),
        dcc.Dropdown(
            id='arter-dropdown-p2',
            options=[
                {'label': 'Salmo salar', 'value': 'Salmo salar'},
                {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
            ],
            value='Salmo salar'
        ),
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

    html.Div([
        html.Label('Choose category for x-axis:'),
        dcc.Dropdown(
            id='field-dropdown-p2',
            options=[
                {'label': 'vassdrag', 'value': 'Vassdrag'},
                {'label': 'antenna name', 'value': 'AntennaName'},
                {'label': 'utsett sted', 'value': 'Utsett.sted'},
                {'label': 'oppdrett', 'value': 'Opp.oppr'},
                {'label': 'gruppe', 'value': 'Gruppe'}
            ],
            value='Vassdrag'
        ),
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

    html.Div([
        dcc.RadioItems(
                id='yaxis-type-field-p2',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='log',
                labelStyle={'display': 'inline-block','padding':'10px'}
            )

    ],style={'font-family': myfont,'width': '20%'}),

    html.Div([
            dcc.RadioItems(
                id='retain-data-field-p2',
                options=[{'label': i, 'value': i} for i in ['keep only one reping for each PIT.ID', 'keep all repings, filter the unique repings by the chosen field (the same PIT.ID can show up multiple times)'] ],
                value='keep all repings, filter the unique repings by the chosen field (the same PIT.ID can show up multiple times)',
                #labelStyle={'display': 'inline-block'}
            ),
        ],style={'font-family': myfont,'font-weight':'bold','width': '100%','padding':'10px'}),


    html.Div([
        dcc.Graph(
            id='countsbyfield-graph-p2',
            #animate=True
        ),
        ],style={'width':'80%','height':'50%','margin':'0 auto'}
    ),

    #-----------------------------------------------------------------------------------------------------------
    # EXAMPLE TABLE
    #-----------------------------------------------------------------------------------------------------------
    html.H2(children='',id='counts-table-header',style={'textAlign': 'center','color': appcolors['background'],'background':appcolors['text'],'font-family': myfont,'padding':'10px'}
    ),
    html.Div([
        html.Label('Choose arter:'),
        dcc.Dropdown(
            id='arter-dropdown-table',
            options=[
                {'label': 'Salmo salar', 'value': 'Salmo salar'},
                {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
            ],
            value='Salmo salar'
        ),
    ],style={'font-family': myfont,'width': '20%', 'padding':'10px'}),

    html.Div([
        html.Label('Choose category for grouping:'),
        dcc.Dropdown(
            id='field-dropdown-table',
            options=[
                {'label': 'antenna name', 'value': 'AntennaName'},
                {'label': 'vassdrag', 'value': 'Vassdrag'},
                {'label': 'oppdrett', 'value': 'Opp.oppr'},
                {'label': 'gruppe', 'value': 'Gruppe'},
                {'label': 'utsett sted', 'value': 'Utsett.sted'},
                {'label': 'year', 'value': 'Year'}
            ],
            value='AntennaName'
        ),
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),
    html.Div(children='',id='counts-table',style={'display': 'flex','justify-content': 'center'}),

    #-------------------------------------------------------------------------------------------------------------
    # DOWNLOAD CHOSEN RAW DATA
    #-------------------------------------------------------------------------------------------------------------
    html.H2('download aggregated data',style={'font-family':myfont,'textAlign': 'center','color': appcolors['background'],'background':appcolors['text'],'margin-top': '2cm','padding':'10px'}),
    html.Div([
        html.Label('Choose category for grouping data:'),
        dcc.Dropdown(
            id='field-dropdown-download',
            options=[
                    {'label': 'antenna name', 'value': 'AntennaName'},
                    {'label': 'vassdrag', 'value': 'Vassdrag'},
                    {'label': 'utsett sted', 'value': 'Utsett.sted'},
                    {'label': 'fangst sted', 'value': 'Fangst.sted'},
                    {'label': 'oppdrett', 'value': 'Opp.oppr'},
                    {'label': 'gruppe', 'value': 'Gruppe'}
            ],
            value='AntennaName'
        ),
    ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

    html.Div([
        html.A(children='' , id='download-chosen',download="rawdata-groupedbychosenfield.csv", href="",target="_blank"),
        ],style={'textAlign': 'center','color': appcolors['text'],'font-family': myfont,'font-size': '3.6rem'} # hosting of the file must be changed
    ),

    #html.Div([
    #    html.A('download whole raw data (not optimal yet)',href='https://www.dropbox.com/s/am08yeian4sgwon/REEDITED-allrepingsbyALLantennas-vassdrag.csv?dl=0'),
    #    ],style={'textAlign': 'center','color': appcolors['text'],'font-family': myfont,'font-size': '3.6rem'} # hosting of the file must be changed
    #),

]) # end page 2 layout
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##########################################################################################################################################################

# Update the base page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    else:
        return base_page
    # You could also return a 404 "URL not found" page here
##########################################################################################################################################################
# CALLBACKS FOR THE BASE PAGE

#first chart: counts by day selected vassdrag, filter antennas, arter dates
#------------------------------------------------------------------------------------------------------------------
@app.callback(
    dash.dependencies.Output('antennas-dropdown', 'options'),
    [dash.dependencies.Input('arter-dropdown-day-3', 'value'),
    dash.dependencies.Input('vassdrag-dropdown-day-3', 'value')])
def update_antennas_dropdown_options(selectedarter,selectedvassdrag):
    return [{'label': i, 'value': i} for i in get_antennas_byartervassdrag(selectedarter,selectedvassdrag)]

@app.callback(
    dash.dependencies.Output('antennas-dropdown', 'value'),
    [dash.dependencies.Input('arter-dropdown-day-3', 'value'),
    dash.dependencies.Input('vassdrag-dropdown-day-3', 'value')])
def update_antennas_dropdown_value(selectedarter,selectedvassdrag):
    return get_antennas_byartervassdrag(selectedarter,selectedvassdrag)#[0]


@app.callback(
    dash.dependencies.Output('countsbyday-wselection-3', 'figure'),
    [dash.dependencies.Input('arter-dropdown-day-3', 'value'),
     dash.dependencies.Input('vassdrag-dropdown-day-3', 'value'),
     dash.dependencies.Input('field-dropdown-day-3', 'value'),
     dash.dependencies.Input('antennas-dropdown', 'value'),
     dash.dependencies.Input('yaxis-type-day-3', 'value'),
     dash.dependencies.Input('retain-data-3', 'value'),
     dash.dependencies.Input('max-date-3', 'value'),
     dash.dependencies.Input('min-date-3', 'value')])
def update_graph_3(selected_arter,selected_vassdrag,selected_column, antennas_list, yaxis_type, retain_data, max_date, min_date):

    dfdatefull = get_arter_vassdrag(selected_arter,selected_vassdrag)
    
    #--------------------------------------------------------------------------
    # filter to remove duplicated PIT.IDs and retain only the FIRST recording
    if (retain_data!='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'):
        dfdatefull = dfdatefull.drop_duplicates(subset='PIT.ID', keep="first")
    #---------------------------------------------------------------------------

    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)
    if (min_date < dfdatefull['date'].min()) :
        min_date = dfdatefull['date'].min()
    if (max_date > dfdatefull['date'].max()) :
        max_date = dfdatefull['date'].max()
    dff = dfdatefull[dfdatefull['date'] < max_date]
    dff = dff[dff['date'] > min_date]
    del dfdatefull

    # we create a filtered dataframe for each gruppe and then concatenate them
    dflist = [] # list of dataframes that will be concatenated

    if (antennas_list is None):   # need a separate case for very first call when antennas_list is None
        listoftraces = []
    else:
        if isinstance(antennas_list,basestring) : # a single string i.e. a single antenna, no need to concatenate
            finaldf = dff[dff["AntennaName"]==antennas_list]
        else: # more than one string i.e. more than one antenna, need for concatenation
            for g in antennas_list:
                gdf = dff[dff["AntennaName"]==g]
                dflist.append(gdf)
            finaldf = pd.concat(dflist)
        #print finaldf.head()

        groupbyselectedcol = finaldf.groupby([selected_column])['PIT.ID'].agg(lambda x:len(x.unique()))     
        #print groupbyselectedcol 
        unstacked = finaldf.groupby(["date",selected_column])['PIT.ID'].agg(lambda x:len(x.unique())).unstack().reset_index()

        cmap = plt.cm.get_cmap('gist_rainbow', groupbyselectedcol.shape[0]) 
        colors = []
        for i in range(cmap.N):
            rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
            colors.append(matplotlib.colors.rgb2hex(rgb))
    
        listoftraces = []
        for i in range(0,groupbyselectedcol.shape[0]) :
            value = groupbyselectedcol.reset_index()[selected_column][i]
            trace = go.Bar(x=unstacked["date"],y=unstacked[value],name=value,marker=dict(color = colors[i]))
            listoftraces.append(trace)
    del dff

    return {
        'data': listoftraces,
        'layout': go.Layout(
            height=700,
            plot_bgcolor = appcolors['background'],
            paper_bgcolor = appcolors['background'],
            barmode='stack',
            font=dict(
                family='Cabin, monospace',
                color='#7f7f7f'
            ),
            xaxis=dict(
                title='date',
                tickangle = 30,
                type='date',
                tickformat='%Y-%m-%d',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='PIT.IDs counts',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                ),
                type=yaxis_type,
            ),
            margin=go.Margin(
                b=150,
                t=100,
                l=100
            )
        )# end layout
    }

# second chart CUMULATIVE sum of counts by date, grouped by selected field
#------------------------------------------------------------------------------------------------------------------
#@app.callback(
#    dash.dependencies.Output('filter-dropdown-cum', 'options'),
#    [dash.dependencies.Input('arter-dropdown-day-cum', 'value'),
#    dash.dependencies.Input('field-dropdown-day-cum', 'value')])
#def update_antennas_dropdown_options(selectedarter,selectedfield):
#    return [{'label': i, 'value': i} for i in get_genericfield_byarter(selectedarter,selectedfield)]

#@app.callback(
#    dash.dependencies.Output('filter-dropdown-cum', 'value'),
#    [dash.dependencies.Input('arter-dropdown-day-cum', 'value'),
#    dash.dependencies.Input('field-dropdown-day-cum', 'value')])
#def update_antennas_dropdown_value(selectedarter,selectedfield):
#    return get_genericfield_byarter(selectedarter,selectedfield)

@app.callback(
    dash.dependencies.Output('antennas-dropdown-cum', 'options'),
    [dash.dependencies.Input('arter-dropdown-day-cum', 'value'),
    dash.dependencies.Input('vassdrag-dropdown-day-cum', 'value')])
def update_antennas_dropdown_options(selectedarter,selectedvassdrag):
    return [{'label': i, 'value': i} for i in get_antennas_byartervassdrag(selectedarter,selectedvassdrag)]

@app.callback(
    dash.dependencies.Output('antennas-dropdown-cum', 'value'),
    [dash.dependencies.Input('arter-dropdown-day-cum', 'value'),
    dash.dependencies.Input('vassdrag-dropdown-day-cum', 'value')])
def update_antennas_dropdown_value(selectedarter,selectedvassdrag):
    return get_antennas_byartervassdrag(selectedarter,selectedvassdrag)

@app.callback(
    dash.dependencies.Output('cumulative-countsbyday-wselection', 'figure'),
    [dash.dependencies.Input('arter-dropdown-day-cum', 'value'),
     dash.dependencies.Input('vassdrag-dropdown-day-cum', 'value'),
     dash.dependencies.Input('field-dropdown-day-cum', 'value'),
     #dash.dependencies.Input('filter-dropdown-cum', 'value'),
     dash.dependencies.Input('antennas-dropdown-cum', 'value'),
     #dash.dependencies.Input('yaxis-type-day-cum', 'value'),
     dash.dependencies.Input('retain-data-cum', 'value'),
     dash.dependencies.Input('max-date-cum', 'value'),
     dash.dependencies.Input('min-date-cum', 'value'),
     dash.dependencies.Input('max-date-fangst-cum', 'value'),
     dash.dependencies.Input('min-date-fangst-cum', 'value')])
#def update_graph_1(selected_arter,selected_column, filter_list, yaxis_type, retain_data, max_date, min_date, max_date_fangst, min_date_fangst):
def update_graph_1(selected_arter,selected_vassdrag, selected_column, antennas_list, retain_data, max_date, min_date, max_date_fangst, min_date_fangst):


    yaxis_type = 'linear'

    #dfdatefull = dfformatdatefull[dfformatdatefull["Arter"]==selected_arter]
    dfdatefull = get_arter_vassdrag(selected_arter,selected_vassdrag)

    #print selected_column, filter_list
    #print selected_column, antennas_list

    #--------------------------------------------------------------------------
    # filter to remove duplicated PIT.IDs and retain only the FIRST recording
    if (retain_data)!='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)':
        dfdatefull = dfdatefull.drop_duplicates(subset='PIT.ID', keep="first")
    #---------------------------------------------------------------------------

    #filter both ping and marking dates
    #min_date = pd.to_datetime(min_date, format='%Y-%m-%d')
    #max_date = pd.to_datetime(max_date, format='%Y-%m-%d')
    #min_date_fangst = pd.to_datetime(min_date_fangst, format='%Y-%m-%d')
    #max_date_fangst = pd.to_datetime(max_date_fangst, format='%Y-%m-%d')
    max_date = pd.Timestamp(max_date)
    min_date = pd.Timestamp(min_date)
    max_date_fangst = pd.Timestamp(max_date_fangst)
    min_date_fangst = pd.Timestamp(min_date_fangst)

    #print min_date_fangst,max_date_fangst
    if (min_date < dfdatefull['date'].min()) :
        min_date = dfdatefull['date'].min()
    if (max_date > dfdatefull['date'].max()) :
        max_date = dfdatefull['date'].max()
    if (min_date_fangst < dfdatefull['Fangst.dato'].min()) :
        min_date_fangst = dfdatefull['Fangst.dato'].min()
    if (max_date_fangst > dfdatefull['Fangst.dato'].max()) :
        max_date_fangst = dfdatefull['Fangst.dato'].max()

    dfdatefull = dfdatefull[dfdatefull['date'] < max_date]
    dfdatefull = dfdatefull[dfdatefull['date'] > min_date]
    dfdatefull = dfdatefull[dfdatefull['Fangst.dato'] > min_date_fangst]
    dfdatefull = dfdatefull[dfdatefull['Fangst.dato'] < max_date_fangst]

    # we create a filtered dataframe for each member of the selected field and then concatenate them
    dflist = [] # list of dataframes that will be concatenated

    if (antennas_list is None):   # need a separate case for very first call when antennas_list is None
        listoftraces = []
    else:
        if isinstance(antennas_list,basestring) : # a single string i.e. a single antenna, no need to concatenate
            finaldf = dfdatefull[dfdatefull["AntennaName"]==antennas_list]
        else: # more than one string i.e. more than one antenna, need for concatenation
            for g in antennas_list:
                gdf = dfdatefull[dfdatefull["AntennaName"]==g]
                dflist.append(gdf)
            finaldf = pd.concat(dflist)


        #group by selected field
        groupbyselectedcol = dfdatefull.groupby([selected_column])['PIT.ID'].agg(lambda x:len(x.unique()))     
        #print groupbyselectedcol 
        unstacked = dfdatefull.groupby(["date",selected_column])['PIT.ID'].agg(lambda x:len(x.unique())).unstack().reset_index()

        # fill the NaN, necessary to display proper cumulative sum
        unstacked = unstacked.fillna(0)

        cmap = plt.cm.get_cmap('rainbow', groupbyselectedcol.shape[0]) 
        colors = []
        for i in range(cmap.N):
            rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
            colors.append(matplotlib.colors.rgb2hex(rgb))
    
        listoftraces = []
        for i in range(0,groupbyselectedcol.shape[0]) :
            value = groupbyselectedcol.reset_index()[selected_column][i]
            #print value, unstacked[value].cumsum()
            trace = go.Bar(x=unstacked["date"],y=unstacked[value].cumsum(),name=value,marker=dict(color = colors[i])) #NOTE THAT THE CUMULATIVE SUM IS ADDED HERE, ORDERING BY DATE SHOULD ALREADY BE OK
            listoftraces.append(trace)

    del dfdatefull
    del unstacked
    del groupbyselectedcol

    return {
        'data': listoftraces,
        'layout': go.Layout(
            height=700,
            plot_bgcolor = appcolors['background'],
            paper_bgcolor = appcolors['background'],
            barmode='stack',
            font=dict(
                family='Cabin, monospace',
                color='#7f7f7f'
            ),
            xaxis=dict(
                title='date',
                tickangle = 30,
                type='date',
                tickformat='%Y-%m-%d',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='PIT.IDs counts',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                ),
                type=yaxis_type,
            ),
            margin=go.Margin(
                b=150,
                t=100,
                l=100
            )
        )# end layout
    }

#---------------------------------------------------------------------------------------------------------------------
generate_callback("ApeltunA1")
generate_callback("ApeltunA2")
generate_callback("ApeltunA3")
generate_callback("ApeltunA4")
generate_callback("ApeltunFTnedeRamme")
generate_callback("ApeltunFToppeRamme")
generate_callback("ApeltunS")
generate_callback("ApeltunVannetRamme")
generate_callback("ArnaBunn")
generate_callback("BjoreioBunn")
generate_callback("BjoreioFlyte")
generate_callback("BolstadBunnM")
generate_callback("BolstadBunnS1")
generate_callback("BolstadBunnS2")
generate_callback("BolstadFlyteM")
generate_callback("BolstadFlyteS")
generate_callback("DaleRevebruaBunn")
generate_callback("DaleelvBunnM")
generate_callback("DaleelvBunnS1")
generate_callback("DaleelvBunnS2")
generate_callback("DalemunningBunn")
generate_callback("DalevågenBunn")
generate_callback("DalevågenBunnM")
generate_callback("DalevågenBunnS")
generate_callback("EioBunnM")
generate_callback("EioBunnS")
generate_callback("EioFlyteM")
generate_callback("EioFlyteS")
generate_callback("EioKjerrRamme")
generate_callback("EioPensjonatBunn")
generate_callback("EksoBunnM")
generate_callback("EksoBunnS")
generate_callback("FurnesRamme")
generate_callback("FurnesRammeM")
generate_callback("FurnesRammeS")
generate_callback("GeitleBunn")
generate_callback("HerdlaBunn")
generate_callback("HerdlaRamme")
generate_callback("ModalenHellandBunn")
generate_callback("ModaltunnelBunnM")
generate_callback("ModaltunnelBunnS")
generate_callback("SkorveBunnM")
generate_callback("SkorveBunnS")
generate_callback("StraumeBunnM")
generate_callback("StraumeBunnS")
generate_callback("Trengereid")
generate_callback("VassendenBunnM")
generate_callback("VassendenBunnS")
generate_callback("ÅrdalBunnM")
generate_callback("ÅrdalBunnS")
generate_callback("ÅrdalSchmidthølenBunn")
generate_callback("ÅrøyBunnM")
generate_callback("ÅrøyBunnS")
generate_callback("ØynahølenBunnM")
generate_callback("ØynahølenBunnS")

#------------------------------------------------------------------------------------------------------------------
@app.callback(dash.dependencies.Output('map-graph', 'figure'),
              [dash.dependencies.Input('arter-dropdown-map', 'value'),
               dash.dependencies.Input('mapstyle-dropdown', 'value')], #Input('my-slider', 'value'),
              #dash.dependencies.Input("bar-selector", "value")
              [dash.dependencies.State('map-graph', 'relayoutData')]
               #dash.dependencies.State('mapControls', 'values')
              )
#def update_graph(value, slider_value, selectedData, prevLayout, mapControls):
def update_graph(selectedarter,value,prevLayout):
    groupbyantenna = get_groupby_formap(selectedarter,'AntennaName')
    #groupbyutsettsted = get_groupby_formap(selectedarter,'Utsett.sted')
    zoom = '7'
    latInitial = 60.6276327
    lonInitial = 6.1940471
    bearing = 0
    #print value
    if (value==dark or value==decimal or value==odyssey or value==labelmaker or value==terminal):
        legendfontcol='#FFFFFF'
        starcol='#333'
    else: 
        legendfontcol=appcolors['text']
        starcol='#f0dba5'
    print prevLayout
    if(prevLayout is not None):
        if ('mapbox.zoom' in prevLayout.keys()):
            #print prevLayout
            zoom = float(prevLayout['mapbox.zoom'])
            latInitial = float(prevLayout['mapbox.center.lat'])
            lonInitial = float(prevLayout['mapbox.center.lon'])
            bearing = float(prevLayout['mapbox.bearing'])
        elif ('mapbox' in prevLayout.keys()):
            zoom = float(prevLayout['mapbox']['zoom'])
            latInitial = float(prevLayout['mapbox']['center']['lat'])
            lonInitial = float(prevLayout['mapbox']['center']['lon'])
            bearing = float(prevLayout['mapbox']['bearing'])
    return go.Figure(
        data=go.Data([
#--------------------------------------------------------------------------------
            # scatter plot for AntennaName
            go.Scattermapbox(
                lat=groupbyantenna['lat'],
                lon=groupbyantenna['lon'],
                mode='markers',
                hoverinfo="text",
                text=groupbyantenna["label"],
                marker=go.Marker(
                    size=15,
                    #color="ff0000",
                    color=groupbyantenna['PIT.ID'],
                    #colorscale='Bluered',
                    #colorscale=[[0,'ffffe0'],[0.1,'ffe6b2'],[0.2,'ffcb91'],[0.3,'ffae79'],[0.4,'fe9061'],[0.5,'f47461'],[0.6,'e75758'],[0.7,'d53c4c'],[0.8,'c0223b'],[0.9,'a70b24'],[1.0,'8b0000']],
                    colorscale = [[0,'ffa500'],[0.1,'ff8f3b'],[0.2,'fc784e'],[0.3,'f64656'],[0.4,'eb5257'],[0.5,'de3f35'],[0.6,'d12e4a'],[0.7,'c01e3d'],[0.8,'b0102e'],[0.9,'9e041b'],[1.0,'8b0000']],
                    #[[0,"E57100"],[0.1,"E16508"],[0.2,"DD5A10"],[0.3,"D94F19"],[0.4,"D54321"],[0.5,"D2382A"],[0.6,"CE2D32"],[0.7,"CA213A"],[0.8,"#C61643"],[0.9,"C20B4B"],[1.0,"#BF0054"]],
                    #'pairs' | 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' | 'Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu' 
                    #opacity=0.5,
                    colorbar=dict(
                        thicknessmode="fraction",
                        title="unique IDs <br>repinged <br>by antenna",
                        x=0.935,
                        xpad=0,
                        ypad=10,
                        nticks=10,
                        tickfont=dict(
                            color=legendfontcol
                        ),
                        titlefont=dict(
                            color=legendfontcol,
                            size=16
                        ),
                        titleside='bottom'
                    )
                ),
            ),
#-------------------------------------------------------------------------------
            # scatter plot for Utsett.sted
#            go.Scattermapbox(
#                lat=groupbyutsettsted['lat'],
#                lon=groupbyutsettsted['lon'],
#                mode='markers',
#                hoverinfo="text",
#                text=groupbyutsettsted["label"],
#                marker=go.Marker(
#                    size=10,
#                    #symbol="star",
#                    #color="ff0000",
#                    color=groupbyutsettsted['PIT.ID'],
#                    #colorscale='Greens',
#                    #colorscale = [[0,"#E5D800"],[0.1,"#CBD501"],[0.2,"#B2D202"],[0.3,"#98CF03"],[0.4,"#7FCC04"],[0.5,"#65CA05"],[0.6,"#4CC706"],[0.7,"#32C407"],[0.8,"#19C108"],[1.0,"#00BF0A"]],
#                    #colorscale = [[0,"#00B6D1"],[0.1,"#01A3CF"],[0.2,"#0391CD"],[0.3,"#047FCB"],[0.4,"#066DC9"],[0.5,"#075BC8"],[0.6,"#0948C6"],[0.7,"#0A36C4"],[0.8,"#0C24C2"],[0.9,"#0D12C0"],[1.0,"#0F00BF"]],
#                    #colorscale = [[0,"#AFA823"],[0.1,"#A0A225"],[0.2,"#929C27"],[0.3,"#849629"],[0.4,"#76902B"],[0.5,"#688A2E"],[0.6,"#5A8430"],[0.7,"#4C7E32"],[0.8,"#3E7834"],[0.9,"#307236"],[1.0,"#226D39"]],
#                    colorscale = [[0,"#DE35DC"],[0.1,"#CB32D0"],[0.2,"#B92FC4"],[0.3,"#A72DB8"],[0.4,"#952AAC"],[0.5,"#8328A0"],[0.6,"#702594"],[0.7,"#5E2288"],[0.8,"#4C207C"],[0.9,"#3A1D70"],[1.0,"#281B64"]],
#                    #opacity=0.5,
#                    colorbar=dict(
#                        thicknessmode="fraction",
#                        title="counts per Utsett.sted",
#                        x=0.065,
#                        xpad=0,
#                        nticks=24,
#                        tickfont=dict(
#                            color=legendfontcol
#                        ),
#                        titlefont=dict(
#                            color=legendfontcol
#                        ),
#                        titleside='left'
#                        )
#                ),
#            ),
#--------------------------------------------------------------------------------------
            # scatter plot of chosen locations
#            go.Scattermapbox(
#                lat=["60.397076","60.4672066","60.5703595","60.4927472","60.6566457",
#                     "60.5955851","60.6956945","60.8796681","60.6472022","60.4634718",
#                     "60.3023381","60.2861912","60.4292494","60.6266941","60.6309229"],
#                lon=["5.3245494","7.0664053","4.9524332","5.3402796","5.8020734",
#                     "5.8148608","5.9288028","5.9303579","6.1099901","7.0808155",
#                     "5.3393327","7.5588226","5.6287493","6.4170592","5.9400552"],
#                mode='markers',
#                hoverinfo="text",
#                text=["Bryggen", "Eidfjord","Herdla","Breistein","Straume",
#                      "Dale","Ekso","Modalen","Evanger","Eio",
#                      "Apeltun", "Bjoreio","Trengereid","Vossevangen","Bolstad"],
#                # opacity=0.5,
#                marker=go.Marker(
#                    size=8,
#                    color=starcol,
#                    symbol="star",
#                ),
#            ),
#------------------------------------------------------------------------------------------
        ]),
        layout=go.Layout(
            autosize=True,
            height=750,
            margin=go.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, #
                    lon=lonInitial # 
                ),
                style=value,
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': '7',
                                    'mapbox.center.lon': '6.1940471',
                                    'mapbox.center.lat': '60.6276327',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Reset Zoom',
                            method='relayout'
                        )
                    ]),
                    direction='left',
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    type='buttons',
                    x=0.45,
                    xanchor='left',
                    yanchor='bottom',
                    bgcolor='#323130',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="#FFFFFF"
                    ),
                    y=0.02
                ),
                
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '7.0664053',
                                    'mapbox.center.lat': '60.4672066',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Eidfjord',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '5.4265774',
                                    'mapbox.center.lat': '60.4061999',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Arna',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '5.95108',
                                    'mapbox.center.lat': '60.64026',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Bolstad',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '5.77',
                                    'mapbox.center.lat': '60.57',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Dale',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '6.4170592',
                                    'mapbox.center.lat': '60.6266941',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Vossevangen',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '4.9524332',
                                    'mapbox.center.lat': '60.5703595',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': value
                                }],
                            label='Herdla',
                            method='relayout'
                        ),
                    
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#FFFFFF"
                    ),
                    x=0,
                    y=0.05
                )
            ]
        )
    )
#-------------------------------------------------------------------------------------------------------------
# callback for dynamic graphs adding

@app.callback(dash.dependencies.Output('container', 'children'), 
              [dash.dependencies.Input('vassdrag-dropdown', 'value')])
def display_graphs(selected_vassdrag):

    antennalist = dfformatdatefull[dfformatdatefull['Vassdrag']==selected_vassdrag]["AntennaName"].unique().tolist()
    #antennalist = ["StraumeBunnS","StraumeBunnM"]

    graphs = []
    
    for ant in antennalist:
        graphs.append(
		html.Div([
        html.H4(children='AntennaName = '+ant,style={
            'textAlign': 'center',
            'color': appcolors['text'],
            'background':appcolors['grey'],
            'font-family': myfont,'padding':'10px'
        }),    

        html.Div([
            html.Div([
                html.Label('Choose arter:'),
                dcc.Dropdown(
                     id='arter-dropdown-day-'+ant,
                        options=[
                            {'label': 'Salmo salar', 'value': 'Salmo salar'},
                            {'label': 'Salmo trutta', 'value': 'Salmo trutta'},
                        ],
                    value='Salmo salar',
                ),
            ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

            html.Div([
                html.Label('Choose category for grouping the data:'),
                dcc.Dropdown(
                    id='field-dropdown-day-'+ant,
                    options=[
                        {'label': 'gruppe', 'value': 'Gruppe'},
                        {'label': 'utsett sted', 'value': 'Utsett.sted'},
                        {'label': 'oppdrett', 'value': 'Opp.oppr'},
                    ],
                    value='Gruppe'
                ),
            ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

            html.Div([
                dcc.RadioItems(
                    id='yaxis-type-day-'+ant,
                    options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                    value='linear',
                    labelStyle={'display': 'inline-block'}
                ),
            ],style={'font-family': myfont,'width': '20%','padding':'10px'}),

            html.Div([
                dcc.RadioItems(
                    id='retain-data-'+ant,
                    options=[{'label': i, 'value': i} for i in ['keep only the first PIT.ID ping for all fish in the database', 'keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'] ],
                    value='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)',
                    #labelStyle={'display': 'inline-block'}
                ),
            ],style={'font-family': myfont,'width': '100%','font-weight':'bold','padding':'10px'}),

            html.Div([
                html.Label('text input of start and end dates to filter data format yyyy-mm-dd'),
                dcc.Input(id='min-date-'+ant,value=antennaedict[ant.decode('utf-8')]['date'].min(), type='text'),
                dcc.Input(id='max-date-'+ant,value=antennaedict[ant.decode('utf-8')]['date'].max(), type='text'),
                ],style={'font-family': myfont,'width': '30%','padding':'10px'}
            ),
        ]),
        dcc.Graph(id='countsbyday-wselection-'+ant)
		]) # end outer div
		) # close append
    return html.Div(graphs)
##########################################################################################################################################################
# CALLBACKS FOR THE SECOND PAGE

@app.callback(
    dash.dependencies.Output('download-PITID-chosen', 'children'),
    [dash.dependencies.Input('database-dropdown-download', 'value')])
def update_pitid_downloader_header(databasestring): 
    return "download table with the selected PIT.IDs from " + databasestring

@app.callback(
    dash.dependencies.Output('pitids-table', 'children'),
    [dash.dependencies.Input('database-dropdown-download', 'value'),
     dash.dependencies.Input('pitids-list', 'value')])
def update_pitids_table(databasestring,stringwlist): 
    if databasestring=='repings database':   
        dff = dfformatdatefull
        filterdf =  dff[dff['PIT.ID'].isin(stringwlist.split())][[u'PIT.ID',u'Arter','Vassdrag',u'Fangst.dato',u'Fangst.metode',u'Fangst.sted',
             u'MarkingFileName',u'Utsett.sted',u'Gruppe',u'Gr.størrelse',u'AntennaFileName',u'AntennaName',u'date',u'time']]
    else:
        dff = dfmarking
        filterdf =  dff[dff['PIT.ID'].isin(stringwlist.split())][[u'PIT.ID',u'Arter',u'Fangst.dato',u'Fangst.metode',u'Fangst.sted',
             u'MarkingFileName',u'Utsett.sted',u'Gruppe',u'Gr.størrelse']]
    del dff
    
    return generate_table(filterdf)

@app.callback(
    dash.dependencies.Output('download-PITID-chosen', 'href'),
    [dash.dependencies.Input('database-dropdown-download', 'value'),
     dash.dependencies.Input('pitids-list', 'value')])
def update_pitid_downloader(databasestring,stringwlist): 
    print stringwlist.split()
    if databasestring=='repings database':   
        df = dfformatdatefull
    else:
        df = dfmarking
    #print df
    filtereddf =  df[df['PIT.ID'].isin(stringwlist.split())]
    del df
    csvString = filtereddf.to_csv(index=False,encoding='latin-1')
    del filtereddf
    csvString = "data:text/csv;charset=utf-8," + urllib.quote(csvString)
    return csvString

#------------------------------------------------------------------------------------------------------------------
@app.callback(
    dash.dependencies.Output('countsbyday-wselection-p2', 'figure'),
    [dash.dependencies.Input('arter-dropdown-day-p2', 'value'),
     dash.dependencies.Input('field-dropdown-day-p2', 'value'),
     dash.dependencies.Input('yaxis-type-day-p2', 'value'),
     dash.dependencies.Input('retain-data-p2', 'value'),
     dash.dependencies.Input('max-date-p2', 'value'),
     dash.dependencies.Input('min-date-p2', 'value')])
def update_graph_bydate_p2(selected_arter,selected_column, yaxis_type, retain_data, max_date, min_date):

    dfdatefull = get_arter(selected_arter)
    
    #--------------------------------------------------------------------------
    # filter to remove duplicated PIT.IDs and retain only the FIRST recording
    if (retain_data!='keep all repings, filter the unique repings by day (the same PIT.ID can show up on multiple dates)'):
        dfdatefull = dfdatefull.drop_duplicates(subset='PIT.ID', keep="first")
    #---------------------------------------------------------------------------

    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)
    if (min_date < dfdatefull['date'].min()) :
        min_date = dfdatefull['date'].min()
    if (max_date > dfdatefull['date'].max()) :
        max_date = dfdatefull['date'].max()

    dfdatefull = dfdatefull[dfdatefull['date'] < max_date]
    dfdatefull = dfdatefull[dfdatefull['date'] > min_date]

    groupbyselectedcol = dfdatefull.groupby([selected_column])['PIT.ID'].agg(lambda x:len(x.unique()))     
    unstacked = dfdatefull.groupby(["date",selected_column])['PIT.ID'].agg(lambda x:len(x.unique())).unstack().reset_index()
    del dfdatefull

    cmap = plt.cm.get_cmap('gist_rainbow', groupbyselectedcol.shape[0]) 
    colors = []
    for i in range(cmap.N):
        rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
        colors.append(matplotlib.colors.rgb2hex(rgb))
    
    listoftraces = []
    for i in range(0,groupbyselectedcol.shape[0]) :
        value = groupbyselectedcol.reset_index()[selected_column][i]
        trace = go.Bar(x=unstacked["date"],y=unstacked[value],name=value,marker=dict(color = colors[i]))
        listoftraces.append(trace)

    return {
        'data': listoftraces,
        'layout': go.Layout(
            height=700,
            plot_bgcolor = appcolors['background'],
            paper_bgcolor = appcolors['background'],
            barmode='stack',
            font=dict(
                family='Cabin, monospace',
                color='#7f7f7f'
            ),
            xaxis=dict(
                title='date',
                tickangle = 30,
                type='date',
                tickformat='%Y-%m-%d',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='PIT.IDs counts',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                ),
                type=yaxis_type,
            ),
            margin=go.Margin(
                b=150,
                t=100,
                l=100
            )
        )# end layout
    }

#------------------------------------------------------------------------------------------------------------------

@app.callback(
    dash.dependencies.Output('countsbyfield-graph-p2', 'figure'),
    [dash.dependencies.Input('arter-dropdown-p2', 'value'),
     dash.dependencies.Input('field-dropdown-p2', 'value'),
     dash.dependencies.Input('yaxis-type-field-p2', 'value'),
     dash.dependencies.Input('retain-data-field-p2', 'value')])

def update_graph_countsbyfiels_p2(selectedarter,selectedcol,yaxis_type,retain_data):

    mydf = get_arter(selectedarter)
   
    #--------------------------------------------------------------------------
    # filter to remove duplicated PIT.IDs and retain only the FIRST recording
    if (retain_data!='keep all repings, filter the unique repings by the chosen field (the same PIT.ID can show up multiple times)'):
        mydf = mydf.drop_duplicates(subset='PIT.ID', keep="first")
    #---------------------------------------------------------------------------

    groupbyselcol = mydf.groupby([selectedcol])['PIT.ID'].agg(lambda x:len(x.unique()))
    del mydf
    reset = groupbyselcol.reset_index()
        
    trace = go.Bar(x=reset[selectedcol],y=reset["PIT.ID"],marker=dict(color = '#9900ff'))
    
    xaxislayout = dict(
        title=selectedcol,
        tickangle = 30,
        titlefont=dict(
            size=18,
            color='#7f7f7f'
        )
    )

    return {
        'data': [trace],
        'layout': go.Layout(
            height=700,
            plot_bgcolor = appcolors['background'],
            paper_bgcolor = appcolors['background'],
            barmode='stack',
            font=dict(
                family='Cabin, monospace',
                color='#7f7f7f'
            ),
            xaxis=xaxislayout,
            yaxis=dict(
                title='PIT.IDs counts',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                ),
                type=yaxis_type,
            ),
            margin=go.Margin(
                b=200,
                t=100,
                l=150,
                r=150
            )
        )# end layout
    }


#---------------------------------------------------------------------------------------------------------
@app.callback(
    dash.dependencies.Output('countsbyantennaname-graph-p2', 'figure'),
    [dash.dependencies.Input('arter-dropdown-byantennaname-p2', 'value'),
     dash.dependencies.Input('field-dropdown-byantennaname-p2', 'value'),
     dash.dependencies.Input('yaxis-type-byantennaname-p2', 'value'),
     dash.dependencies.Input('retain-data-byantennaname-p2', 'value')])
def update_graph_countsbyantennaname_p2(selectedarter,selectedcol,yaxis_type,retain_data):

    mydf = get_arter(selectedarter)

    #--------------------------------------------------------------------------
    # filter to remove duplicated PIT.IDs and retain only the FIRST recording
    if (retain_data!='keep all repings, filter the unique repings by antenna (the same PIT.ID can show up for more than one antenna)'):
        mydf = mydf.drop_duplicates(subset='PIT.ID', keep="first")
    #---------------------------------------------------------------------------

    unstacked = mydf.groupby(["AntennaName",selectedcol])['PIT.ID'].agg(lambda x:len(x.unique()))
    del mydf
    unstacked = unstacked.unstack().reset_index()

    cmap = plt.cm.get_cmap('gist_rainbow', len(unstacked.columns.values[1:])) 
    colors = []
    for i in range(cmap.N):
        rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
        colors.append(matplotlib.colors.rgb2hex(rgb))
    
    listoftraces = []
    for i in range(0,len(unstacked.columns.values[1:])) :
        value = unstacked.columns.values[1+i]
        #print valuec
        trace = go.Bar(x=unstacked["AntennaName"],y=unstacked[value],name=value,marker=dict(color = colors[i]))
        listoftraces.append(trace)

    del unstacked
    
    return {
        'data': listoftraces,
        'layout': go.Layout(
            height=700,
            plot_bgcolor = appcolors['background'],
            paper_bgcolor = appcolors['background'],
            barmode='stack',
            font=dict(
                family='Cabin, monospace',
                color='#7f7f7f'
            ),
            #title='Counts by ' + selectedcol + ' limited to Arter = Salmo salar, repings in all years of all years marking data ',
            xaxis=dict(
                title="AntennaName",
                tickangle = 35,
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='PIT.IDs counts',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                ),
                type=yaxis_type,
            ),
            margin=go.Margin(
                b=150,
                t=100,
                l=100
            )
        )# end layout
    }

#-------------------------------------------------------------------------------------------------------------
@app.callback(
    dash.dependencies.Output('download-chosen', 'children'),
    [dash.dependencies.Input('field-dropdown-download', 'value')])
def update_downloader_header(selcol): 
    return "repings database grouped by column " + selcol

@app.callback(
    dash.dependencies.Output('download-chosen', 'href'),
    [dash.dependencies.Input('field-dropdown-download', 'value')])
def update_downloader(selcol): 
    groupedf = dfformatdatefull.groupby([selcol])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index()
    csvString = groupedf[[selcol,'PIT.ID']].to_csv(index=False,encoding='utf-8')
    del groupedf
    csvString = "data:text/csv;charset=utf-8," + urllib.quote(csvString)
    return csvString
#------------------------------------------------------------------------------------------------------------------
@app.callback(
    dash.dependencies.Output('counts-table-header', 'children'),
    [dash.dependencies.Input('field-dropdown-table', 'value')])
def update_table_header(selcol): 
    return 'example table: unique PIT.ID repings by ' + selcol

@app.callback(
    dash.dependencies.Output('counts-table', 'children'),
    [dash.dependencies.Input('arter-dropdown-table', 'value'),
     dash.dependencies.Input('field-dropdown-table', 'value')])
def update_table(selarter,selcol): 
    dftable = pd.DataFrame( get_arter(selarter).groupby([selcol])['PIT.ID'].agg(lambda x:len(x.unique())).reset_index(), columns=[selcol,'PIT.ID'] )
    #print dftable    
    return generate_table(dftable)

##########################################################################################################################################################

#-----------------------------------------------------------------------------------------------------------------
external_css = [ "https://codepen.io/chriddyp/pen/bWLwgP.css","https://fonts.googleapis.com/css?family=Days One"]#,Righteous Bungee+Inline|Russo+One "Monoton"#"Righteous"#"Bungee Inline"#"Orbitron" #Fredoka One # Monoton #Audiowide #Fugaz One #Baloo #Titan One #Days One

# "https://fonts.googleapis.com/css?family=Londrina+Solid"]
# "https://afeld.github.io/emoji-css/emoji.css"
# "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css","fontcss.css"]

for css in external_css: 
    app.css.append_css({ "external_url": css })

#my_js_url = 'https://gist.github.com/hamxiaoz/a664f52e34c22f2be83f.js'
#app.scripts.append_script({
#    "external_url": my_js_url
#})

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='129.177.18.253', port='8050',debug=True)

