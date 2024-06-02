import streamlit as st
import pickle
from datetime import datetime
import math
import pandas as pd
startTime = datetime.now()

## Getting our model
filename = "gamesModelLoL.pkl"
model = pickle.load(open(filename,'rb'))

## Setting first radio options (left side), not displayed yet
firstBlood_d = {0:"Noone has first blood yet", 1:"Your team gets first blood", 2:"Enemy team gets first blood"}
firstTower_d = {0:"Noone has first tower yet", 1:"Your team gets first tower", 2:"Enemy team gets first tower"}
firstInhibitor_d = {0:"Noone has first inhibitor yet", 1:"Your team get first inhibitor", 2:"Enemy team gets first inhibitor"}
firstBaron_d = {0:"Noone gets first baron", 1:"Your team gets first baron", 2:"Enemy team gets first baron"}
firstDragon_d = {0:"Noone gets first dragon", 1:"Your team gets first dragon", 2:"Enemy team gets first dragon"}
firstRiftHerald_d = {0:"Noone gets first herald", 1:"Your team gets first herald", 2:"Enemy team gets first herald"}

## Turning the Json with champion names/ID's to a dataframe for easier manipulation
import json

champs = pd.read_json("champion_info.json")
champs = champs.T
champs['name'] = champs['name'].str.lower()

def main():

    ## Setting up the general streamlit page
    st.set_page_config(page_title="LoL Games Calculator")
    st.image("PAD Project Logo.jpg")
    overview = st.container()
    left, right = st.columns(2)
    prediction = st.container()


    with overview:
        st.title("League of Legends Win Calculator")

    ## Displaying radio buttons on left side
    with left:
        firstBlood_radio = st.radio("First blood", list(firstBlood_d.keys()),format_func=lambda x : firstBlood_d[x])
        firstTower_radio = st.radio("First tower", list(firstTower_d.keys()),format_func=lambda x : firstTower_d[x])
        firstInhibitor_radio = st.radio("First inhibitor", list(firstInhibitor_d.keys()),format_func=lambda x : firstInhibitor_d[x])
        firstBaron_radio = st.radio("First baron", list(firstBaron_d.keys()),format_func=lambda x : firstBaron_d[x])
        firstDragon_radio = st.radio("First dragon", list(firstDragon_d.keys()),format_func=lambda x : firstDragon_d[x])
        firstRiftHerald_radio = st.radio("First rift herald", list(firstRiftHerald_d.keys()),format_func=lambda x : firstRiftHerald_d[x])
        
    ## Displaying options on right side (game duration, champions, objective amount)
    with right:
        gameDuration_slider = st.slider("Game duration (10 minute intervals)", min_value=1,max_value=6,step=1)
        
        for i in range(1,5):
                st.write(" ")
                
        with st.popover("Team one"):
            champ1 = st.number_input("Champion 1 ID", min_value=1,max_value=700,step=1)
            champ2 = st.number_input("Champion 2 ID", min_value=1,max_value=700,step=1)
            champ3 = st.number_input("Champion 3 ID", min_value=1,max_value=700,step=1)
            champ4 = st.number_input("Champion 4 ID", min_value=1,max_value=700,step=1)
            champ5 = st.number_input("Champion 5 ID", min_value=1,max_value=700,step=1)
        with st.popover("Team two"):
            champ6 = st.number_input("Champion 6 ID", min_value=1,max_value=700,step=1)
            champ7 = st.number_input("Champion 7 ID", min_value=1,max_value=700,step=1)
            champ8 = st.number_input("Champion 8 ID", min_value=1,max_value=700,step=1)
            champ9 = st.number_input("Champion 9 ID", min_value=1,max_value=700,step=1)
            champ10 = st.number_input("Champion 10 ID", min_value=1,max_value=700,step=1)
        with st.popover("Team one objectives amount"):
            team1_towers = st.number_input("Team 1 tower kills", min_value=0,max_value=11,step=1)
            team1_inhibitors = st.number_input("Team 1 inhibitor kills", min_value=0,max_value=20,step=1)
            team1_barons = st.number_input("Team 1 baron kills", min_value=0,max_value=20,step=1)
            team1_dragons = st.number_input("Team 1 dragon kills", min_value=0,max_value=20,step=1)
            team1_heralds = st.number_input("Team 1 rift herald kills", min_value=0,max_value=20,step=1)
        with st.popover("Team two objectives amount"):
            team2_towers = st.number_input("Team 2 tower kills", min_value=0,max_value=11,step=1)
            team2_inhibitors = st.number_input("Team 2 inhibitor kills", min_value=0,max_value=20,step=1)
            team2_barons = st.number_input("Team 2 baron kills", min_value=0,max_value=20,step=1)
            team2_dragons = st.number_input("Team 2 dragon kills", min_value=0,max_value=20,step=1)   
            team2_heralds = st.number_input("Team 2 rift herald kills", min_value=0,max_value=2,step=1)
            
        for i in range(1,5):
                st.write(" ")    
        
        ## Checking the ID of a champion using their name
        st.write("Type a champion name, and receive its ID")
        checkChar = st.text_input("Champion name")
        checkChar = checkChar.lower()
        if len(checkChar) > 0:
            fnd = champs.loc[champs['name']==checkChar]
            if fnd.shape[0] < 1:
                st.write("No such champion")
            else:
                st.write(fnd.iloc[0].id)
            
        ## Automatically setting radiobuttons/kills based on what was input (team 1 cannot simultaneously have first tower, and also 0 tower kills)
        if team1_towers == 0 and firstTower_radio == 1:
            team1_towers = 1
        if team2_towers == 0 and firstTower_radio == 2:
            team2_towers = 1
        
        if team1_inhibitors == 0 and firstInhibitor_radio == 1:
            team2_inhibitors = 1
        if team2_inhibitors == 0 and firstInhibitor_radio == 2:
            team2_inhibitors = 1    
        
        if team1_barons == 0 and firstBaron_radio == 1:
            team1_barons = 1
        if team2_barons == 0 and firstBaron_radio == 2:
            team2_barons = 1
        
        if team1_dragons == 0 and firstDragon_radio == 1:
            team1_dragons = 1
        if team2_dragons == 0 and firstDragon_radio == 2:
            team2_dragons = 1

        if team1_heralds == 0 and firstRiftHerald_radio == 1:
            team1_heralds = 1
        if team2_heralds == 0 and firstRiftHerald_radio == 2:
            team2_heralds = 1

    ## Writing the final composition/general info of the teams
    with st.sidebar:
        st.header("Team one")
        st.write("Composition:   " + str(champ1) + ", " + str(champ2) + ", " + str(champ3) + ", " + str(champ4) + ", " + str(champ5))
        st.write("Towers: " + str(team1_towers)) 
        st.write("Inhibitors: " + str(team1_inhibitors))
        st.write("Barons: " + str(team1_barons))
        st.write("Dragons: " + str(team1_dragons))
        st.write("Heralds: " + str(team1_heralds))
        
        for i in range(1,5):
            st.write(" ")
        
        st.header("Team two")
        st.write("Composition:   " + str(champ6) + ", " + str(champ7) + ", " + str(champ8) + ", " + str(champ9) + ", " + str(champ10))   
        st.write("Towers: " + str(team2_towers)) 
        st.write("Inhibitors: " + str(team2_inhibitors))
        st.write("Barons: " + str(team2_barons))
        st.write("Dragons: " + str(team2_dragons))
        st.write("Heralds: " + str(team2_heralds))

    ## Inputting the variables into model, and predicting it
    data = [[gameDuration_slider, firstBlood_radio, firstTower_radio, firstInhibitor_radio, firstBaron_radio, firstDragon_radio, firstRiftHerald_radio,
            champ1,champ2,champ3,champ4,champ5,team1_towers,team1_inhibitors,team1_barons,team1_dragons,team1_heralds,
            champ6,champ7,champ8,champ9,champ10,team2_towers,team2_inhibitors,team2_barons,team2_dragons,team2_heralds]]
    winner = model.predict(data)
    s_confidence = model.predict_proba(data)

    ## Showing certainty of prediction (e.g. 65 precent chance of team 1 winning, as we assume we are team 1)
    with prediction:
        st.header("				Will you win the game?")
        st.header(("Yes" if winner[0] == 1 else "No"))
        try:
            st.write("Percent certainty: " + str(math.floor(s_confidence[0][0] * 100)) + "%")
        except:
            st.write("Unable to determine certainty")


if __name__ == "__main__":
    main()