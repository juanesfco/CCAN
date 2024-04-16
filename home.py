import streamlit as st
import pandas as pd
import io
import os
import requests

def do_stuff_on_page_load():
    st.set_page_config(layout="wide")

do_stuff_on_page_load()

st.markdown(f'''
<style>
.appview-container .main .block-container{{
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;    }}
</style>
''', unsafe_allow_html=True,
)

st.title('CCAN Trigger Web App')
st.markdown('***')

if st.button('Show'):

    url = 'https://indicadores.pr/dataset/49746389-12ce-48f6-b578-65f6dc46f53f/resource/8025f821-45c1-4c6a-b2f4-8d641cc03df1/download/aee-meta-ultimo.csv'
    s=requests.get(url,verify=False).content
    df_aee=pd.read_csv(io.StringIO(s.decode('latin-1')), thousands=',')

    df_aee1 = df_aee[['Mes','      Generación Neta  (mkWh)     ','Generación Neta con Hidroeléctrica (mkWh)',
        'Generación con energía comprada-Fotovoltaica (mkWh)','Generación con energía comprada-Eólica (mkWh)']]
    df_aee1['Renewable Energy Net Generation (mkWh)'] = df_aee1.iloc[:,2:5].sum(axis=1)

    month = df_aee1['Mes'].values
    netGeneration = df_aee1['      Generación Neta  (mkWh)     '].values
    renewableNetGeneration = df_aee1['Renewable Energy Net Generation (mkWh)'].values

    df_aee2 = pd.DataFrame({'month':month,'ind_11':renewableNetGeneration/netGeneration*100})
    df_aee2['month'] = pd.to_datetime(df_aee2['month'])

    df_aee2.to_csv('data/df_aee.csv',index=False)

    st.write(os.stat('data/df_aee.csv').st_mtime)