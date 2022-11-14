import streamlit as st
import pandas as pd
import pickle
import bz2

# Declaring the teams

teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']

# declaring the venues

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# loading the model
model = pickle.load(bz2.BZ2File('model.pkl', 'rb'))

st.title('IPL Win Predictor App')


col1, col2 = st.columns(2)

with col1:
    battingteam = st.selectbox('Select the batting team', sorted(teams))
    if battingteam:
        battingteam = teams.index(battingteam)

with col2:
    bowlingteam = st.selectbox('Select the bowling team', sorted(teams))
    if bowlingteam:
        bowlingteam = teams.index(bowlingteam)


city = st.selectbox(
    'Select the city where the match is being played', sorted(cities))
if city:
    city = cities.index(city)


target = st.number_input('Target', step = 1)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', step = 1)

with col4:
    overs = st.slider('Overs', min_value = 0.1, max_value = 20.0, step = 0.1)

with col5:
    wickets = st.slider('Wickets', 0, 10)

columns = st.columns((2, 1, 2))
button_pressed = columns[1].button('Predict')

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
</style>""", unsafe_allow_html=True)

if button_pressed:

    runs_left = target-score
    balls_left = 120-(overs*6)
    wickets = 10-wickets
    currentrunrate = score/overs
    requiredrunrate = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team': [battingteam], 'bowling_team': [bowlingteam], 'city': [city], 'runs_left': [runs_left], 'balls_left': [
                            balls_left], 'wickets': [wickets], 'total_runs_x': [target], 'cur_run_rate': [currentrunrate], 'req_run_rate': [requiredrunrate]})

    result = model.predict_proba(input_df)
    lossprob = result[0][0]
    winprob = result[0][1]

    winprob = str(round(winprob*100, 2))
    lossprob = str(round(lossprob*100, 2))

    st.header(teams[battingteam]+' has a '+winprob+"% chance of winning the match")

    st.header(teams[bowlingteam]+' has a '+lossprob+"% chance of winning the match")