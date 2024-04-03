import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
st.set_page_config(layout="wide")

from streamlit_agraph.config import Config, ConfigBuilder




final_vd = pd.read_csv(r'./final_top5.csv')

with st.sidebar: 
    option = st.selectbox(
    'Please select CV Disease Type:',
    ('CVA','IHD','CM','ARR','VD','CHD'))

final_coll = final_vd[final_vd.Condition == option]

final_arr_short= final_coll



nodes = []
edges = []
#final_genes = pd.DataFrame(final_arr.Gene.unique(),columns=['Nodes'])
#final_condition = pd.DataFrame(final_arr.Condition.unique(),columns=['Nodes'])
#final_disease = pd.DataFrame(final_arr.neighbour_name.unique(),columns=['Nodes'])
#final_plot = pd.concat([final_genes,final_condition,final_disease])
df_genes = dict()
df_genes=dict(enumerate(final_arr_short.Protein.unique()))
for i in df_genes:
            nodes.append( Node(id=df_genes[i], 
                        label=df_genes[i], 
                        size=40,
                        shape="diamond",
                        color='#00008B'
                        )
                    ) # includes **kwargs
#df_disease = dict()
#df_disease=dict(enumerate(final_arr.neighbour_name.unique()))
df_disease = pd.DataFrame(final_arr_short.neighbour_name.value_counts().reset_index().values, columns=["name", "count"])
df_disease = df_disease.sort_index(axis = 0, ascending=True)
for index, row in df_disease.iterrows():
#    print(row['count'])
#for j in df_disease:
            nodes.append( Node(id=row['name'], 
                        label=row['name'], 
                        size=15 * row['count'],
                        shape="square",
                        color='#bf9b30'
                        )
                    ) # includes **kwargs
df_condition = dict()
df_condition=dict(enumerate(final_arr_short.Condition.unique()))
for k in df_condition:
            nodes.append( Node(id=df_condition[k], 
                        label=f"          {option}          ", 
                        size=200,
                        shape="circle",
                        color='#00FFFF'
                        )
                    ) # includes **kwargs

df_connections = final_arr_short.filter(items=['Protein', 'neighbour_name']).drop_duplicates()
for index, row in df_connections.iterrows():           
        edges.append( Edge(source=row['Protein'], 
                        label="--", 
                        target=row['neighbour_name'], 
                        # **kwargs
                        ) 
                    ) 
        
df_mconnections = final_arr_short.filter(items=['Protein', 'Condition']).drop_duplicates()
for index, row in df_mconnections.iterrows():         
        edges.append( Edge(source=row['Condition'], 
                        label="--", 
                        target=row['Protein'], 
                        # **kwargs
                        ) 
                    ) 
# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# 2. If your done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")



return_value = agraph(nodes=nodes, 
                        edges=edges, 
                        config=config)
