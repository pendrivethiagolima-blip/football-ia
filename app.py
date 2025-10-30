import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Football IA Analytics",
    page_icon="⚽", 
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e40af;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #1e40af;
    }
</style>
""", unsafe_allow_html=True)

# Dados das partidas
partidas = [
    {
        'id': 1, 'time_casa': 'Manchester City', 'time_visitante': 'Liverpool',
        'liga': 'Premier League', 'data': '2024-01-20 17:30:00',
        'prob_over_gol_jogo': 85, 'prob_over_gol_ht': 72,
        'prob_over_escanteio_ht': 68, 'prob_over_escanteio_jogo': 81,
        'prob_over_cartao_jogo': 65, 'prob_over_cartao_ht': 48,
        'prob_escanteio_10min': 82
    },
    {
        'id': 2, 'time_casa': 'Real Madrid', 'time_visitante': 'Barcelona', 
        'liga': 'La Liga', 'data': '2024-01-20 20:00:00',
        'prob_over_gol_jogo': 78, 'prob_over_gol_ht': 65,
        'prob_over_escanteio_ht': 72, 'prob_over_escanteio_jogo': 84, 
        'prob_over_cartao_jogo': 71, 'prob_over_cartao_ht': 52,
        'prob_escanteio_10min': 79
    }
]

# Ranking dados
ranking_escanteios = [
    {'time': 'Manchester City', 'escanteios_ht': 6.8, 'escanteios_ft': 12.5},
    {'time': 'Bayern Munich', 'escanteios_ht': 6.2, 'escanteios_ft': 11.8},
    {'time': 'Liverpool', 'escanteios_ht': 5.9, 'escanteios_ft': 11.2}
]

ranking_gols_ht = [
    {'time': 'Real Madrid', 'gols_ht': 1.8},
    {'time': 'PSG', 'gols_ht': 1.7}, 
    {'time': 'Manchester City', 'gols_ht': 1.6}
]

def main():
    st.markdown('<h1 class="main-header">⚽ Football IA Analytics</h1>', unsafe_allow_html=True)
    
    # Menu lateral
    with st.sidebar:
        st.header("🎯 Navegação")
        pagina = st.selectbox("Selecione:", [
            "Dashboard Pré-Live", 
            "🏆 Ranking Escanteios",
            "⚽ Ranking Gols HT",
            "🚀 Escanteios 10min"
        ])
        
        st.header("🔧 Filtros")
        prob_minima = st.slider("Probabilidade Mínima (%)", 50, 95, 75)
    
    # Páginas
    if pagina == "Dashboard Pré-Live":
        mostrar_dashboard(partidas, prob_minima)
    elif pagina == "🏆 Ranking Escanteios":
        mostrar_ranking_escanteios()
    elif pagina == "⚽ Ranking Gols HT":
        mostrar_ranking_gols_ht()
    else:
        mostrar_escanteios_10min(partidas)

def mostrar_dashboard(partidas, prob_minima):
    st.header("📊 Dashboard Pré-Live")
    
    for partida in partidas:
        if partida['prob_over_gol_jogo'] >= prob_minima:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.subheader(f"🏟️ {partida['time_casa']} vs {partida['time_visitante']}")
                    st.write(f"**Liga:** {partida['liga']}")
                    st.write(f"**Data:** {partida['data']}")
                
                with col2:
                    st.metric("Over Gol Jogo", f"{partida['prob_over_gol_jogo']}%")
                    st.metric("Over Gol HT", f"{partida['prob_over_gol_ht']}%")
                    st.metric("Escanteios HT", f"{partida['prob_over_escanteio_ht']}%")
                
                with col3:
                    st.metric("Escanteios Jogo", f"{partida['prob_over_escanteio_jogo']}%")
                    st.metric("Cartões Jogo", f"{partida['prob_over_cartao_jogo']}%")
                    st.metric("Escanteios 10min", f"{partida['prob_escanteio_10min']}%")
                
                st.markdown('</div>', unsafe_allow_html=True)

def mostrar_ranking_escanteios():
    st.header("🏆 Ranking - Maiores Médias de Escanteios")
    df = pd.DataFrame(ranking_escanteios)
    st.dataframe(df, use_container_width=True)
    
    # Gráfico
    fig = px.bar(
        df, 
        x='time', 
        y=['escanteios_ht', 'escanteios_ft'],
        title='Escanteios HT vs FT',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_ranking_gols_ht():
    st.header("⚽ Ranking - Maiores Médias de Gols no 1° Tempo") 
    df = pd.DataFrame(ranking_gols_ht)
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(df, x='time', y='gols_ht', title='Gols no 1° Tempo')
    st.plotly_chart(fig, use_container_width=True)

def mostrar_escanteios_10min(partidas):
    st.header("🚀 Partidas com Alta Probabilidade de +1 Escanteio (0-10min)")
    
    for partida in partidas:
        if partida['prob_escanteio_10min'] >= 75:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{partida['time_casa']} vs {partida['time_visitante']}**")
                st.write(f"Liga: {partida['liga']}")
            with col2:
                st.metric("Probabilidade", f"{partida['prob_escanteio_10min']}%")

if __name__ == "__main__":
    main()
