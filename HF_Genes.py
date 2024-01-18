import streamlit as st

import pandas as pd


df = pd.read_csv(r'./121geneneighboursbyprotein.csv')

types_u = []

types_u = df['Type'].unique()

with st.sidebar: 
    option = st.selectbox(
    'Please select your Type:',
    types_u)

plot_df = df[df.Type == option]



res = plot_df['Node'].value_counts()\
                 .to_frame('protein_count').rename_axis('Node')\
                 .reset_index()

text_title = 'HFpEF/HFrEF Genes'

st.markdown("<h1 style='text-align: center; color: #0096FF;'>HFpEF/HFrEF Genes</h1>", unsafe_allow_html=True)

html_str = f""" <h1 style='text-align: center; color: #0096FF;'> Explore {option} Option </h1> """

st.markdown(html_str, unsafe_allow_html=True)

st.bar_chart(res,x="Node", y="protein_count", color="protein_count",)


option1 = st.selectbox(
'Please select your Sub Type:',
plot_df['Node'].unique())

table_df = plot_df[plot_df.Node == option1]

table_df.rename(columns = {'Gene':'Protein Name'}, inplace = True) 

st.dataframe(table_df)