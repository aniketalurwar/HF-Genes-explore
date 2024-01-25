import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
st.set_page_config(layout="wide")


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

st.markdown("<h1 style='text-align: center; color: #0096FF;'>Knowledge Graph per Type</h1>", unsafe_allow_html=True)

plot_df1=plot_df


filt = st.checkbox("Filter by Subtype?")


if filt:
    plot_df1.Node == option1

    nodes = []
    edges = []

    df_genes = dict()
    for k, v in plot_df1.groupby('Gene'):
        df_genes[k] = v
    for i in df_genes:
        nodes.append( Node(id=i, 
                    label=i, 
                    size=15
                    )
                ) # includes **kwargs
    df_nodes = dict()
    for kk, vv in plot_df1.groupby('Node'):
        df_nodes[kk] = vv
    for j in df_nodes:
        nodes.append( Node(id=j, 
                    #label=j, 
                    size=15
                    )
                ) # includes **kwargs
    for index, row in plot_df.iterrows():
        
        edges.append( Edge(source=row['Gene'], 
                    label="--", 
                    target=row['Node'], 
                    # **kwargs
                    ) 
                ) 

    config = Config(width=1050,
                    height=1050,
                    directed=True, 
                    #physics=True, 
                    hierarchical=False,
                    collapsible=True,
                    # **kwargs
                    )

    return_value = agraph(nodes=nodes, 
                        edges=edges, 
                        config=config)