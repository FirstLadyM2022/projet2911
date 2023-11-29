import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from streamlit_lottie import st_lottie
import requests

def render_animation():
    animation_response = requests.get('https://lottie.host/c17d5978-9bf0-4a87-8bdf-66dae56508f3/olQqpxxFMn.json')
    animation_json = dict()
    
    if animation_response.status_code == 200:
        animation_json = animation_response.json()
    else:
        print("Error in the URL")     
                        
    return st_lottie(animation_json, height=200, width=300)

st.title('Vous avez vu un film qui vous a plu?')

st.write("On vous aidera de trouver les meilleurs films pareils!")

df_test = pd.read_csv('filtered_data_images1.csv', sep=',')
#df_test

def recommendation(nom_film):
    try:
        index_film = df_test[df_test['primaryTitle']==nom_film].index[0]
        groupe = df_test.loc[index_film, 'groupe']
        df_recommendation = df_test[df_test['groupe']== groupe].drop(index_film)
        df_recommendation = df_recommendation.sort_values(by='numVotes', ascending=False).head(3)
        return df_recommendation
    except:
        return "Entrez le titre valide du film pour voir les recommendations"


if "input" not in st.session_state:
    st.session_state.input = ""
def input_callback():
    st.session_state.input = st.session_state.my_input
user_input = st.text_input("Entrer le nom du film: ", key="my_input",on_change=input_callback,args=None)

#st.text("your input is : " + st.session_state.my_input)
#st.text("your input is: " + st.session_state.input)
if user_input:
    if isinstance(recommendation(st.session_state.my_input), str):
        st.write("Entrez le titre valide du film pour voir les recommendations")
    else:
        df = recommendation(st.session_state.my_input).reset_index()
        #df
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)


        with st.container():
            c1.image('https://image.tmdb.org/t/p/w500'+df['backdrop_path'][0], use_column_width=True)
            c2.image('https://image.tmdb.org/t/p/w500'+df['backdrop_path'][1], use_column_width=True)
            c3.image('https://image.tmdb.org/t/p/w500'+df['backdrop_path'][2], use_column_width=True)
        with st.container():
            c4.header(df['primaryTitle'][0])
            c5.header(df['primaryTitle'][1])
            c6.header(df['primaryTitle'][2])

st.header("Les moyens de machine learning utilisés:")
st.write("Nous avons effectué du clustering sur la base de donnée nettoyer, afin d'identifier les groupes de films pareils. L'algoritme identifie le cluster du film rentré et propose les films les plus connus de ce cluster.")
#st.header("Les axes d'améliorations:")
#st.write("Changer le clusters")
if st.button("wanna see some magic ?"):
    render_animation()

    #for ind in df.index:
        #st.text("Movie title: "+df['primaryTitle'][ind])
        #st.image('https://image.tmdb.org/t/p/w500'+df['backdrop_path'][ind], width=200)
    #col1,col2,col3 = st.beta_columns(2)
    #col1.success("Movie title: "+df['primaryTitle'][0])
    #col1.button("Hello")
    #col2.success("Movie title: "+df['primaryTitle'][1])
    #col3.success("Movie title: "+df['primaryTitle'][2])


    #grid = st.grid()
    #for ind in df.index:
        #row = grid.row()
        # Now you can use row.foo() to do the same as st.foo(), but 
        # the elements you insert will all go inside a horizontal
        # container.
        #row.image('https://image.tmdb.org/t/p/w500'+df['backdrop_path'][ind])
        #row.text("Movie title: "+df['primaryTitle'][ind])
