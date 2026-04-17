"""
Dashboard de visualisation des alertes de securite
"""

import streamlit as st
import folium
from folium.plugins import HeatMap
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.config import POSTGRES_CONFIG

st.set_page_config(
    page_title="INSO Security Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Connexion DB
@st.cache_resource
def get_engine():
    conn_str = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}"
    return create_engine(conn_str)

def load_data():
    engine = get_engine()
    query = """
    SELECT id, source_id, source_type, content, raw_entities, locations,
           primary_location, latitude, longitude, country, severity_score,
           severity_label, verification_status, created_at, collected_at
    FROM security_alerts 
    WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
    ORDER BY created_at DESC
    """
    # Connexion explicite avec SQLAlchemy 2.0
    with engine.connect() as conn:
        df = pd.read_sql(query, conn.connection)
        return df

# Titre
st.title("🛡️ INSO Security Intelligence Dashboard")
st.markdown("Surveillance OSINT des zones de crise")

# Sidebar filtres
st.sidebar.header("Filtres")
severity_filter = st.sidebar.multiselect(
    "Gravite",
    ['HIGH', 'MEDIUM', 'LOW'],
    default=['HIGH', 'MEDIUM']
)

date_range = st.sidebar.date_input(
    "Periode",
    value=[pd.Timestamp.now() - pd.Timedelta(days=7), pd.Timestamp.now()]
)

# Chargement donnees
df = load_data()

if not df.empty:
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Alertes", len(df))
    col2.metric("Alertes HIGH", len(df[df['severity_label'] == 'HIGH']))
    col3.metric("Pays couverts", df['country'].nunique())
    col4.metric("Derniere alerte", df['created_at'].max().strftime('%H:%M'))
    
    # Carte
    st.subheader("Carte des incidents")
    
    m = folium.Map(location=[48.3794, 31.1656], zoom_start=6)
    
    # Heatmap
    heat_data = df[df['latitude'].notna()][['latitude', 'longitude', 'severity_score']].values.tolist()
    if heat_data:
        HeatMap(heat_data, radius=15).add_to(m)
    
    # Marqueurs HIGH
    high_alerts = df[df['severity_label'] == 'HIGH']
    for _, row in high_alerts.iterrows():
        if pd.notna(row['latitude']):
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=f"{row['content'][:100]}...",
                icon=folium.Icon(color='red', icon='warning-sign')
            ).add_to(m)
    
    st.components.v1.html(m._repr_html_(), height=500)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution par gravite")
        fig = px.pie(df, names='severity_label', color='severity_label',
                     color_discrete_map={'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#2ecc71'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Alertes dans le temps")
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        daily = df.groupby(['date', 'severity_label']).size().reset_index(name='count')
        fig = px.line(daily, x='date', y='count', color='severity_label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tableau detaille
    st.subheader("Dernieres alertes")
    st.dataframe(
        df[['created_at', 'severity_label', 'primary_location', 'country', 'content']].head(20),
        use_container_width=True
    )
    
else:
    st.warning("Aucune donnee disponible. Executez le pipeline d'abord.")
