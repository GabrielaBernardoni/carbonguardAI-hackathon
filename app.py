import streamlit as st
import pandas as pd
import json
import random
from groq import Groq
import folium
from streamlit_folium import st_folium

# 1. CONFIGURAÇÃO DA PÁGINA 
st.set_page_config(page_title="CarbonGuard AI", page_icon="🌿", layout="wide")

# 2. ESTILIZAÇÃO CSS 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top left, #1a2e24, #0e1117);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}

    /* Título */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00ffa3, #00b8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle { font-size: 1.2rem; color: #b0b0b0; margin-bottom: 30px; }

    /* Cards e Botões */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #fff; }
    .metric-label { font-size: 0.9rem; text-transform: uppercase; color: #00ffa3; }

    div.stButton > button {
        background: linear-gradient(90deg, #00ffa3 0%, #00bc7d 100%);
        color: #000;
        font-weight: bold;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-transform: uppercase;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 163, 0.5);
        color: #000;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 5px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00ffa3 !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

# 3. API 
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.warning("⚠️ Configure o .streamlit/secrets.toml")
        st.stop()
except:
    st.error("⚠️ Erro de Configuração: API Key.")
    st.stop()

# 4. DADOS
@st.cache_data
def load_registry():
    try:
        return pd.read_csv("carbon_registry.csv")
    except:
        return pd.DataFrame()

df_registry = load_registry()

# 5. MAPA 
def render_mapa_satelite(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles=None)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Satélite', overlay=False, control=True
    ).add_to(m)
    folium.Circle(location=[lat, lon], radius=2000, color='#00ffa3', fill=True, fill_opacity=0.1, weight=2).add_to(m)
    folium.Marker([lat, lon], popup="Projeto", icon=folium.Icon(color="green", icon="leaf")).add_to(m)
    return m

def carregar_evidencias(arquivo):
    if "AM_Forest" in arquivo:
        return {
            "coords": {"lat": -3.4653, "lon": -62.2159},
            "dados": {
                "satelite_optico": {"analise": "Biomassa Densa", "ndvi": "0.85 (Excelente)"},
                "radar_sar": {"estrutura": "Canopy Fechado", "desmatamento": "0%"},
                "iot_sensores": {"bioacustica": "Fauna rica", "motosserras": 0},
                "juridico": {"licenciamento": "Regular", "ti": "Não consta"}
            }
        }
    elif "MT_Soy" in arquivo:
        return {
            "coords": {"lat": -12.55, "lon": -55.72},
            "dados": {
                "satelite_optico": {"analise": "Verde (Copa)", "ndvi": "0.70 (Médio)"},
                "radar_sar": {"estrutura": "Perda de sub-bosque", "desmatamento": "Trilhas ocultas"},
                "iot_sensores": {"bioacustica": "Baixa diversidade", "motosserras": 42},
                "juridico": {"licenciamento": "Em análise", "ti": "Não consta"}
            }
        }
    else: 
        return {
            "coords": {"lat": -3.20, "lon": -52.20},
            "dados": {
                "satelite_optico": {"analise": "Intacto", "ndvi": "0.88"},
                "radar_sar": {"estrutura": "Preservado", "desmatamento": "0%"},
                "iot_sensores": {"bioacustica": "Normal", "motosserras": 0},
                "juridico": {"licenciamento": "FALSIFICADO", "ti": "100% (TI Xingu)"}
            }
        }

# 6. HERO HEADER 
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown('<h1 class="hero-title">CarbonGuard AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Auditoria Forense de Carbono via Satélite & Blockchain.</p>', unsafe_allow_html=True)
with c2:
    preco_atual = 12.50 + random.uniform(-0.5, 0.8)
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">📡 Cotação Global (Token CO2)</div>
        <div class="metric-value">US$ {preco_atual:.2f} <span style="font-size:16px; color:#00ffa3;">▲ +1.2%</span></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 7. DASHBOARD 
col_sidebar, col_main = st.columns([1, 2.5])

# ESQUERDA: CONTROLES
with col_sidebar:
    st.markdown("### ⚙️ Painel de Operações")
    with st.container():
        st.markdown('<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">', unsafe_allow_html=True)
        st.caption("📂 SELEÇÃO DE ARQUIVO")
        arquivo_selecionado = st.selectbox("Pacote de Evidências:", 
            ["AM_Forest_Preservation_V4.json", "MT_Soy_Integration_Report.json", "PA_Altamira_Land_Registry.json"], label_visibility="collapsed")
        
        st.caption("🔢 SERIAL NUMBER")
        opcao_serial = st.selectbox("Serial:", 
            ["AM-2024-8892 (50.000 tCO2e)", "MT-2021-0045 (RETIRED)", "BR-INVALID-000"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    parts = opcao_serial.split(" ")
    serial_limpo = parts[0]
    qtd_creditos = 50000 if "50.000" in opcao_serial else (12000 if "RETIRED" in opcao_serial else 0)

    if qtd_creditos > 0:
        valor_total = qtd_creditos * preco_atual
        carros = int(qtd_creditos * 0.21)
        st.markdown(f"""
        <div style="margin-top: 20px; background: linear-gradient(135deg, rgba(0, 255, 163, 0.1), rgba(0, 255, 163, 0.0)); border: 1px solid #00ffa3; border-radius: 10px; padding: 15px;">
            <div style="color: #00ffa3; font-size: 12px; font-weight: bold; letter-spacing: 1px;">VALOR DA TRANSAÇÃO</div>
            <div style="color: #fff; font-size: 24px; font-weight: bold;">US$ {valor_total:,.2f}</div>
            <div style="color: #ccc; font-size: 12px; margin-top: 5px;">🚗 -{carros:,} carros/ano.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    btn_auditar = st.button("🚀 INICIAR AUDITORIA")

cenario = carregar_evidencias(arquivo_selecionado)

# LÓGICA DO BOTÃO 
if btn_auditar:
    registro = df_registry[df_registry['serial_number'] == serial_limpo]
    status_fin = registro.iloc[0].to_dict() if not registro.empty else "REGISTRO NÃO ENCONTRADO"
    
    prompt_sistema = """
    Voce e o CarbonGuard, uma IA especializada em Auditoria Forense Ambiental.
    Cruze multiplas fontes de dados para validar a integridade de um credito de carbono.
    
    FONTES:
    1. REGISTRO OFICIAL: Status legal do serial number.
    2. DOSSIE TECNICO: Dados de Satelite, Radar, IoT, Juridico e Financeiro.
    3. OFERTA: O que esta sendo vendido.
    
    LOGICA DE DETECCAO:
    - Se Registro diz 'Retired', e Double Spending (Fraude).
    - Se Satelite ve floresta, mas Radar/IoT detecta degradacao, e Fraude Oculta.
    - Se imagem e boa, mas Juridico aponta Terra Indigena, e Grilagem.
    
    SAIDA:
    Forneca um relatorio profissional em Portugues.
    Nao use emojis no texto técnico.
    Comece com o VEREDITO: "APROVADO", "REPROVADO" ou "SUSPEITO".
    Liste as evidencias que suportam sua decisao em topicos.
    """
    
    prompt_usuario = f"""
    ANALISE ESTE CASO:
    
    [A] DADOS DO REGISTRO OFICIAL (Serial: {serial_limpo}):
    {status_fin}
    
    [B] OFERTA DE VENDA:
    Quantidade: {qtd_creditos} tCO2
    
    [C] DOSSIE DE EVIDENCIAS:
    {json.dumps(cenario['dados'], indent=2)}
    """
    
    with st.spinner("🔄 Processando Análise Forense..."):
        try:
            chat = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )
            laudo = chat.choices[0].message.content
            # Salva no estado
            st.session_state['laudo'] = laudo
            st.session_state['dados_atuais'] = cenario['dados']
            
        except Exception as e:
            st.error(f"Erro na IA: {e}")

# DIREITA: RESULTADOS
with col_main:
    tab1, tab2, tab3 = st.tabs(["🛰️ VISÃO SATÉLITE", "📊 DADOS TÉCNICOS", "📑 LAUDO IA"])
    
    with tab1:
        st.markdown(f'<div style="background:black; padding:5px; border-radius:10px;">', unsafe_allow_html=True)
        mapa = render_mapa_satelite(cenario['coords']['lat'], cenario['coords']['lon'])
        st_folium(mapa, height=450, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with tab2:
        st.markdown("### Evidências Coletadas")
        st.json(cenario['dados'])

    with tab3:
        # Exibe apenas se existir um laudo na memória
        if 'laudo' not in st.session_state:
            st.info("👈 Aguardando comando para iniciar varredura...")
        else:
            laudo_atual = st.session_state['laudo']
            
            if "REPROVADO" in laudo_atual:
                st.error("🚨 REPROVADO: RISCO CRÍTICO DETECTADO")
            elif "SUSPEITO" in laudo_atual or "NÃO ENCONTRADO" in laudo_atual:
                st.warning("⚠️ ALERTA: OPERAÇÃO SUSPEITA")
            else:
                st.success("✅ APROVADO: INTEGRIDADE VERIFICADA")
                # SEM BALÕES AQUI
            
            st.markdown(laudo_atual)

# 8. CHATBOT 
st.write("---")
if 'laudo' in st.session_state:
    st.markdown("### 💬 Assistente Virtual")
    if q := st.chat_input("Pergunte sobre os detalhes da auditoria..."):
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            prompt_chat = f"Contexto: {st.session_state['laudo']}\nDados: {st.session_state['dados_atuais']}\nPergunta: {q}\nResponda curto e técnico."
            r = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_chat}],
                model="llama-3.3-70b-versatile"
            )
            st.write(r.choices[0].message.content)