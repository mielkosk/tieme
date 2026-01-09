import streamlit as st
import random
from collections import defaultdict
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Metsänomistajan arvot",
    layout="wide"
)

st.title("Metsänomistajan arvojen pohdinta")
st.write(
    "Seuraavaksi pääset pohtimaan, mitkä asiat ovat sinulle metsänomistajana "
    "tärkeimpiä ja mitkä vähiten tärkeitä."
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

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = defaultdict(int)
    st.session_state.groups = [
        random.sample(STATEMENTS, GROUP_SIZE)
        for _ in range(NUMBER_OF_GROUPS)
    ]

step = st.session_state.step
scores = st.session_state.scores
groups = st.session_state.groups

# --------------------------------------------------
# BEST–WORST -VALINNAT
# --------------------------------------------------

if step < NUMBER_OF_GROUPS:
    group = groups[step]

    st.subheader(f"Valinta {step + 1} / {NUMBER_OF_GROUPS}")

    labels = [s[0] for s in group]

    col_high, col_text, col_low = st.columns([1, 6, 1])

    with col_high:
        st.markdown("**Tärkein**")
        highest = st.radio(
            "",
            options=labels,
            key=f"high_{step}"
        )

    with col_text:
        for text in labels:
            st.write(text)

    with col_low:
        st.markdown("**Vähiten tärkeä**")
        lowest = st.radio(
            "",
            options=labels,
            key=f"low_{step}"
        )

    if st.button("Seuraava"):
        if highest == lowest:
            st.warning("Et voi valita samaa väittämää sekä tärkeimmäksi että vähiten tärkeäksi.")
        else:
            for statement, category in group:
                if statement == highest:
                    scores[category] += 1
                if statement == lowest:
                    scores[category] -= 1

            st.session_state.step += 1
            st.experimental_rerun()

# --------------------------------------------------
# TULOKSET + ARVOKARTTA
# --------------------------------------------------

else:
    st.subheader("Arvoprofiilisi")

    # ---- Pisteet ----
    for cat, value in scores.items():
        st.write(f"**{cat}**: {value}")

    # ---- Arvokartta ----
    st.subheader("Arvokartta")

    x = scores["Talous"] - scores["Luonto"]
    y = scores["Jatkuvuus"] - scores["Tunne"]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axhline(0)
    ax.axvline(0)

    ax.scatter(x, y, s=200)
    ax.text(x + 0.1, y + 0.1, "Sinä", fontsize=12)

    ax.set_xlabel("Talous  ← →  Luonto")
    ax.set_ylabel("Tunne  ← →  Jatkuvuus")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)

    # ---- Tulkinta ----
    st.subheader("Mitä tämä kertoo sinusta?")

    if x > 0 and y > 0:
        st.write(
            "Painotat metsänhoidossa taloudellista järkevyyttä ja pitkän aikavälin jatkuvuutta. "
            "Metsä on sinulle vastuullinen sijoitus tulevaisuuteen."
        )
    elif x > 0 and y <= 0:
        st.write(
            "Taloudelliset näkökulmat ovat sinulle tärkeitä, mutta metsällä on myös "
            "henkilökohtainen ja kokemuksellinen merkitys."
        )
    elif x <= 0 and y > 0:
        st.write(
            "Luontoarvot ja pitkäjänteisyys ohjaavat metsäsuhdettasi. "
            "Ajattelet metsää osana laajempaa kokonaisuutta."
        )
    else:
        st.write(
            "Metsä on sinulle ennen kaikkea hyvinvoinnin ja merkityksen lähde. "
            "Taloudellinen tuotto ei ole keskiössä."
        )

    # ---- Reflektio ----
    st.info(
        "Pohdi hetki:\n\n"
        "• Miten tämä arvoprofiili näkyy nykyisissä metsänhoitovalinnoissasi?\n"
        "• Onko jokin arvo, jota haluaisit tulevaisuudessa painottaa enemmän?"
    )
