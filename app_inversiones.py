import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import datetime

# ─────────────────────────────────────────────
# 1. CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI.lino", page_icon="🧠", layout="wide")

# ─────────────────────────────────────────────
# 2. ESTILOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
    color: #e6edf3;
}

h1 { color: #58a6ff !important; font-size: 2.8rem !important; font-weight: 700 !important; }
h2, h3 { color: #c9d1d9 !important; font-weight: 600 !important; }

div[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

.semaforo-verde {
    background: linear-gradient(135deg, #0d3321, #1a5c3a);
    border: 2px solid #2ea043;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 0 30px rgba(46,160,67,0.3);
}
.semaforo-rojo {
    background: linear-gradient(135deg, #3d0000, #6b1010);
    border: 2px solid #f85149;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 0 30px rgba(248,81,73,0.3);
}
.semaforo-amarillo {
    background: linear-gradient(135deg, #3d2d00, #6b4c00);
    border: 2px solid #d29922;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 0 30px rgba(210,153,34,0.3);
}
.semaforo-azul {
    background: linear-gradient(135deg, #001f3d, #0d2b4e);
    border: 2px solid #58a6ff;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 0 30px rgba(88,166,255,0.3);
}

.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

.rescate-card {
    background: #1c2128;
    border-left: 4px solid #58a6ff;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

.stButton>button {
    background: linear-gradient(135deg, #238636, #2ea043) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 20px rgba(46,160,67,0.4) !important;
}

.strategy-card {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label {
    color: #8b949e !important;
    font-weight: 600 !important;
}

.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. DICCIONARIO LYNCH
# ─────────────────────────────────────────────
narrativas = {
    "🔄 Cíclica (Minería, Chips, Autos)": {
        "estilo": "Estrategia de Supervivencia Cíclica",
        "mensaje": "Las empresas cíclicas dependen del ritmo del mercado. Promediar es válido solo si el ciclo no ha terminado.",
        "consejo": "No te enamores del activo. Busca tu punto de equilibrio y evalúa si el ciclo aún tiene combustible.",
        "meta_pct": 1.15, "nombre_meta": "Objetivo Lynch Cíclico (+15%)"
    },
    "🚀 Startup / Cripto (Crecimiento Alto / Volatilidad)": {
        "estilo": "Ajuste de Exposición Volátil",
        "mensaje": "Volatilidad extrema. Al promediar multiplicas el rebote potencial, pero también el riesgo de caída.",
        "consejo": "Mantén Stop Loss ajustado. En cripto el suelo puede ser mucho más profundo de lo esperado.",
        "meta_pct": 1.50, "nombre_meta": "Moonshot Cripto (+50%)"
    },
    "🛡️ Defensiva (Consumo, Fibras)": {
        "estilo": "Protección de Capital y Dividendos",
        "mensaje": "Negocios estables. Promediar aquí mejora tu rendimiento por dividendo sin asumir riesgo excesivo.",
        "consejo": "La paciencia es clave. Estas acciones construyen riqueza sólida, no riqueza rápida.",
        "meta_pct": 1.10, "nombre_meta": "Objetivo Defensivo (+10%)"
    },
    "🏛️ ETF / Índice (Inversión Pasiva)": {
        "estilo": "Fortalecimiento de Patrimonio Pasivo",
        "mensaje": "Promediar en un ETF es comprar el mercado a descuento. Alimentas tu interés compuesto.",
        "consejo": "El tiempo es tu mejor aliado. Cada peso extra hoy es una bola de nieve más grande mañana.",
        "meta_pct": 1.08, "nombre_meta": "Crecimiento de Índice (+8%)"
    }
}

# ─────────────────────────────────────────────
# 4. FUNCIONES CORE
# ─────────────────────────────────────────────
def limpiar_ticker(ticker_input):
    dicc = {
        "PEÑOLES": "PE&OLES.MX", "GMEXICO": "GMEXICOB.MX",
        "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD",
        "S&P 500": "VOO", "SP500": "VOO", "NAFTRAC": "NAFTRAC.MX",
        "FIBRAMQ": "FMTY.MX", "WALMEX": "WALMEX.MX",
        "AMXL": "AMXL.MX", "FEMSAUBD": "FEMSAUBD.MX"
    }
    t = ticker_input.upper().strip()
    if t in dicc:
        return dicc[t]
    if "/" in t:
        return t.replace("/", "") + ".MX"
    return t

def calcular_rsi(serie, periodo=14):
    delta = serie.diff()
    gan = delta.clip(lower=0)
    per = -delta.clip(upper=0)
    avg_gan = gan.rolling(periodo).mean()
    avg_per = per.rolling(periodo).mean()
    rs = avg_gan / avg_per.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_macd(serie):
    ema12 = serie.ewm(span=12, adjust=False).mean()
    ema26 = serie.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    señal = macd.ewm(span=9, adjust=False).mean()
    return macd, señal

def calcular_bb(serie, periodo=20):
    media = serie.rolling(periodo).mean()
    std = serie.rolling(periodo).std()
    upper = media + (2 * std)
    lower = media - (2 * std)
    return upper, media, lower

def analizar_semaforo(df, precio_actual, info, categoria):
    """
    Semáforo de 4 colores:
    🔴 NO COMPRAR   — múltiples señales negativas
    🟡 PUEDE SEGUIR CAYENDO — señales mixtas con sesgo bajista
    🔵 NEUTRAL      — señales mixtas sin dirección clara
    🟢 INYECTAR CAPITAL — señales técnicas y fundamentales positivas
    """
    puntos = 0
    razones = []
    alertas = []

    # ── RSI ──
    rsi_serie = calcular_rsi(df['Close'])
    rsi = rsi_serie.iloc[-1]

    if rsi < 30:
        puntos += 3
        razones.append(f"✅ RSI en {rsi:.1f} — Zona de sobreventa fuerte (oportunidad)")
    elif rsi < 40:
        puntos += 1
        razones.append(f"✅ RSI en {rsi:.1f} — Ligeramente sobrevendido")
    elif rsi > 70:
        puntos -= 3
        alertas.append(f"🔴 RSI en {rsi:.1f} — Sobrecomprado, riesgo de corrección")
    elif rsi > 60:
        puntos -= 1
        alertas.append(f"⚠️ RSI en {rsi:.1f} — Calentándose, precaución")
    else:
        razones.append(f"🔵 RSI en {rsi:.1f} — Zona neutral")

    # ── MACD ──
    macd, señal_macd = calcular_macd(df['Close'])
    if macd.iloc[-1] > señal_macd.iloc[-1] and macd.iloc[-2] <= señal_macd.iloc[-2]:
        puntos += 2
        razones.append("✅ MACD cruzó al alza — señal de impulso positivo")
    elif macd.iloc[-1] > señal_macd.iloc[-1]:
        puntos += 1
        razones.append("✅ MACD por encima de señal — tendencia alcista activa")
    elif macd.iloc[-1] < señal_macd.iloc[-1] and macd.iloc[-2] >= señal_macd.iloc[-2]:
        puntos -= 2
        alertas.append("🔴 MACD cruzó a la baja — señal de impulso negativo")
    else:
        puntos -= 1
        alertas.append("⚠️ MACD por debajo de señal — presión vendedora")

    # ── MEDIAS MÓVILES ──
    ma50 = df['Close'].rolling(50).mean().iloc[-1]
    ma200 = df['Close'].rolling(200).mean().iloc[-1] if len(df) >= 200 else None

    if precio_actual > ma50:
        puntos += 1
        razones.append(f"✅ Precio (${precio_actual:.2f}) sobre MA50 (${ma50:.2f})")
    else:
        puntos -= 1
        alertas.append(f"⚠️ Precio bajo MA50 — tendencia de corto plazo bajista")

    if ma200 is not None:
        if precio_actual > ma200:
            puntos += 1
            razones.append(f"✅ Precio sobre MA200 (${ma200:.2f}) — tendencia larga alcista")
        else:
            puntos -= 1
            alertas.append(f"⚠️ Precio bajo MA200 (${ma200:.2f}) — tendencia larga bajista")

    # ── POSICIÓN EN RANGO ANUAL ──
    techo = df['High'].max()
    piso = df['Low'].min()
    rango = techo - piso
    posicion_pct = ((precio_actual - piso) / rango * 100) if rango > 0 else 50

    if posicion_pct < 25:
        puntos += 2
        razones.append(f"✅ Precio en zona baja del rango anual ({posicion_pct:.0f}%) — posible piso")
    elif posicion_pct > 75:
        puntos -= 2
        alertas.append(f"⚠️ Precio en zona alta del rango anual ({posicion_pct:.0f}%) — riesgo de corrección")
    else:
        razones.append(f"🔵 Precio en zona media del rango ({posicion_pct:.0f}%)")

    # ── BOLLINGER BANDS ──
    bb_up, bb_mid, bb_low = calcular_bb(df['Close'])
    if precio_actual < bb_low.iloc[-1]:
        puntos += 2
        razones.append(f"✅ Precio bajo Banda Bollinger inferior — zona de rebote potencial")
    elif precio_actual > bb_up.iloc[-1]:
        puntos -= 2
        alertas.append(f"🔴 Precio sobre Banda Bollinger superior — sobreextendido")

    # ── FUNDAMENTALES (solo acciones, no cripto) ──
    es_cripto = any(c in categoria for c in ["Cripto", "Startup"])
    pe_ratio = None
    if not es_cripto and info:
        try:
            pe_ratio = info.get('trailingPE', None)
            forward_pe = info.get('forwardPE', None)
            profit_margins = info.get('profitMargins', None)
            revenue_growth = info.get('revenueGrowth', None)
            debt_equity = info.get('debtToEquity', None)

            if pe_ratio and pe_ratio > 0:
                if pe_ratio < 15:
                    puntos += 2
                    razones.append(f"✅ P/E de {pe_ratio:.1f} — valuación atractiva (Lynch: busca <15)")
                elif pe_ratio < 25:
                    puntos += 1
                    razones.append(f"✅ P/E de {pe_ratio:.1f} — valuación razonable")
                elif pe_ratio > 50:
                    puntos -= 2
                    alertas.append(f"🔴 P/E de {pe_ratio:.1f} — caro, fundamentales débiles vs precio")
                else:
                    alertas.append(f"⚠️ P/E de {pe_ratio:.1f} — valuación elevada")

            if profit_margins and profit_margins > 0.15:
                puntos += 1
                razones.append(f"✅ Margen de ganancia {profit_margins*100:.1f}% — empresa rentable")
            elif profit_margins and profit_margins < 0:
                puntos -= 1
                alertas.append(f"⚠️ Empresa con pérdidas — margen negativo")

            if revenue_growth and revenue_growth > 0.10:
                puntos += 1
                razones.append(f"✅ Crecimiento de ingresos {revenue_growth*100:.1f}% — empresa expandiéndose")

            if debt_equity and debt_equity > 200:
                puntos -= 1
                alertas.append(f"⚠️ Deuda/Capital elevada ({debt_equity:.0f}) — riesgo financiero")

        except:
            pass

    # ── VOLUMEN ──
    vol_avg = df['Volume'].rolling(20).mean().iloc[-1]
    vol_hoy = df['Volume'].iloc[-1]
    if vol_hoy > vol_avg * 1.5 and df['Close'].iloc[-1] > df['Close'].iloc[-2]:
        puntos += 1
        razones.append("✅ Volumen alto con precio subiendo — compradores activos")
    elif vol_hoy > vol_avg * 1.5 and df['Close'].iloc[-1] < df['Close'].iloc[-2]:
        puntos -= 1
        alertas.append("⚠️ Volumen alto con precio cayendo — vendedores activos")

    # ── DECISIÓN FINAL ──
    if puntos >= 6:
        color = "verde"
        emoji = "🟢"
        decision = "INYECTAR CAPITAL"
        descripcion = "Múltiples señales técnicas y fundamentales positivas alineadas. Es momento de considerar una entrada."
    elif puntos >= 2:
        color = "azul"
        emoji = "🔵"
        decision = "NEUTRAL — ESPERAR"
        descripcion = "Señales mixtas sin dirección clara. Observa más antes de comprometer capital."
    elif puntos >= -2:
        color = "amarillo"
        emoji = "🟡"
        decision = "PUEDE SEGUIR CAYENDO"
        descripcion = "Señales con sesgo bajista. El precio podría continuar corrigiendo. Paciencia."
    else:
        color = "rojo"
        emoji = "🔴"
        decision = "NO COMPRAR AHORA"
        descripcion = "Múltiples señales negativas. Esperar confirmación de piso antes de entrar."

    return {
        "color": color, "emoji": emoji, "decision": decision,
        "descripcion": descripcion, "puntos": puntos,
        "razones": razones, "alertas": alertas,
        "rsi": rsi, "ma50": ma50, "ma200": ma200,
        "techo": techo, "piso": piso, "posicion_pct": posicion_pct,
        "pe_ratio": pe_ratio,
        "bb_up": bb_up.iloc[-1], "bb_low": bb_low.iloc[-1]
    }

def calcular_rescate(cant_actual, inv_total_orig, precio_mercado, cat_sel, techo_y, piso_m):
    """Motor de rescate específico con 3 niveles y análisis de soporte."""
    if cant_actual <= 0 or inv_total_orig <= 0:
        return None

    precio_promedio = inv_total_orig / cant_actual
    perdida_actual = (precio_mercado - precio_promedio) * cant_actual
    pct_perdida = ((precio_mercado / precio_promedio) - 1) * 100

    narrativa = narrativas[cat_sel]
    meta_pct = narrativa["meta_pct"]

    # ── Soporte real del mercado ──
    distancia_piso = ((precio_mercado - piso_m) / precio_mercado) * 100
    stop_loss_sugerido = piso_m * 0.97  # 3% bajo el piso

    # ── 3 niveles de rescate ──
    niveles = []
    porcentajes = [0.25, 0.50, 1.00]
    nombres = ["Nivel 1 — Conservador (25%)", "Nivel 2 — Moderado (50%)", "Nivel 3 — Agresivo (100%)"]

    for pct, nombre in zip(porcentajes, nombres):
        capital_extra = inv_total_orig * pct
        nuevos_titulos = capital_extra / precio_mercado
        titulos_finales = cant_actual + nuevos_titulos
        inv_final = inv_total_orig + capital_extra
        nuevo_promedio = inv_final / titulos_finales
        precio_meta = nuevo_promedio * meta_pct
        ganancia_en_meta = (precio_meta - nuevo_promedio) * titulos_finales
        distancia_a_tablas = ((nuevo_promedio / precio_mercado) - 1) * 100

        niveles.append({
            "nombre": nombre,
            "capital_extra": capital_extra,
            "nuevos_titulos": nuevos_titulos,
            "titulos_finales": titulos_finales,
            "inv_final": inv_final,
            "nuevo_promedio": nuevo_promedio,
            "precio_meta": precio_meta,
            "ganancia_en_meta": ganancia_en_meta,
            "distancia_a_tablas": distancia_a_tablas
        })

    return {
        "precio_promedio": precio_promedio,
        "perdida_actual": perdida_actual,
        "pct_perdida": pct_perdida,
        "niveles": niveles,
        "stop_loss": stop_loss_sugerido,
        "distancia_piso": distancia_piso,
        "techo_y": techo_y,
        "piso_m": piso_m,
        "narrativa": narrativa
    }

# ─────────────────────────────────────────────
# 5. SESSION STATE
# ─────────────────────────────────────────────
if 'community_strategies' not in st.session_state:
    st.session_state['community_strategies'] = [
        {
            'autor': 'Lino', 'activo': 'BTC-USD',
            'categoria': '🚀 Startup / Cripto',
            'estrategia': 'Hacer DCA mensual hasta los $100k. Comprar fuerte si rompe el piso de los $50k.',
            'fecha': '2026-03-16'
        }
    ]

# ─────────────────────────────────────────────
# 6. HEADER
# ─────────────────────────────────────────────
col_h1, col_h2 = st.columns([8, 2])
with col_h1:
    st.title("🧠 AI.lino")
    st.markdown("### Simulador de Mercado · Análisis VIP · Comunidad de Estrategias")
with col_h2:
    st.write("<br>", unsafe_allow_html=True)
    st.link_button("🎁 Apoyar el proyecto", "https://buymeacoffee.com/Hugo.lino", use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# 7. MODOS
# ─────────────────────────────────────────────
modo = st.radio(
    "¿Qué deseas hacer hoy?",
    ["🔍 Modo Explorador (Gratis)", "💼 Modo Portafolio (Suite Premium)", "🤝 Comunidad de Estrategias"],
    horizontal=True
)

# ═══════════════════════════════════════════════
# MODOS EXPLORADOR Y PORTAFOLIO
# ═══════════════════════════════════════════════
if "Comunidad" not in modo:
    col1, col2 = st.columns([1, 2])
    with col1:
        ticker_input = st.text_input("Símbolo (ej. TSLA, GMEXICO, BTC, SOL):", "TSLA")
        ticker_limpio = limpiar_ticker(ticker_input)

    with col2:
        categoria = st.selectbox("Categoría de Activo (Estilo Peter Lynch):", list(narrativas.keys()))

    # Inputs según modo
    if "Explorador" in modo:
        inversion_sim = st.number_input("💰 Capital que deseas simular (USD/MXN):", min_value=100.0, value=10000.0)
        cant = 0.0
        total_inv = 0.0
    else:
        c1, c2 = st.columns(2)
        with c1:
            cant = st.number_input("📦 Títulos / Fracciones que tienes:", min_value=0.0, value=10.0, format="%0.8f")
        with c2:
            total_inv = st.number_input("💵 Costo Total Invertido ($):", min_value=0.01, value=5000.0)
        inversion_sim = 0.0

    ejecutar = st.button("📊 Ejecutar Motor AI.lino", use_container_width=False)

    if ejecutar:
        with st.spinner("Conectando con mercados en tiempo real..."):
            try:
                stock = yf.Ticker(ticker_limpio)
                df_1y = stock.history(period="1y")
                df_1m = stock.history(period="1mo", interval="1h")

                if df_1y.empty:
                    st.error(f"❌ No se encontraron datos para '{ticker_input}'. Verifica el símbolo.")
                    st.stop()

                # Datos base
                precio_actual = df_1y['Close'].iloc[-1]
                techo_y = df_1y['High'].max()
                piso_m = df_1y.tail(22)['Low'].min()
                piso_anual = df_1y['Low'].min()

                # Info fundamental
                try:
                    info = stock.info
                    nombre_empresa = info.get('longName', ticker_limpio)
                    sector = info.get('sector', 'N/A')
                    pais = info.get('country', 'N/A')
                except:
                    info = {}
                    nombre_empresa = ticker_limpio
                    sector = 'N/A'
                    pais = 'N/A'

                st.success(f"🟢 Datos obtenidos en tiempo real · **{nombre_empresa}** · Sector: {sector}")

                # ─────────────────────────────
                # SEMÁFORO DE DECISIÓN
                # ─────────────────────────────
                analisis = analizar_semaforo(df_1y, precio_actual, info, categoria)

                st.markdown("## 🚦 Semáforo de Decisión AI.lino")

                clase_css = f"semaforo-{analisis['color']}"
                st.markdown(f"""
                <div class="{clase_css}">
                    <h1 style="font-size:3.5rem; margin:0;">{analisis['emoji']}</h1>
                    <h2 style="color:white; margin:8px 0;">{analisis['decision']}</h2>
                    <p style="color:#ccc; font-size:1.1rem; margin:0;">{analisis['descripcion']}</p>
                    <p style="color:#aaa; margin-top:12px; font-size:0.9rem;">Score técnico: <b>{analisis['puntos']:+d} puntos</b></p>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                # Razones y alertas
                col_r, col_a = st.columns(2)
                with col_r:
                    st.markdown("#### ✅ Señales Positivas")
                    if analisis['razones']:
                        for r in analisis['razones']:
                            st.markdown(f"- {r}")
                    else:
                        st.markdown("- Sin señales positivas detectadas")

                with col_a:
                    st.markdown("#### ⚠️ Alertas y Riesgos")
                    if analisis['alertas']:
                        for a in analisis['alertas']:
                            st.markdown(f"- {a}")
                    else:
                        st.markdown("- Sin alertas detectadas")

                st.markdown("---")

                # ─────────────────────────────
                # PANEL DE INDICADORES
                # ─────────────────────────────
                st.markdown("## 📐 Panel Analítico")

                i1, i2, i3, i4, i5 = st.columns(5)
                i1.metric("💲 Precio Actual", f"${precio_actual:,.2f}")
                i2.metric("📊 RSI (14D)", f"{analisis['rsi']:.1f}",
                          delta="Sobrevendido" if analisis['rsi'] < 35 else ("Sobrecomprado" if analisis['rsi'] > 65 else "Neutral"))
                i3.metric("📈 MA50", f"${analisis['ma50']:,.2f}",
                          delta=f"{((precio_actual/analisis['ma50'])-1)*100:.1f}% vs precio")
                i4.metric("🔺 Techo Anual", f"${techo_y:,.2f}")
                i5.metric("🔻 Piso Anual", f"${piso_anual:,.2f}")

                if analisis['pe_ratio']:
                    p1, p2, p3 = st.columns(3)
                    p1.metric("📋 P/E Ratio", f"{analisis['pe_ratio']:.1f}")
                    p2.metric("📊 BB Superior", f"${analisis['bb_up']:,.2f}")
                    p3.metric("📊 BB Inferior", f"${analisis['bb_low']:,.2f}")

                st.markdown("---")

                # ─────────────────────────────
                # MODO EXPLORADOR
                # ─────────────────────────────
                if "Explorador" in modo:
                    st.markdown(f"## 🔍 Tablero AI.lino: {nombre_empresa}")
                    acciones_posibles = inversion_sim / precio_actual
                    st.info(f"💼 Con **${inversion_sim:,.2f}** puedes comprar **{acciones_posibles:.4f}** títulos al precio actual de **${precio_actual:,.2f}**")

                    # Gráfica histórica
                    st.markdown("#### 📈 Histórico 1 Año")
                    st.line_chart(df_1y['Close'])

                    # Radar último mes
                    if not df_1m.empty:
                        st.markdown("#### 📡 Radar Último Mes (1H)")
                        st.line_chart(df_1m['Close'])

                # ─────────────────────────────
                # MODO PORTAFOLIO
                # ─────────────────────────────
                else:
                    precio_promedio = total_inv / cant if cant > 0 else 0
                    valor_actual = precio_actual * cant
                    ganancia_perdida = valor_actual - total_inv
                    rendimiento = (ganancia_perdida / total_inv * 100) if total_inv > 0 else 0

                    st.markdown(f"## 💎 Suite VIP AI.lino: {nombre_empresa}")

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Tu Promedio", f"${precio_promedio:,.2f}")
                    m2.metric("Precio Mercado", f"${precio_actual:,.2f}",
                              delta=f"{((precio_actual/precio_promedio)-1)*100:.1f}%" if precio_promedio > 0 else None)
                    m3.metric("Rendimiento", f"{rendimiento:.2f}%")
                    m4.metric("Valor Hoy", f"${valor_actual:,.2f}")

                    # ── TradingView ──
                    tv_symbol = ticker_limpio.replace(".MX", "").replace("-", "")
                    tv_widget = f"""
                    <div class="tradingview-widget-container">
                    <div id="tv_chart"></div>
                    <script src="https://s3.tradingview.com/tv.js"></script>
                    <script>
                    new TradingView.widget({{
                        "width": "100%", "height": 420,
                        "symbol": "{tv_symbol}",
                        "interval": "D",
                        "theme": "dark",
                        "style": "1",
                        "locale": "es",
                        "toolbar_bg": "#161b22",
                        "hide_side_toolbar": false,
                        "container_id": "tv_chart"
                    }});
                    </script></div>"""
                    components.html(tv_widget, height=430)

                    st.markdown("---")

                    # ── MOTOR DE RESCATE ──
                    if rendimiento < 0:
                        rescate = calcular_rescate(cant, total_inv, precio_actual, categoria, techo_y, piso_m)

                        if rescate:
                            st.markdown("## 🛡️ Motor de Rescate AI.lino")
                            st.error(f"📉 Pérdida actual: **${abs(rescate['perdida_actual']):,.2f}** ({rescate['pct_perdida']:.1f}%)")

                            # Contexto Lynch
                            st.markdown(f"""
                            <div class="card">
                                <b>Filosofía: {rescate['narrativa']['estilo']}</b><br>
                                {rescate['narrativa']['mensaje']}
                            </div>
                            """, unsafe_allow_html=True)

                            # Soporte y Stop Loss
                            col_s1, col_s2 = st.columns(2)
                            with col_s1:
                                dist_color = "🟢" if rescate['distancia_piso'] > 5 else "🔴"
                                st.info(f"{dist_color} **Piso mensual:** ${piso_m:,.2f} · Distancia: {rescate['distancia_piso']:.1f}% abajo")
                            with col_s2:
                                st.warning(f"🛑 **Stop Loss sugerido:** ${rescate['stop_loss']:,.2f} (3% bajo el piso)")

                            # Sala de Simulación
                            st.markdown("### 🎯 Sala de Simulación — 3 Niveles de Rescate")
                            st.caption(f"Objetivo de salida: **{rescate['narrativa']['nombre_meta']}** ({rescate['narrativa']['meta_pct']*100-100:.0f}% sobre tu nuevo promedio)")

                            for nivel in rescate['niveles']:
                                color_borde = "#2ea043" if "Conservador" in nivel['nombre'] else ("#d29922" if "Moderado" in nivel['nombre'] else "#f85149")
                                st.markdown(f"""
                                <div class="rescate-card" style="border-left-color: {color_borde};">
                                    <b>{nivel['nombre']}</b><br>
                                    💵 Capital a inyectar: <b>${nivel['capital_extra']:,.2f}</b> · 
                                    Títulos nuevos: <b>{nivel['nuevos_titulos']:.4f}</b><br>
                                    📊 Nuevo promedio: <b>${nivel['nuevo_promedio']:,.2f}</b> 
                                    (antes: <b>${rescate['precio_promedio']:,.2f}</b>) · 
                                    Reducción: <b>{nivel['distancia_a_tablas']:.1f}% a tablas</b><br>
                                    🎯 Precio objetivo ({rescate['narrativa']['nombre_meta']}): 
                                    <b>${nivel['precio_meta']:,.2f}</b> → 
                                    Ganancia neta: <b>${nivel['ganancia_en_meta']:,.2f}</b>
                                </div>
                                """, unsafe_allow_html=True)

                            st.warning(f"⚠️ **Consejo Lynch:** {rescate['narrativa']['consejo']}")

                    elif rendimiento > 0:
                        st.success(f"🎉 **¡En ganancia! +${ganancia_perdida:,.2f} ({rendimiento:.2f}%)**")

                        # Objetivo de toma de ganancias
                        narrativa = narrativas[categoria]
                        precio_meta = precio_promedio * narrativa["meta_pct"]
                        if precio_actual >= precio_meta:
                            st.balloons()
                            st.success(f"🏆 **¡Alcanzaste el objetivo {narrativa['nombre_meta']}!** Considera tomar ganancias parciales.")
                        else:
                            falta = precio_meta - precio_actual
                            st.info(f"🎯 Objetivo {narrativa['nombre_meta']}: **${precio_meta:,.2f}** · Faltan **${falta:,.2f}** ({((precio_meta/precio_actual)-1)*100:.1f}%)")

            except Exception as e:
                st.error(f"⚠️ Error inesperado: {e}")
                st.info("Verifica que el símbolo sea correcto. Ejemplos: TSLA, AAPL, BTC-USD, GMEXICOB.MX, ETH-USD, SOL-USD")

# ═══════════════════════════════════════════════
# COMUNIDAD
# ═══════════════════════════════════════════════
else:
    st.markdown("## 🤝 Comunidad de Estrategias AI.lino")
    st.caption("Comparte y aprende de las mejores jugadas de la comunidad.")

    col_c1, col_c2 = st.columns([1, 2])

    with col_c1:
        st.markdown("### 📝 Publica tu Estrategia")
        with st.form("crear_estrategia"):
            autor = st.text_input("Tu Nombre o Nickname:", placeholder="ej. Lobo de Wall Street")
            activo = st.text_input("Activo / Símbolo:", placeholder="ej. BTC-USD, GMEXICO, S&P 500").upper()
            cat_comm = st.selectbox("Categoría:", list(narrativas.keys()))
            estrategia = st.text_area("Tu Estrategia Detallada:", placeholder="ej. Comprar si rompe la resistencia de los $X, buscando el techo en $Y. Stop Loss en $Z.", height=120)
            publicar = st.form_submit_button("📢 Publicar en Comunidad")
            if publicar:
                if autor and activo and estrategia:
                    st.session_state['community_strategies'].insert(0, {
                        'autor': autor, 'activo': activo,
                        'categoria': cat_comm, 'estrategia': estrategia,
                        'fecha': str(datetime.date.today())
                    })
                    st.success("✅ Estrategia publicada.")
                    st.rerun()
                else:
                    st.warning("Completa todos los campos antes de publicar.")

    with col_c2:
        st.markdown("### 📡 Feed de Estrategias Públicas")
        for estr in st.session_state['community_strategies']:
            st.markdown(f"""
            <div class="strategy-card">
                <b>👤 Autor: {estr['autor']}</b><br>
                <small>Activo: {estr['activo']} | Categoría: {estr.get('categoria','—')} | Publicado: {estr['fecha']}</small><br><br>
                {estr['estrategia']}
            </div>
            """, unsafe_allow_html=True)
ailino_app.py
Mostrando ailino_app.py
