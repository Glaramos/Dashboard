import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#Page configuration
st.set_page_config(
    page_title= "DELIVERY DATA",   
    page_icon= "logistics-delivery.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

#st.header('')

#CSS styling
st.markdown("""
<style>
         
[data-testid="block-container]{
            padding-lef: 2rem;
            padding-right: 2rem;
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-bottom:-7rem;
}  
[data-testid="stVerticalBlock]{
            padding-lef: 0rem;
            padding-righr: 0rem;
}    
[data-testid="stMertic]{
            background-color: #393939;
            text-alig: center;
            padding: 15px 0;
}    
[data-testid="stMerticLabel"]{
            display: flex;
            justify-content: center;
            align-itmes: center;
}    
[data-testid="stMerticDeltaIcon-up"]{
            position: relative;
            left: 38%;
            -webkit-transform: translateX(-50);
            -ms-transform: translateX(-50);
            transform: translateX(-50);
}    
[data-testid="stMerticDeltaIcon-Down"]{
            position: relative;
            left: 38%;
            -webkit-transform: translateX(-50);
            -ms-transform: translateX(-50);
            transform: translateX(-50);
}    
   </style>
            """,unsafe_allow_html=True)

#data
df = pd.read_csv('Delivery Data3.csv', sep=';')

#Slidebar
with st.sidebar:
    st.image( './logistics-delivery.png')
    # st.image("https://www.pixenli.com/image/fm0aEpMI", width=150)
    st.title('Delivery Dashboard')

    # #Select years of data
    df['fecha_envio'] = pd.to_datetime(df['fecha_envio'], format= '%d/%m/%Y')
    df_sorted = df.sort_values('fecha_envio')
    years_unique = df['fecha_envio'].dt.year.unique()
    year_list = list(map(str,years_unique))
    select_year = 2020
    select_year = st.selectbox('Seleccione el Año', year_list)
    df_selected_year = df[df['fecha_envio'].dt.year == int(select_year)]


    st.metric(label='Número de Registro', value= df_selected_year.shape[0], delta =None)
    with st.expander('', expanded=True):

        st.write(  ''' :orange[**A cerca del contenido**]: Este conjunto de datos proporciona una vision detallada
            de las transacciones de ventas y comercio electronico.
            Cada entrada en el dataset representa una transacción unica, con información valiosa
            sobre productos, cliente y regiones. '''
    )


df.columns = ["Codigo",	"Fecha de envio","Proveedor","Prioridad","Cantidad","Ventas","Descuento","Modo de envio","Margen","Utilidad","Precio de venta","Precio de costo","Costo de envio","Nombre de cliente","Región","Segmento","Categoría","Subcategoria"]
df["Ventas"] = df["Ventas"].map("$ {}".format)
df["Precio de venta"] = df["Precio de venta"].map("$ {}".format)
df["Precio de costo"] = df["Precio de costo"].map("$ {}".format)
df["Costo de envio"] = df["Costo de envio"].map("$ {}".format)
df["Descuento"] = df["Descuento"].map("{} %".format)
df["Margen"] = df["Margen"].map("{} %".format)
df["Utilidad"] = df["Utilidad"].map(" $ {}".format)

# def style(data):
#     data.style.bar(subset=['Ventas'], color='blue')
#     return data


st.write('''### Datos''')
st.dataframe(df) 
 
#visualizaciones



#1
def make_tree_map(data):
    fig = px.treemap(data, path = ['Nombre_cliente','Categoria','Subcategoria','Cantidad'], values ='Costo_envio', 
                 color ='Ventas', color_continuous_scale ='viridis', 
                )
    return fig
#2
def make_pie(data):
    fig = px.pie(data, values='Cantidad', names = 'Categoria', 
             hover_data = ['Costo_envio'],
             labels={'Costo_envio': 'Costo_envio'})
    return fig
#3
def make_sunburst(data):
    fig = px.sunburst(data, path=['Categoria','Subcategoria'],
                 labels={'Categoria': 'Subcategoria'})
    return fig
#4
def make_sunburst(data):
    fig = px.sunburst(data, path=['Prioridad','Categoria'],
                 labels={'Categoria': 'Categoria'})
    return fig
#5
def make_time_line(data):
    fig = px.line(df, x='Fecha de envio', y='Ventas', color='Prioridad')
    return fig

#Dashboard Main Panel
col= st.columns((0.1,2.25,2.25), gap='medium')

with col[1]:
    st.markdown('#### Relación entre Cliente y Categorías')
    treemap = make_tree_map(df_selected_year)
    st.plotly_chart(treemap, use_container_width=True)

    st.markdown('#### Prioridad de envios por Categorías')

    sun = make_sunburst(df_selected_year)
    st.plotly_chart(sun, use_container_width=True)

with col[2]:
    st.markdown('#### Porcentaje de Envios y Costos por Región')
    pie = make_pie(df_selected_year)
    st.plotly_chart(pie, use_container_width=True)

    st.markdown('####  Prioridad y Categorías')
    time_line = make_time_line(df_selected_year)
    st.plotly_chart(time_line, use_container_width=True)