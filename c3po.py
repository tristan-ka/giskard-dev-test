import streamlit as st
import json
import sys

sys.path.append('./')
from src.utils import load_default_millenium_data, convert_bounty_hunters_dict
from src.calculate_odds import compute_paths, count_encounters, output_odds

st.write("""
# What are the Odds?
""")

uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])

# Check if a file was uploaded
if uploaded_file is not None:
    # Read and display the content of the JSON file
    empire_data = json.load(uploaded_file)
    st.write("JSON content:")
    st.json(empire_data)

    graph, car_autonomy, start_planet, destination_planet = load_default_millenium_data()

    count_down = empire_data['countdown']
    bounty_hunters = empire_data['bounty_hunters']
    hunters_dict = convert_bounty_hunters_dict(bounty_hunters)

    possible_paths = compute_paths(graph, start_planet, destination_planet, car_autonomy, count_down)
    possible_paths = count_encounters(possible_paths, hunters_dict)
    odds, final_path, final_time_path = output_odds(possible_paths)

    st.write("The odds of reaching " + destination_planet + " from " + start_planet + " are " + str(odds) + "%")
