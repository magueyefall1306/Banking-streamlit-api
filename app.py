"""
Banking Transaction Analysis System
Interface claire et professionnelle
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configuration
st.set_page_config(
    page_title="Banking Analytics",
    page_icon="🏦",
    layout="wide"
)

# Styles CSS - THÈME CLAIR
st.markdown("""
<style>
    /* Thème clair */
    .main {
        background-color: #f8fafc;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: white;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        background-color: #f1f5f9;
        border-radius: 6px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000/api"

# Fonctions API
def api_call(endpoint: str, method: str = "GET", params: dict = None, payload: dict = None):
    """Appel API simplifié."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        else:
            response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def check_api():
    """Vérifie l'API."""
    health = api_call("system/health")
    return health is not None and health.get("status") == "ok"

# Interface principale
def main():
    # En-tête
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🏦 Banking Transaction Analytics")
        st.caption(f"Session: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    with col2:
        if check_api():
            st.success("🟢 En ligne")
        else:
            st.error("🔴 Hors ligne")
            st.info("Lancez l'API : `uvicorn app.main:app --reload`")
            st.stop()
    
    st.markdown("---")
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Transactions", "🛡️ Détection", "📋 Rapports"])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_transactions()
    
    with tab3:
        show_fraud_detection()
    
    with tab4:
        show_reports()

def show_dashboard():
    """Dashboard principal."""
    st.subheader(" Vue d'ensemble")
    
    stats = api_call("stats/overview")
    
    if not stats:
        st.warning("Impossible de charger les données")
        return
    
    # KPIs - UTILISER LES MÉTRIQUES STREAMLIT NATIVES
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=" Total Transactions",
            value=f"{stats.get('total_transactions', 0):,}"
        )
    
    with col2:
        fraud_rate = stats.get('fraud_rate', 0) * 100
        st.metric(
            label=" Taux de Fraude",
            value=f"{fraud_rate:.2f}%"
        )
    
    with col3:
        st.metric(
            label=" Montant Moyen",
            value=f"${stats.get('avg_amount', 0):,.0f}"
        )
    
    with col4:
        st.metric(
            label=" Type Principal",
            value=stats.get('most_common_type', 'N/A')
        )
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Distribution par type**")
        stats_by_type = api_call("stats/by-type")
        
        if stats_by_type:
            df = pd.DataFrame(stats_by_type)
            fig = px.bar(
                df,
                x='type',
                y='count',
                title="Transactions par type",
                color='count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Analyse de fraude**")
        fraud_data = api_call("fraud/by-type")
        
        if fraud_data:
            df = pd.DataFrame(fraud_data)
            fig = px.pie(
                df,
                values='fraud_count',
                names='type',
                title="Répartition des fraudes",
                hole=0.4
            )
            fig.update_layout(height=400, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

def show_transactions():
    """Explorateur de transactions."""
    st.subheader("🔍 Explorateur de Transactions")
    
    # Filtres
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        tx_type = st.selectbox("Type", ["Tous", "PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"])
    
    with col2:
        fraud_filter = st.selectbox("Statut", ["Tous", "Fraudes", "Légitimes"])
    
    with col3:
        sort_by = st.selectbox("Tri", ["ID", "Montant ↑", "Montant ↓"])
    
    with col4:
        limit = st.number_input("Résultats", 10, 100, 25, 5)
    
    if st.button("🔍 Rechercher", type="primary"):
        params = {"page": 1, "limit": limit}
        
        if tx_type != "Tous":
            params["type"] = tx_type
        
        if fraud_filter == "Fraudes":
            params["isFraud"] = 1
        elif fraud_filter == "Légitimes":
            params["isFraud"] = 0
        
        with st.spinner("Chargement..."):
            data = api_call("transactions", params=params)
        
        if data and data.get('transactions'):
            transactions = data['transactions']
            df = pd.DataFrame(transactions)
            
            st.success(f"✅ {len(transactions)} transactions trouvées")
            
            # Résumé
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Résultats", len(transactions))
            with col2:
                st.metric("Volume total", f"${df['amount'].sum():,.0f}")
            with col3:
                st.metric("Montant moyen", f"${df['amount'].mean():,.0f}")
            with col4:
                st.metric("Fraudes", df['isFraud'].sum())
            
            st.markdown("---")
            
            # Graphique
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.scatter(
                    df,
                    x=df.index,
                    y='amount',
                    color='isFraud',
                    color_discrete_map={0: '#10b981', 1: '#ef4444'},
                    title="Distribution des montants"
                )
                fig.update_layout(height=400, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                type_counts = df['type'].value_counts()
                fig = px.pie(values=type_counts.values, names=type_counts.index, title="Par type")
                fig.update_layout(height=400, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            
            # Table
            st.markdown("**Détails**")
            display_df = df[['id', 'type', 'amount', 'nameOrig', 'nameDest', 'isFraud']].copy()
            display_df['isFraud'] = display_df['isFraud'].map({0: '✅', 1: '🚨'})
            display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(display_df, use_container_width=True, height=400)
        else:
            st.info("Aucune transaction trouvée")

def show_fraud_detection():
    """Détection de fraude."""
    st.subheader("🛡️ Détecteur de Fraude")
    
    st.info("Simulez une transaction pour évaluer le risque")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Transaction**")
        tx_type = st.selectbox("Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"])
        amount = st.number_input("Montant ($)", 0.0, value=2500.0, step=100.0)
    
    with col2:
        st.markdown("**Compte**")
        old_bal = st.number_input("Solde avant ($)", 0.0, value=8000.0, step=500.0)
        new_bal = st.number_input("Solde après ($)", 0.0, value=5500.0, step=500.0)
    
    if st.button("🎯 Analyser", type="primary"):
        with st.spinner("Analyse..."):
            result = api_call("fraud/predict", method="POST", payload={
                "type": tx_type,
                "amount": amount,
                "oldbalanceOrg": old_bal,
                "newbalanceOrig": new_bal
            })
        
        if result:
            is_fraud = result.get('isFraud', False)
            probability = result.get('probability', 0) * 100
            
            st.markdown("---")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if is_fraud:
                    st.error(f"### 🚨 FRAUDE DÉTECTÉE\n\n**Risque:** {probability:.1f}%")
                else:
                    st.success(f"### ✅ TRANSACTION NORMALE\n\n**Risque:** {probability:.1f}%")
            
            with col2:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability,
                    title={'text': "Score de Risque (%)"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#ef4444" if is_fraud else "#10b981"},
                        'steps': [
                            {'range': [0, 30], 'color': "#d1fae5"},
                            {'range': [30, 70], 'color': "#fef3c7"},
                            {'range': [70, 100], 'color': "#fee2e2"}
                        ]
                    }
                ))
                fig.update_layout(height=300, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Recommandations**")
            if is_fraud:
                st.warning("- Bloquer la transaction\n- Contacter le client\n- Créer un rapport")
            else:
                st.info("- Approuver la transaction\n- Surveillance normale")

def show_reports():
    """Rapports."""
    st.subheader("📋 Rapports")
    
    report_type = st.selectbox("Type de rapport", [
        "Synthèse de la fraude",
        "Top clients",
        "Statistiques par type"
    ])
    
    if report_type == "Synthèse de la fraude":
        fraud_summary = api_call("fraud/summary")
        
        if fraud_summary:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Fraudes", f"{fraud_summary.get('total_frauds', 0):,}")
            with col2:
                st.metric("Signalées", fraud_summary.get('flagged', 0))
            with col3:
                st.metric("Précision", f"{fraud_summary.get('precision', 0)*100:.1f}%")
            with col4:
                st.metric("Rappel", f"{fraud_summary.get('recall', 0)*100:.1f}%")
            
            st.markdown("---")
            
            fraud_by_type = api_call("fraud/by-type")
            if fraud_by_type:
                df = pd.DataFrame(fraud_by_type)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df['type'], y=df['total_count'], name='Total', marker_color='#3b82f6'))
                fig.add_trace(go.Bar(x=df['type'], y=df['fraud_count'], name='Fraudes', marker_color='#ef4444'))
                
                fig.update_layout(
                    title="Fraudes vs Total",
                    barmode='group',
                    height=500,
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df, use_container_width=True)
    
    elif report_type == "Top clients":
        n = st.slider("Nombre", 10, 50, 20)
        
        top_customers = api_call("customers/top", params={"n": n})
        
        if top_customers:
            df = pd.DataFrame(top_customers)
            
            fig = px.bar(
                df,
                x='customer_id',
                y='total_amount',
                color='transaction_count',
                title=f"Top {n} clients",
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()