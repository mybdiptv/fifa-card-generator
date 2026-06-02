import streamlit as st
import pandas as pd
import pickle as pk
import random
from PIL import Image, ImageDraw, ImageFont

@st.cache_resource
def load():
    with open("fifa.pkl","rb") as f:
        bundle = pk.load(f)
    return bundle
def get_caption(value, attribute):
    captions = {
        "pace": [
            (40, "Slow 🐢"),
            (74, "Average Speed"),
            (89, "Fast ⚡"),
            (99, "Explosive Pace 🔥")
        ],
        "shooting": [
            (40, "Weak Shooter"),
            (72, "Average Shooter"),
            (88, "Good Finisher 🎯"),
            (99, "Deadly Finisher 💥")
        ],
        "passing": [
            (40, "Basic Passing"),
            (82, "Decent Passer"),
            (88, "Creative Playmaker 🎩"),
            (99, "Passing Maestro 🪄")
        ],
        "dribbling": [
            (40, "Basic Ball Control"),
            (74, "Decent Dribbler"),
            (87, "Skillful Dribbler ✨"),
            (99, "Magician On The Ball 🪄")
        ],
        "defending": [
            (40, "Poor Defender"),
            (75, "Average Defender"),
            (88, "Reliable Defender 🧱"),
            (99, "World-Class Defender 🛡️")
        ],
        "physic": [
            (40, "Low Strength"),
            (74, "Average Physicality"),
            (87, "Strong Player 💪"),
            (99, "Physical Beast 🦁")
        ]
    }
    for limit, text in captions[attribute]:
        if value <= limit:
            return text

res = load()
model = res["model"]
features = res["features"]

st.title("⚽ FIFA Card Rating System")
st.caption("Create your own FIFA Overall Rating!")

st.subheader("Player Information")
st.divider()
name = st.text_input("Player Name")
position = st.selectbox(
    "Position",
    ["ST", "LW", "RW", "AM", "CM", "DM", "LB", "RB", "CB"]
)

st.subheader("Player Attributes")
st.caption("Use arrow keys for better adjustment of values")
st.divider()
pace = st.slider("Pace", 1, 99, 70)
st.caption(get_caption(pace, "pace"))
st.divider()
shooting = st.slider("Shooting", 1, 99, 70)
st.caption(get_caption(shooting, "shooting"))
st.divider()
passing = st.slider("Passing", 1, 99, 70)
st.caption(get_caption(passing, "passing"))
st.divider()
dribbling = st.slider("Dribbling", 1, 99, 70)
st.caption(get_caption(dribbling, "dribbling"))
st.divider()
defending = st.slider("Defending", 1, 99, 70)
st.caption(get_caption(defending, "defending"))
st.divider()
physic = st.slider("Physical", 1, 99, 70)
st.caption(get_caption(physic, "physic"))
st.divider()

if st.button("Generate Card"):
    data = pd.DataFrame({
        "pace": [pace],
        "shooting": [shooting],
        "passing": [passing],
        "dribbling": [dribbling],
        "defending": [defending],
        "physic": [physic]
    })
    data = data[features]
    overall = round(model.predict(data)[0])
    
    card_templates = [
        "cards/card1.png",
        "cards/card2.png",
        "cards/card3.png",
        "cards/card4.png",
        "cards/card5.png"
    ]
    selected_card = random.choice(card_templates)
    card = Image.open(selected_card)    
    draw = ImageDraw.Draw(card)
    font_big = ImageFont.truetype("arial.ttf", 120)
    font_medium = ImageFont.truetype("arial.ttf", 85)
    font_small = ImageFont.truetype("arial.ttf", 60)

    draw.text((230, 200), str(overall), fill="black", font=font_big)
    draw.text((255, 345), position, fill="black", font=font_small)

    draw.text((375, 815), name.upper(), fill="black", font=font_medium)

    draw.text((250, 970), f"{pace} PAC", fill="black", font=font_small)
    draw.text((250, 1050), f"{shooting} SHO", fill="black", font=font_small)
    draw.text((250, 1130), f"{passing} PAS", fill="black", font=font_small)

    draw.text((650, 970), f"{dribbling} DRI", fill="black", font=font_small)
    draw.text((650, 1050), f"{defending} DEF", fill="black", font=font_small)
    draw.text((650, 1130), f"{physic} PHY", fill="black", font=font_small)

    st.image(card)
