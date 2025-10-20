import streamlit as st

# ---- Minimal color palette ----
st.set_page_config(page_title="Data Analytics • AI", page_icon="📊", layout="wide")
st.markdown("""
<style>
:root{
  --brand:#3d7bfd;      
  --brand-strong:#2458b3;
  --ink:#1f2937;        
}
h1,h2,h3 { color: var(--ink) !important; }
.stButton > button {
  background: var(--brand) !important; color:white !important; border:0 !important;
}
.stButton > button:hover { background: var(--brand-strong) !important; }
</style>
""", unsafe_allow_html=True)

# ---- Session state ----
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "PC", "Professor", "Team"]

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)
    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.header("Log out")
    if st.button("Log out"):
        st.session_state.role = None
        st.rerun()

role = st.session_state.role

# ---- Pages ----
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

visualization = st.Page(
    "Visualization/visualization.py",
    title="Dashboard",
    icon=":material/monitoring:",
    default=(role == "Requester"),
)
maps = st.Page(
    "Visualization/maps.py",
    title="Maps",
    icon=":material/map:",
    default=(role == "Requester"),
)
maps2 = st.Page(
    "Visualization/maps2.py",
    title="Other maps",
    icon=":material/public:",
    default=(role == "Requester"),
)
ml = st.Page(
    "ml/ml_analysis.py",
    title="Machine Learning",
    icon=":material/neurology:",
    default=(role == "Responder"),
)
eda = st.Page(
    "EDA/eda.py",
    title="Exploratory Data Analysis",
    icon=":material/insights:",
    default=(role == "Admin"),
)

account_pages = [logout_page, settings]
visualization_pages = [visualization, maps, maps2]
ml_pages = [ml]
eda_pages = [eda]

# ---- Header and logo ----
st.title("Data Analytics • AI")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

# ---- Sidebar ----
with st.sidebar:
    st.header("Menu")
    st.caption("Available sections:")
    st.markdown(
        "- **Visualization**: Dashboards and maps\n"
        "- **EDA**: Data exploration\n"
        "- **Machine Learning**: Modeling and evaluation\n"
        "- **Account**: Settings and log out"
    )
    st.divider()
    st.caption(f"**Current role:** {role if role else 'Not logged in'}")

# ---- Small info sections ----
with st.expander("About this app"):
    st.write(
        "Includes **Visualization**, **EDA**, and **Machine Learning** modules. "
        "Select your role to enable corresponding sections."
    )
with st.expander("Quick access"):
    st.write("Go to **Account → Settings** to update your preferences or log out.")

# ---- Navigation logic ----
page_dict = {}

if st.session_state.role in ["Professor", "Team"]:
    page_dict["EDA"] = eda_pages
if st.session_state.role in ["Professor", "Team", "PC"]:
    page_dict["Visualization"] = visualization_pages
if st.session_state.role in ["Professor", "Team"]:
    page_dict["Machine Learning"] = ml_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
