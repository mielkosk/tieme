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
    "Valitse kustakin ryhmästä yksi **tärkein** ja yksi **vähiten tärkeä** arvolause. "
    "Tehtävän lopuksi saat yhteenvedon arvoistasi."
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

GROUP_SIZE = 4
NUMBER_OF_GROUPS = 5

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.scores = defaultdict(int)
    st.session_state.groups = [
        random.sample(STATEMENTS, GROUP_SIZE)
        for _ in range(NUMBER_OF_GROUPS)
    ]

index = st.session_state.index
scores = st.session_state.scores
groups = st.session_state.groups

# --------------------------------------------------
# PARIVERTAILU
# --------------------------------------------------

if index < NUMBER_OF_GROUPS:
    group = groups[index]

    st.subheader(f"Valinta {index + 1} / {NUMBER_OF_GROUPS}")

    labels = [s[0] for s in group]

    col_left, col_mid, col_right = st.columns([1, 6, 1])

    with col_left:
        st.markdown("**Tärkein**")
        best = st.radio("", labels, key=f"best_{index}")

    with col_mid:
        for l in labels:
            st.write(l)

    with col_right:
        st.markdown("**Vähiten tärkeä**")
        worst = st.radio("", labels, key=f"worst_{index}")

    if st.button("Seuraava"):
        if best == worst:
            st.warning("Et voi valita samaa väittämää sekä tärkeimmäksi että vähiten tärkeäksi.")
        else:
            for statement, category in group:
                if statement == best:
                    scores[category] += 1
                if statement == worst:
                    scores[category] -= 1

            st.session_state.index += 1
            st.rerun()

# --------------------------------------------------
# TULOKSET + RADAR CHART + REFLEKTIO
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

    ax.set_thetagrids(
        np.degrees(angles[:-1]),
        categories
    )

    ax.set_title("Metsänomistajan arvoprofiili", pad=20)
    ax.set_rlabel_position(0)
    ax.grid(True)

    st.pyplot(fig)

    # --- Sanallinen tulkinta ---
    st.subheader("Tulkinta")

    top_value = max(scores, key=scores.get)

    INTERPRETATION = {
        "Talous": (
            "Vastauksissasi korostuu metsän taloudellinen merkitys ja hallittavuus. "
            "Arvostat selkeitä ja ennakoitavia ratkaisuja."
        ),
        "Luonto": (
            "Luontoarvot ja kestävyys ovat sinulle keskeisiä. "
            "Metsä on sinulle muutakin kuin tuotannon väline."
        ),
        "Jatkuvuus": (
            "Ajattelet metsää pitkällä aikavälillä ja tulevia sukupolvia silmällä pitäen."
        ),
        "Tunne": (
            "Metsä on sinulle henkilökohtaisesti merkityksellinen ja hyvinvointia tuova."
        ),
    }

    st.write(INTERPRETATION[top_value])

    # --- Reflektiokysymys ---
    st.info(
        "Pohdi hetki:\n\n"
        "• Miten tämä arvoprofiili näkyy nykyisissä metsänhoitovalinnoissasi?\n"
        "• Onko jokin arvo, jota haluaisit tulevaisuudessa painottaa enemmän?"
    )
