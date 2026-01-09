# tallennetaan tiedostoksi esim. arvopolku.py

import streamlit as st
import random
from collections import defaultdict

st.set_page_config(page_title="Metsänomistajan arvopolku")

st.title("Arvopohdinta metsänomistajille")
st.write(
    "Valitse jokaisesta parista se väittämä, joka kuvaa sinulle tärkeintä arvoa metsänomistajana."
)

# --- Arvoväittämät ja kategoriat ---
STATEMENTS = [
    # Talous & käyttö
    ("Metsän kuuluu tuottaa taloudellista hyötyä omistajalleen.", "Talous"),
    ("Metsänhoidon pitää olla kustannuksiltaan ennakoitavaa ja hallittua.", "Talous"),
    ("Metsä on minulle sijoitus muiden joukossa.", "Talous"),
    ("Haluan, että metsän hoito vaatii mahdollisimman vähän omaa aikaa.", "Talous"),

    # Luonto & kestävyys
    ("Luonnon monimuotoisuuden säilyminen on metsän hoidossa keskeistä.", "Luonto"),
    ("Haluan, että metsänhoitoni tukee ilmastonmuutoksen hillintää.", "Luonto"),
    ("Metsän ei tarvitse tuottaa maksimaalista taloudellista hyötyä ollakseen arvokas.", "Luonto"),
    ("Luonnon oma rytmi saa näkyä metsässäni.", "Luonto"),

    # Jatkuvuus & arvot
    ("On tärkeää, että metsä säilyy hyvässä kunnossa tuleville sukupolville.", "Jatkuvuus"),
    ("Metsä on osa perheeni tai sukuni historiaa.", "Jatkuvuus"),
    ("Teen metsää koskevat päätökset pitkällä aikavälillä.", "Jatkuvuus"),
    ("Haluan jättää metsän paremmassa kunnossa kuin sen sain.", "Jatkuvuus"),

    # Omistajuus & tunne
    ("Metsä tuo minulle rauhaa ja hyvinvointia.", "Tunne"),
    ("Haluan päättää itse metsää koskevista ratkaisuista.", "Tunne"),
    ("Metsän hoito on minulle mielekäs ja merkityksellinen asia.", "Tunne"),
    ("Metsän käyttö omiin tarpeisiin (retkeily, marjastus, mökki) on tärkeää.", "Tunne"),
]

NUMBER_OF_PAIRS = 10

# --- Sessiomuisti käyttäjälle ---
if "pair_index" not in st.session_state:
    st.session_state.pair_index = 0
    st.session_state.scores = defaultdict(int)
    # arvotaan parit
    st.session_state.pairs = random.sample(
        [(a, b) for idx, a in enumerate(STATEMENTS)
         for b in STATEMENTS[idx + 1:]],
        NUMBER_OF_PAIRS
    )

pair_index = st.session_state.pair_index
scores = st.session_state.scores
pairs = st.session_state.pairs

# --- Näytetään nykyinen pari ---
if pair_index < NUMBER_OF_PAIRS:
    left, right = pairs[pair_index]

    st.write(f"**Valinta {pair_index + 1}/{NUMBER_OF_PAIRS}**")
    choice = st.radio(
        "Kumpi väittämä kuvaa sinua paremmin?",
        (left[0], right[0])
    )

    if st.button("Valitse ja siirry seuraavaan"):
        # tallennetaan valinta
        chosen = left if choice == left[0] else right
        scores[chosen[1]] += 1
        st.session_state.pair_index += 1
        st.experimental_rerun()  # päivitys seuraavaan pariin
else:
    # --- Tulokset ja palaute ---
    st.subheader("Tuloksesi")

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for category, score in sorted_scores:
        st.write(f"{category}: {score} valintaa")

    top_value = sorted_scores[0][0]

    FEEDBACK = {
        "Talous": (
            "Vastauksissasi korostui metsän taloudellinen merkitys ja hallittavuus. "
            "Arvostat ennakoitavuutta ja selkeitä ratkaisuja metsänhoidossa."
        ),
        "Luonto": (
            "Arvostat metsän ekologisia arvoja ja luonnon monimuotoisuutta. "
            "Metsä on sinulle muutakin kuin tuotantoresurssi."
        ),
        "Jatkuvuus": (
            "Pitkäjänteisyys ja tulevat sukupolvet ovat sinulle tärkeitä. "
            "Teet metsää koskevia päätöksiä laajemmassa aikahorisontissa."
        ),
        "Tunne": (
            "Metsä on sinulle henkilökohtaisesti merkityksellinen. "
            "Hyvinvointi, omistajuus ja tunneperäinen suhde korostuvat."
        ),
    }

    st.subheader("Arvoprofiilisi")
    st.write(FEEDBACK[top_value])
    st.write("Pidä tämä mielessä, kun etenet metsänhoitoa koskevissa valinnoissa.")
