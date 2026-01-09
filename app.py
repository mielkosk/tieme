import streamlit as st
import random
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Metsänomistajan arvot – parivertailu",
    layout="wide"
)

st.title("Metsänomistajan arvojen pohdinta")
st.write(
    "Näet aina kaksi arvolausetta. Valitse niistä se, "
    "joka on sinulle metsänomistajana tärkeämpi."
)

# --------------------------------------------------
# ARVOLAUSET
# --------------------------------------------------

STATEMENTS = [
    ("Metsän kuuluu tuottaa taloudellista hyötyä omistajalleen.", "Talous"),
    ("Metsänhoidon pitää olla kustannuksiltaan ennakoitavaa ja hallittua.", "Talous"),
    ("Metsä on minulle sijoitus muiden joukossa.", "Talous"),
    ("Haluan, että metsän hoito vaatii mahdollisimman vähän omaa aikaa.", "Talous"),

    ("Luonnon monimuotoisuuden säilyminen on metsän hoidossa keskeistä.", "Luonto"),
    ("Haluan, että metsänhoitoni tukee ilmastonmuutoksen hillintää.", "Luonto"),
    ("Metsän ei tarvitse tuottaa maksimaalista taloudellista hyötyä ollakseen arvokas.", "Luonto"),
    ("Luonnon oma rytmi saa näkyä metsässäni.", "Luonto"),

    ("On tärkeää, että metsä säilyy hyvässä kunnossa tuleville sukupolville.", "Jatkuvuus"),
    ("Metsä on osa perheeni tai sukuni historiaa.", "Jatkuvuus"),
    ("Teen metsää koskevat päätökset pitkällä aikavälillä.", "Jatkuvuus"),
    ("Haluan jättää metsän paremmassa kunnossa kuin sen sain.", "Jatkuvuus"),

    ("Metsä tuo minulle rauhaa ja hyvinvointia.", "Tunne"),
    ("Haluan päättää itse metsää koskevista ratkaisuista.", "Tunne"),
    ("Metsän hoito on minulle mielekäs ja merkityksellinen asia.", "Tunne"),
    ("Metsän käyttö omiin tarpeisiin on tärkeää.", "Tunne"),
]

# --------------------------------------------------
# ASETUKSET
# --------------------------------------------------

NUMBER_OF_PAIRS = 12

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "pair_index" not in st.session_state:
    st.session_state.pair_index = 0
    st.session_state.scores = defaultdict(int)

    all_pairs = []
    for i in range(len(STATEMENTS)):
        for j in range(i + 1, len(STATEMENTS)):
            all_pairs.append((STATEMENTS[i], STATEMENTS[j]))

    random.shuffle(all_pairs)
    st.session_state.pairs = all_pairs[:NUMBER_OF_PAIRS]

pair_index = st.session_state.pair_index
pairs = st.session_state.pairs
scores = st.session_state.scores

# --------------------------------------------------
# PARIVERTAILU
# --------------------------------------------------

if pair_index < NUMBER_OF_PAIRS:
    left, right = pairs[pair_index]

    st.subheader(f"Valinta {pair_index + 1} / {NUMBER_OF_PAIRS}")

    choice = st.radio(
        "Kumpi on sinulle tärkeämpi?",
        [left[0], right[0]],
        key=f"choice_{pair_index}"
    )

    if st.button("Seuraava"):
        if choice == left[0]:
            scores[left[1]] += 1
        else:
            scores[right[1]] += 1

        st.session_state.pair_index += 1
        st.rerun()

# --------------------------------------------------
# TULOKSET + RADAR CHART
# --------------------------------------------------

else:
    st.subheader("Arvoprofiilisi")

    categories = ["Talous", "Luonto", "Jatkuvuus", "Tunne"]
    values = [scores[c] for c in categories]

    # --- Radar chart ---
    st.subheader("Arvokartta")

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_title("Metsänomistajan arvoprofiili", pad=20)
    ax.grid(True)

    st.pyplot(fig)

    # --- Sanallinen palaute ---
    st.subheader("Tulkinta")

    top_value = max(scores, key=scores.get)

    FEEDBACK = {
        "Talous": "Taloudelliset näkökulmat ja metsän tuotto ovat sinulle keskeisiä.",
        "Luonto": "Luontoarvot ja kestävyys ohjaavat vahvasti metsäsuhdettasi.",
        "Jatkuvuus": "Ajattelet metsää pitkällä aikavälillä ja tulevia sukupolvia varten.",
        "Tunne": "Metsällä on sinulle henkilökohtainen ja hyvinvointia tuova merkitys.",
    }

    st.write(FEEDBACK[top_value])

    # --- Reflektiokysymys ---
    st.info(
        "Pohdi:\n\n"
        "• Missä metsänhoitoa koskevissa päätöksissä nämä arvot näkyvät selkeimmin?\n"
        "• Onko jokin arvo, jota haluaisit tulevaisuudessa painottaa enemmän?"
    )
