import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="Political Compass", layout="wide")

# Custom CSS for UI styling
st.markdown("""
    <style>
    .stRadio [data-testid="stWidgetLabel"] { display: none; } 
    .question-box { 
        background-color: #f9f9f9; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 5px; 
        border-left: 5px solid #007bff; 
        font-weight: bold; 
    }
    .result-text { 
        font-size: 32px; 
        font-weight: bold; 
        text-align: center; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        border: 3px solid #000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- REFERENCE DATA ---
references = pd.DataFrame([
    {"Name": "Narendra Modi (BJP)", "Econ": 7.0, "Soc": 8.0},
    {"Name": "Amit Shah (BJP)", "Econ": 6.5, "Soc": 9.5},
    {"Name": "Rahul Gandhi (INC)", "Econ": -6.0, "Soc": -3.0},
    {"Name": "Arvind Kejriwal (AAP)", "Econ": -4.0, "Soc": 1.0},
    {"Name": "Mamata Banerjee (TMC)", "Econ": -7.5, "Soc": 7.5},
    {"Name": "Pinarayi Vijayan (CPI-M)", "Econ": -9.0, "Soc": 6.5},
    {"Name": "Nirmala Sitharaman", "Econ": 8.0, "Soc": 5.0},
    {"Name": "Mahatma Gandhi", "Econ": -5.5, "Soc": -6.5},
    {"Name": "Jawaharlal Nehru", "Econ": -7.5, "Soc": 4.5},
    {"Name": "Sardar Patel", "Econ": 3.0, "Soc": 6.5},
    {"Name": "B.R. Ambedkar", "Econ": -4.0, "Soc": 2.5},
    {"Name": "Manmohan Singh", "Econ": 7.5, "Soc": 1.5},
    {"Name": "Stalin", "Econ": -9.5, "Soc": 9.5},
    {"Name": "Thatcher", "Econ": 8.5, "Soc": 5.0},
    {"Name": "Bernie Sanders", "Econ": -7.0, "Soc": -2.0}
])

def get_political_label(econ, soc):
    if soc > 3:
        if econ < -3: return "Authoritarian Left", "#ff4b4b" 
        if econ > 3: return "Authoritarian Right", "#1c83e1" 
        return "Authoritarian Center", "#a1a1a1"
    elif soc < -3:
        if econ < -3: return "Libertarian Left", "#28a745" 
        if econ > 3: return "Libertarian Right", "#ffd43b" 
        return "Libertarian Center", "#a1a1a1"
    else:
        if econ < -3: return "Social Democracy", "#ff8c00"
        if econ > 3: return "Liberalism / Capitalism", "#00ced1"
        return "Centrist", "#31333F"

# --- 20 QUESTIONS ---
econ_qs = [
    "1. The state should own or heavily regulate essential industries like energy and transport.",
    "2. Minimum wage laws are a necessary protection for the working class.",
    "3. High-income earners should pay significantly more tax to fund public services.",
    "4. A completely free market without regulation is the best economic system.", 
    "5. Inherited wealth is fundamentally unfair and should be heavily taxed.",
    "6. Government should provide a Universal Basic Income to all citizens.",
    "7. Privatization of public assets (like water or mail) usually leads to better efficiency.",
    "8. Protectionist tariffs are necessary to protect local industries and jobs.",
    "9. Strong labor unions are essential for a healthy and fair economy.",
    "10. Excessive government welfare spending is a primary cause of economic stagnation."
]

soc_qs = [
    "11. Preserving traditional and religious values is more important than progressive change.",
    "12. Military service should be a mandatory requirement for all young citizens.",
    "13. The government should be allowed to monitor private communications to prevent crime.",
    "14. Possession of non-medical drugs should be a personal choice, not a crime.",
    "15. The death penalty should remain an option for the most heinous crimes.",
    "16. Immigration should be strictly controlled to preserve the national culture.",
    "17. Reproductive rights (like abortion) should be protected by law.", 
    "18. Questioning authority is a sign of a healthy and free society.",
    "19. National sovereignty is always more important than international cooperation.",
    "20. A strong leader is more effective for a nation than a slow democratic consensus."
]

econ_weights = [-1, -1, -1, 1, -1, -1, 1, -1, -1, 1] 
soc_weights = [1, 1, 1, -1, 1, 1, -1, -1, 1, 1]

options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
multiplier = {"Strongly Disagree": -1.0, "Disagree": -0.5, "Neutral": 0, "Agree": 0.5, "Strongly Agree": 1.0}

# --- UI EXECUTION ---
st.title("🎯 Political Compass")

# NEW: User Name Input
user_name = st.text_input("Enter your name for the map:", placeholder="e.g. Rahul, Priya, etc.")
display_name = user_name.upper() if user_name else "YOU"

st.write(f"Hello **{display_name}**! Answer the questions below to see where you stand.")

st.header("Section 1: Economic Policy")
econ_ans = []
for i, text in enumerate(econ_qs):
    st.markdown(f"<div class='question-box'>{text}</div>", unsafe_allow_html=True)
    ans = st.radio(f"E{i}", options, index=2, horizontal=True, key=f"econ_{i}")
    econ_ans.append(multiplier[ans] * econ_weights[i])

st.divider()

st.header("Section 2: Social & Cultural Policy")
soc_ans = []
for i, text in enumerate(soc_qs):
    st.markdown(f"<div class='question-box'>{text}</div>", unsafe_allow_html=True)
    ans = st.radio(f"S{i}", options, index=2, horizontal=True, key=f"soc_{i}")
    soc_ans.append(multiplier[ans] * soc_weights[i])

if st.button("Generate My Results", type="primary", use_container_width=True):
    final_econ = sum(econ_ans)
    final_soc = sum(soc_ans)
    
    label, color = get_political_label(final_econ, final_soc)

    st.markdown(f"<div class='result-text' style='color: white; background-color: {color};'>"
                f"{display_name}'S ALIGNMENT: {label}</div>", unsafe_allow_html=True)

    fig = go.Figure()
    
    # Quadrant Colors
    fig.add_shape(type="rect", x0=-10, y0=0, x1=0, y1=10, fillcolor="red", opacity=0.12, layer="below")
    fig.add_shape(type="rect", x0=0, y0=0, x1=10, y1=10, fillcolor="blue", opacity=0.12, layer="below")
    fig.add_shape(type="rect", x0=-10, y0=-10, x1=0, y1=0, fillcolor="green", opacity=0.12, layer="below")
    fig.add_shape(type="rect", x0=0, y0=-10, x1=10, y1=0, fillcolor="yellow", opacity=0.12, layer="below")

    # Trace for Reference People
    fig.add_trace(go.Scatter(
        x=references["Econ"], y=references["Soc"], mode="markers+text",
        text=references["Name"], textposition="bottom center",
        marker=dict(color='#ffcccc', size=8, line=dict(color='#ff6666', width=1)),
        textfont=dict(color='#cc0000', size=9), name="Famous People"
    ))

    # Trace for User (Using Custom Name)
    fig.add_trace(go.Scatter(
        x=[final_econ], y=[final_soc], mode="markers+text",
        text=[display_name], textposition="top center",
        marker=dict(color='#1a1a1a', size=24, symbol='diamond', line=dict(width=2, color='white')),
        textfont=dict(color='black', size=18, family="Arial Black"), name="User"
    ))

    fig.update_layout(
        width=850, height=850,
        xaxis=dict(range=[-11, 11], title="<b>ECONOMIC AXIS</b><br>Left (Socialist) ← → Right (Capitalism)", zeroline=True, zerolinewidth=3, zerolinecolor='black'),
        yaxis=dict(range=[-11, 11], title="<b>SOCIAL AXIS</b><br>Libertarian ← → Authoritarian", zeroline=True, zerolinewidth=3, zerolinecolor='black'),
        showlegend=False, plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)
