import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="CarbonRoots CO₂ Calculator", layout="centered")

# 🔶 Shared CSS styling
st.markdown("""
    <style>
        .block-container {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 10px;
        }
        h1, h2, h3 {
            color: #2e7d32;
        }
        .stMarkdown p {
            font-size: 16px;
            color: #2f3e2f;
        }
        .logo-title {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .logo-title img {
            height: 45px;
        }
    </style>
""", unsafe_allow_html=True)

# 🔶 Logo at the top (always visible)

    # Logo + Title (streamlit-friendly)
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
    st.image("logo.png", width=200)
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("## CarbonRoots: Modeling CO₂ Absorption Potential of Indian Tree Species")


# Step 1: Ask for user's name
if "username" not in st.session_state:
    st.markdown("### 🌿 Welcome to CarbonRoots")
    st.markdown("To get started, please enter your name:")

    name = st.text_input("Your Name")
    if st.button("Start"):
        if name.strip():
            st.session_state.username = name.strip().title()
            st.rerun()
        else:
            st.warning("Please enter a valid name to continue.")

else:
    # Load dataset
    df = pd.read_excel("dataset.xlsx")
    df["CO2_Sequestered_kg_per_year"] = (
        df["Annual_Biomass_Gain_kg"] * (df["Carbon_Content_Percent"] / 100) * 3.67
    )

    # 🌿 Intro content
    st.markdown(f"""
    ### Hello, {st.session_state.username}!
    Trees are vital to Earth's ecosystems. They absorb CO₂, release oxygen, cool urban heat, support biodiversity, and prevent soil erosion.

    ### 🌍 Why CO₂ Sequestration Matters:
    - **Climate Change Mitigation:** Trees act as natural carbon sinks, absorbing atmospheric carbon and storing it in their trunks, branches, and roots.
    - **Sustainable Future:** Knowing how much CO₂ each tree absorbs helps us plan smarter, greener spaces.
    - **Biodiversity Support:** Native tree species create better habitats for local wildlife.

    ### 🌿 Did You Know?
    - A single mature Neem tree can absorb up to 30 kg of CO₂ per year.
    - Fast-growing species like Bamboo and Teak are excellent carbon absorbers.
    - Choosing region-specific trees ensures higher survival and lower maintenance.

    Use this tool to explore the environmental impact of tree planting and contribute to a greener planet.
    """)

    # 🖼️ Dummy image
    st.image("image.png", caption="Your green impact starts here")

    st.markdown("---")
    st.header("🌿 Tree-Based CO₂ Calculator")

    # Inputs
    tree = st.selectbox("Select a Tree Species", df["Tree_Species"].unique())
    num_trees = st.number_input("Number of Trees", min_value=1, value=100)
    years = st.number_input("Number of Years", min_value=1, value=10)

    # Calculation
    row = df[df["Tree_Species"] == tree].iloc[0]
    co2_per_tree = row["CO2_Sequestered_kg_per_year"]
    total_co2 = co2_per_tree * num_trees * years

    st.success(f"🌍 {st.session_state.username}, your trees will sequester **{round(total_co2, 2)} kg** of CO₂ over {years} years.")

    st.markdown(f"""
    - **CO₂ per tree per year:** {round(co2_per_tree, 2)} kg  
    - **Survival Rate:** {row['Survival_Rate_Percent']}%  
    - **Native Region:** {row['Native_Region']}
    """)

    # Save to Excel
    log_data = pd.DataFrame([{
        "User": st.session_state.username,
        "Tree_Species": tree,
        "Trees_Planted": num_trees,
        "Years": years,
        "CO2_Sequestered_kg": round(total_co2, 2),
    }])

    excel_path = "CarbonRoots_User_Data.xlsx"
    if os.path.exists(excel_path):
        existing_data = pd.read_excel(excel_path)
        combined_data = pd.concat([existing_data, log_data], ignore_index=True)
    else:
        combined_data = log_data

    combined_data.to_excel(excel_path, index=False)

    if st.checkbox("Show Top 10 CO₂ Absorbing Trees"):
        top = df.sort_values("CO2_Sequestered_kg_per_year", ascending=False).head(10)
        st.bar_chart(top.set_index("Tree_Species")["CO2_Sequestered_kg_per_year"])

    st.markdown("---")
    st.caption("© 2025 CarbonRoots by Meher Raju")