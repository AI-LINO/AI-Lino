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
    line-height: 1.8;
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

.escalon-card {
    border-radius: 12px;
    padding: 16px 20px;
    margin: 8px 0;
    line-height: 1.8;
    border-left: 6px solid #ccc;
}
.escalon-activo {
    background: linear-gradient(135deg, #1a1f2e, #1c2540);
    border-left-color: #58a6ff !important;
    box-shadow: 0 0 20px rgba(88,166,255,0.2);
}
.escalon-pendiente {
    background: #1c2128;
    border-left-color: #30363d !important;
    opacity: 0.85;
}
.login-box {
    max-width: 400px;
    margin: 60px auto;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 0 40px rgba(88,166,255,0.15);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. SISTEMA DE LOGIN
# ─────────────────────────────────────────────
def verificar_login(usuario, password):
    try:
        return (usuario.strip() == st.secrets["auth"]["username"] and
                password == st.secrets["auth"]["password"])
    except Exception:
        return False

def pantalla_login():
    st.markdown("""
    <div style='text-align:center; padding:50px 0 20px 0;'>
        <span style='font-size:3.5rem;'>🧠</span>
        <h1 style='color:#58a6ff; margin:10px 0;'>AI.lino</h1>
        <p style='color:#8b949e; font-size:1.1rem;'>Motor de Inversión — Acceso Privado</p>
    </div>
    """, unsafe_allow_html=True)
    col = st.columns([1, 1.1, 1])[1]
    with col:
        with st.form("login_form"):
            st.markdown("#### 🔐 Iniciar Sesión")
            usuario  = st.text_input("Usuario", placeholder="tu usuario")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            entrar   = st.form_submit_button("Entrar →", use_container_width=True)
            if entrar:
                if verificar_login(usuario, password):
                    st.session_state["autenticado"] = True
                    st.session_state["usuario_nombre"] = st.secrets["auth"].get("nombre", usuario)
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos.")

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# ─────────────────────────────────────────────
# FUNCIÓN: ESCALONES DE SOPORTE
# ─────────────────────────────────────────────
def calcular_escalones(df_1y, precio_actual, piso_m, piso_anual, narrativa, cant, total_inv):
    """
    Calcula los mínimos reales de cada mes del año (de más reciente a más antiguo),
    filtra solo los que están DEBAJO del precio actual (pisos ya rotos o en riesgo),
    y los vincula con los 3 niveles de rescate.
    Retorna lista de escalones con su nivel sugerido y estado de alerta.
    """
    hoy = pd.Timestamp.now(tz=df_1y.index.tz)
    escalones_raw = []

    # Recolectar mínimo de cada mes en el historial (hasta 12 meses atrás)
    for i in range(1, 13):
        mes  = (hoy.month - i - 1) % 12 + 1
        anio = hoy.year if hoy.month - i > 0 else hoy.year - 1
        # ajuste fino de año
        offset = hoy.month - i
        if offset <= 0:
            anio = hoy.year - 1
            mes  = 12 + offset
        else:
            anio = hoy.year
            mes  = offset

        bloque = df_1y[(df_1y.index.month == mes) & (df_1y.index.year == anio)]
        if not bloque.empty:
            low_mes  = float(bloque['Low'].min())
            nombre_m = pd.Timestamp(year=anio, month=mes, day=1).strftime("%b %Y")
            escalones_raw.append((low_mes, nombre_m))

    # Eliminar duplicados y ordenar de mayor a menor
    vistos = set()
    escalones_uniq = []
    for v, n in sorted(escalones_raw, reverse=True):
        key = round(v, 2)
        if key not in vistos:
            vistos.add(key)
            escalones_uniq.append((v, n))

    # Solo los que están por DEBAJO del precio actual (soporte roto o en riesgo)
    debajo = [(v, n) for v, n in escalones_uniq if v < precio_actual]

    # Agregar piso anual al final si no está ya
    if piso_anual < precio_actual and not any(abs(v - piso_anual) < 1.0 for v, _ in debajo):
        debajo.append((piso_anual, "🔻 Piso Anual"))

    # Tomar máximo 4 escalones más relevantes
    debajo = debajo[:4]

    # Vincular cada escalón con nivel de rescate
    nivel_labels = [
        ("Nivel 1 — Conservador (25%)", "#2ea043"),
        ("Nivel 2 — Moderado (50%)",    "#d29922"),
        ("Nivel 3 — Agresivo (100%)",   "#f85149"),
        ("Zona Extrema / Stop Loss",    "#8b0000"),
    ]

    precio_promedio = total_inv / cant if cant > 0 else 0
    meta_pct = narrativa["meta_pct"]

    resultado = []
    for idx, (precio_esc, nombre_m) in enumerate(debajo):
        nivel_nombre, nivel_color = nivel_labels[idx] if idx < len(nivel_labels) else nivel_labels[-1]

        # Calcular simulación si se entra en este escalón
        pct_rescate = [0.25, 0.50, 1.00, 1.00][idx]
        capital_extra   = total_inv * pct_rescate
        nuevos_titulos  = capital_extra / precio_esc if precio_esc > 0 else 0
        titulos_finales = cant + nuevos_titulos
        inv_final       = total_inv + capital_extra
        nuevo_promedio  = inv_final / titulos_finales if titulos_finales > 0 else 0
        precio_meta     = nuevo_promedio * meta_pct
        ganancia_meta   = (precio_meta - nuevo_promedio) * titulos_finales

        # Estado de alerta
        dist_pct = ((precio_actual - precio_esc) / precio_actual) * 100
        if dist_pct <= 2:
            alerta = "🔴 PRECIO EN ZONA — ¡Decidir ahora!"
            estado = "activo"
        elif dist_pct <= 6:
            alerta = "🟡 CERCA — Preparar capital"
            estado = "activo"
        else:
            alerta = f"🔵 A {dist_pct:.1f}% de distancia"
            estado = "pendiente"

        resultado.append({
            "precio":         precio_esc,
            "nombre_mes":     nombre_m,
            "nivel_nombre":   nivel_nombre,
            "nivel_color":    nivel_color,
            "alerta":         alerta,
            "estado":         estado,
            "dist_pct":       dist_pct,
            "capital_extra":  capital_extra,
            "nuevo_promedio": nuevo_promedio,
            "precio_meta":    precio_meta,
            "ganancia_meta":  ganancia_meta,
            "nuevos_titulos": nuevos_titulos,
        })

    return resultado

# ─────────────────────────────────────────────
# 4. DICCIONARIO LYNCH
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
        # Mexico
        "PEÑOLES": "PE&OLES.MX", "GMEXICO": "GMEXICOB.MX",
        "FIBRAMQ": "FMTY.MX",    "WALMEX": "WALMEX.MX",
        "AMXL": "AMXL.MX",       "FEMSAUBD": "FEMSAUBD.MX",
        "NAFTRAC": "NAFTRAC.MX",
        # Cripto
        "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD",
        # ETFs
        "S&P 500": "VOO", "SP500": "VOO",
        # Europa nombres comunes
        "MONDI": "MNDI.L",   "ASML": "ASML.AS",  "ADIDAS": "ADS.DE",
        "SAP": "SAP.DE",     "LVMH": "MC.PA",     "SIEMENS": "SIE.DE",
        "NESTLE": "NESN.SW", "ROCHE": "ROG.SW",   "SHELL": "SHEL.L",
        "VOLKSWAGEN": "VOW3.DE", "BMW": "BMW.DE",
    }
    t = ticker_input.upper().strip()
    if t in dicc:
        return dicc[t]
    # Si ya trae sufijo de mercado lo devuelve tal cual
    if "." in t:
        return t
    # Cripto con guion escrito manualmente
    if "-USD" in t or "-EUR" in t:
        return t
    # Empresas mexicanas con diagonal
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
    puntos = 0
    razones = []
    alertas = []

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

    bb_up, bb_mid, bb_low = calcular_bb(df['Close'])
    if precio_actual < bb_low.iloc[-1]:
        puntos += 2
        razones.append(f"✅ Precio bajo Banda Bollinger inferior — zona de rebote potencial")
    elif precio_actual > bb_up.iloc[-1]:
        puntos -= 2
        alertas.append(f"🔴 Precio sobre Banda Bollinger superior — sobreextendido")

    es_cripto = any(c in categoria for c in ["Cripto", "Startup"])
    pe_ratio = None
    if not es_cripto and info:
        try:
            pe_ratio = info.get('trailingPE', None)
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

    # ── ESCUDO DE VOLUMEN ────────────────────────
    vol_avg = df['Volume'].rolling(20).mean().iloc[-1]
    vol_hoy = df['Volume'].iloc[-1]

    if vol_hoy > vol_avg * 1.8 and df['Close'].iloc[-1] < df['Close'].iloc[-2]:
        puntos -= 3
        alertas.append("🚨 VOLUMEN DE VENTA EXTREMO — El piso actual no es confiable. Espera a que los vendedores se agoten.")
    elif vol_hoy > vol_avg * 1.5 and df['Close'].iloc[-1] < df['Close'].iloc[-2]:
        puntos -= 1
        alertas.append("⚠️ Volumen alto con precio cayendo — vendedores activos.")
    elif vol_hoy > vol_avg * 1.5 and df['Close'].iloc[-1] > df['Close'].iloc[-2]:
        puntos += 2
        razones.append("✅ Rebote con volumen — El piso está aguantando. Señal de compra más confiable.")
    elif vol_hoy > vol_avg * 1.0 and df['Close'].iloc[-1] > df['Close'].iloc[-2]:
        puntos += 1
        razones.append("✅ Volumen normal con precio subiendo — compradores activos.")

    if puntos >= 6:
        color = "verde"; emoji = "🟢"; decision = "INYECTAR CAPITAL"
        descripcion = "Múltiples señales técnicas y fundamentales positivas alineadas. Es momento de considerar una entrada."
    elif puntos >= 2:
        color = "azul"; emoji = "🔵"; decision = "NEUTRAL — ESPERAR"
        descripcion = "Señales mixtas sin dirección clara. Observa más antes de comprometer capital."
    elif puntos >= -2:
        color = "amarillo"; emoji = "🟡"; decision = "PUEDE SEGUIR CAYENDO"
        descripcion = "Señales con sesgo bajista. El precio podría continuar corrigiendo. Paciencia."
    else:
        color = "rojo"; emoji = "🔴"; decision = "NO COMPRAR AHORA"
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
    if cant_actual <= 0 or inv_total_orig <= 0:
        return None

    precio_promedio = inv_total_orig / cant_actual
    perdida_actual = (precio_mercado - precio_promedio) * cant_actual
    pct_perdida = ((precio_mercado / precio_promedio) - 1) * 100

    narrativa = narrativas[cat_sel]
    meta_pct = narrativa["meta_pct"]

    distancia_piso = ((precio_mercado - piso_m) / precio_mercado) * 100
    stop_loss_sugerido = piso_m * 0.97

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
# MOTOR PRO VITERBI (simplificado sin HMM externo)
# ─────────────────────────────────────────────
def motor_pro_viterbi(df, rsi_actual, score_semaforo):
    caida_reciente = (df["Close"].iloc[-1] / df["High"].max() - 1) * 100
    vol_avg = df["Volume"].rolling(20).mean().iloc[-1]
    volumen_stop = df["Volume"].iloc[-1] > vol_avg * 1.5

    estado = "LATERAL"
    if score_semaforo >= 6:
        estado = "ALCISTA"
    elif score_semaforo <= -2:
        estado = "BAJISTA"

    rebote_confirmado = (
        caida_reciente < -3.0
        and volumen_stop
        and df["Close"].iloc[-1] > df["Open"].iloc[-1]
    )
    return estado, rebote_confirmado, caida_reciente

# ─────────────────────────────────────────────
# CALCULADOR DE LIQUIDACIÓN REAL (GBM + ISR MX)
# ─────────────────────────────────────────────
def calcular_efectivo_real(precio_venta, precio_compra, titulos):
    inversion     = precio_compra * titulos
    venta_bruta   = precio_venta  * titulos
    ganancia_bruta = venta_bruta - inversion
    comision_gbm  = venta_bruta * 0.0025 * 1.16          # 0.25% + IVA 16%
    impuesto_isr  = max(0, (ganancia_bruta - comision_gbm) * 0.10)  # 10% ISR
    efectivo_limpio = venta_bruta - comision_gbm - impuesto_isr
    return efectivo_limpio, ganancia_bruta, comision_gbm, impuesto_isr

# ─────────────────────────────────────────────
# BOT DE ESTRATEGIA — VEREDICTO MAESTRO
# ─────────────────────────────────────────────
def bot_sentencia_lino(es_portafolio, estado_pro, rebote, rendimiento, ma200, precio_actual, rsi):
    """Genera el mensaje de voz/texto del Bot y el HTML del widget con bocina."""
    if es_portafolio:
        if rendimiento < -10:
            if rebote:
                msg = (f"Ejecuta Rescate. La caída fue dura pero el volumen confirma rebote. "
                       f"No esperes más, baja tu promedio ahora.")
                emoji = "🔥"
                color = "#2ea043"
            elif ma200 and precio_actual < ma200:
                msg = ("Alto. Estás en zona de pérdida y bajo la MA200. "
                       "No metas más dinero. Es una trampa. Espera soporte real.")
                emoji = "🛑"
                color = "#f85149"
            else:
                msg = ("Paciencia. El mercado está sangrando. "
                       "Mantén disciplina. No operes por emoción.")
                emoji = "⏳"
                color = "#d29922"
        elif rendimiento > 5:
            msg = ("Momento de cobrar. Vas en verde. "
                   "Considera tomar el cincuenta por ciento de ganancias para reinvertir en oportunidades de piso.")
            emoji = "💰"
            color = "#2ea043"
        else:
            msg = ("Posición estable. Monitorea el soporte mensual y espera confirmación antes de mover capital.")
            emoji = "📡"
            color = "#58a6ff"
    else:
        if estado_pro == "ALCISTA" and rebote:
            msg = ("Entrada de élite detectada. Confirmación de giro alcista. Alta probabilidad. Considera entrar ahora.")
            emoji = "🎯"
            color = "#2ea043"
        elif estado_pro == "BAJISTA":
            msg = ("Motor detecta debilidad estructural. Aunque veas señales verdes, espera mejor confirmación.")
            emoji = "⚠️"
            color = "#d29922"
        else:
            msg = ("Escaneando mercado. No hay señales de alta probabilidad. Un ganador sabe cuándo no jugar.")
            emoji = "📡"
            color = "#58a6ff"

    return msg, emoji, color

def render_bot_voz(msg, emoji, color, ticker):
    """Renderiza el widget del bot con botón de bocina y Web Speech API."""
    msg_js = msg.replace("'", " ").replace('"', ' ').replace("\n", " ")
    components.html(f"""
    <div style="background:linear-gradient(135deg,#161b22,#1c2128); border:2px solid {color};
         border-radius:16px; padding:20px 24px; margin:12px 0; display:flex;
         align-items:flex-start; gap:16px;">
        <div style="font-size:2.2rem; line-height:1;">{emoji}</div>
        <div style="flex:1;">
            <div style="color:{color}; font-weight:700; font-size:0.85rem; margin-bottom:4px;">
                🤖 VEREDICTO MAESTRO AI.lino · {ticker}
            </div>
            <div style="color:#e6edf3; font-size:1rem; line-height:1.6;" id="bot_msg_{ticker.replace('.','_')}">
                {msg}
            </div>
        </div>
        <button onclick="hablarBot()" title="Escuchar veredicto"
            style="background:{color}; border:none; border-radius:50%; width:48px; height:48px;
            font-size:1.4rem; cursor:pointer; flex-shrink:0; box-shadow:0 0 16px {color}66;">
            🔊
        </button>
    </div>
    <script>
    function hablarBot() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance('{msg_js}');
            u.lang = 'es-MX';
            u.rate = 0.95;
            u.pitch = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var esp = voices.find(v => v.lang && v.lang.startsWith('es'));
            if (esp) u.voice = esp;
            window.speechSynthesis.speak(u);
        }} else {{
            alert('Tu navegador no soporta síntesis de voz.');
        }}
    }}
    // Pre-cargar voces
    window.speechSynthesis.getVoices();
    </script>
    """, height=140)

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
# ── SIDEBAR ─────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 AI.lino")
    st.caption("Motor de Inversión Inteligente")
    st.markdown("---")

    # ── ANÁLISIS IA EN SIDEBAR ────────────────────
    st.markdown("### 🤖 Análisis IA Profundo")
    st.caption("Técnico + Fundamental + Noticias + Recomendación")

    ticker_ia = st.text_input("Símbolo a analizar:", value="TSLA",
                               key="sidebar_ticker_ia",
                               placeholder="TSLA, GMEXICOB.MX, MNDI.L...")

    if st.button("🔍 Generar Análisis Completo", use_container_width=True, key="btn_analisis_ia"):
        st.session_state["sidebar_analisis_solicitado"] = True
        st.session_state["sidebar_ticker_analizado"] = ticker_ia.upper().strip()

    if st.session_state.get("sidebar_analisis_solicitado") and st.session_state.get("sidebar_ticker_analizado"):
        t_ia = st.session_state["sidebar_ticker_analizado"]
        with st.spinner(f"Analizando {t_ia}..."):
            try:
                import yfinance as _yf, numpy as _np, json as _json, urllib.request as _ur

                _stock = _yf.Ticker(limpiar_ticker(t_ia))
                _df    = _stock.history(period="1y")
                _info  = {}
                try: _info = _stock.info
                except: pass

                if not _df.empty:
                    _pc    = float(_df['Close'].iloc[-1])
                    _ma50  = float(_df['Close'].rolling(50).mean().iloc[-1])
                    _ma200 = float(_df['Close'].rolling(200).mean().iloc[-1]) if len(_df) >= 200 else None
                    _techo = float(_df['High'].max())
                    _piso  = float(_df['Low'].min())
                    _rsi_d = _df['Close'].diff()
                    _g     = _rsi_d.clip(lower=0).rolling(14).mean()
                    _l     = (-_rsi_d.clip(upper=0)).rolling(14).mean()
                    _rsi   = float(100 - 100/(1 + _g/_l.replace(0,_np.nan))).iloc[-1] if not _l.empty else 50
                    _vol_r = float(_df['Volume'].iloc[-1] / _df['Volume'].rolling(20).mean().iloc[-1])
                    _macd  = float(_df['Close'].ewm(span=12,adjust=False).mean().iloc[-1] -
                                   _df['Close'].ewm(span=26,adjust=False).mean().iloc[-1])
                    _pe    = _info.get('trailingPE')
                    _name  = _info.get('longName', t_ia)
                    _sect  = _info.get('sector','N/D')
                    _pais  = _info.get('country','N/D')
                    _52wH  = _info.get('fiftyTwoWeekHigh', _techo)
                    _52wL  = _info.get('fiftyTwoWeekLow', _piso)
                    _mktcap = _info.get('marketCap')
                    _div   = _info.get('dividendYield')
                    _beta  = _info.get('beta')
                    _rev_g = _info.get('revenueGrowth')
                    _margin = _info.get('profitMargins')
                    _deuda = _info.get('debtToEquity')

                    _ma200_str = str(round(_ma200,2)) if _ma200 else "N/D"
                    _ma200_pos = "SOBRE" if _ma200 and _pc > _ma200 else ("BAJO" if _ma200 else "SIN DATO")
                    _pe_str    = f"{_pe:.1f}" if _pe else "N/D"
                    _margin_str = f"{_margin*100:.1f}%" if _margin else "N/D"
                    _rev_str   = f"{_rev_g*100:.1f}%" if _rev_g else "N/D"
                    _deuda_str = f"{_deuda:.0f}%" if _deuda else "N/D"
                    _mktcap_str = f"${_mktcap/1e9:.1f}B" if _mktcap else "N/D"
                    _div_str   = f"{_div*100:.2f}%" if _div else "N/D"
                    _tend_str  = "alcista" if _pc > _ma50 else "bajista"
                    _caida_str = f"{((_pc/_52wH)-1)*100:.1f}%"
                    _rebote_str = f"{((_pc/_52wL)-1)*100:.1f}%"
                    _macd_dir  = "positivo" if _macd > 0 else "negativo"
                    _beta_str  = str(round(_beta,2)) if _beta else "N/D"
                    _vol_str   = f"{_vol_r:.2f}x"

                    prompt_deep = (
                        "Eres el mejor analista financiero del mundo, especializado en mercados de Mexico, EE.UU. y Europa. "
                        "Tu analisis es PROFUNDO, HUMANO y ACCIONABLE. Hablas directo, con criterio propio. "
                        "NO uses frases genericas. Cada parrafo debe aportar valor real al inversor. "
                        "Busca patrones, riesgos ocultos y oportunidades reales en los datos. "
                        f"=== DATOS COMPLETOS DE {_name} ({t_ia}) === "
                        f"Precio: ${_pc:,.2f} | Sector: {_sect} | Pais: {_pais} | "
                        f"Tendencia vs MA50: {_tend_str} | MA50: ${_ma50:,.2f} | MA200: {_ma200_str} ({_ma200_pos}) | "
                        f"RSI: {_rsi:.1f} | MACD: {_macd_dir} ({_macd:,.2f}) | "
                        f"Volumen relativo: {_vol_str} | Beta: {_beta_str} | "
                        f"Maximo 52s: ${_52wH:,.2f} | Minimo 52s: ${_52wL:,.2f} | "
                        f"Caida desde maximo: {_caida_str} | Rebote desde minimo: {_rebote_str} | "
                        f"P/E: {_pe_str} | Margen neto: {_margin_str} | "
                        f"Crecimiento ingresos: {_rev_str} | Deuda/Capital: {_deuda_str} | "
                        f"Cap. mercado: {_mktcap_str} | Dividendo: {_div_str}. "
                        "Escribe el analisis en ESPANOL con estas 5 secciones (sin asteriscos ni markdown): "
                        "1. PANORAMA ACTUAL: Que esta pasando HOY. Contexto del mercado y del sector. Por que esta donde esta. Especifico con numeros. "
                        "2. RADIOGRAFIA TECNICA: Interpreta RSI, MACD, MA50, MA200 y volumen como medico leyendo resultados. Di que senales son confiables y cuales son trampas. Identifica divergencias. "
                        "3. FUNDAMENTOS Y SALUD FINANCIERA: Analiza P/E, margen, crecimiento, deuda y dividendo. Compara con lo normal del sector. Di si la empresa es solida o tiene problemas ocultos. "
                        "4. RIESGOS REALES: Los 3 riesgos mas importantes ahora mismo. Cuanto puede bajar en el peor escenario. Que nivel romper seria peligro real. "
                        "5. VEREDICTO Y PLAN DE ACCION: Precio de entrada ideal, stop loss logico, objetivo con plazo. Una frase final memorable. "
                        "Maximo 500 palabras. Directo, sin relleno."
                    )

                    api_key = st.secrets.get("anthropic", {}).get("api_key", "")
                    if api_key:
                        payload = _json.dumps({
                            "model": "claude-sonnet-4-20250514",
                            "max_tokens": 1200,
                            "messages": [{"role": "user", "content": prompt_deep}]
                        }).encode()
                        req = _ur.Request(
                            "https://api.anthropic.com/v1/messages", data=payload,
                            headers={"Content-Type": "application/json",
                                     "x-api-key": api_key,
                                     "anthropic-version": "2023-06-01"}, method="POST"
                        )
                        with _ur.urlopen(req, timeout=30) as resp:
                            analisis_ia = _json.loads(resp.read())["content"][0]["text"]
                        st.session_state["sidebar_resultado_ia"] = analisis_ia
                        st.session_state["sidebar_ticker_resultado"] = t_ia
                    else:
                        st.session_state["sidebar_resultado_ia"] = (
                            "Configura tu API key de Anthropic en Streamlit Secrets para activar la IA real. "
                            f"Resumen basico de {_name}: "
                            f"Precio ${_pc:,.2f} | RSI {_rsi:.1f} | Tendencia {_tend_str} vs MA50. "
                            f"{'Sobre MA200 - estructura de largo plazo positiva.' if _ma200 and _pc > _ma200 else 'Bajo MA200 - precaucion en largo plazo.'}"
                        )
                        st.session_state["sidebar_ticker_resultado"] = t_ia
                else:
                    st.session_state["sidebar_resultado_ia"] = f"No se encontraron datos para {t_ia}. Verifica el simbolo."
                    st.session_state["sidebar_ticker_resultado"] = t_ia

            except Exception as _e:
                st.session_state["sidebar_resultado_ia"] = f"Error al analizar: {_e}"
                st.session_state["sidebar_ticker_resultado"] = t_ia

    # Mostrar resultado en expander
    if st.session_state.get("sidebar_resultado_ia"):
        t_res = st.session_state.get("sidebar_ticker_resultado", "")
        with st.expander(f"📊 Análisis IA: {t_res}", expanded=True):
            resultado_txt = st.session_state["sidebar_resultado_ia"]
            st.markdown(f"""
            <div style="font-size:0.82rem; line-height:1.7; color:#e6edf3;
                 white-space:pre-line;">{resultado_txt}</div>
            """, unsafe_allow_html=True)

            # Bocina
            voz_safe = resultado_txt.replace("'", " ").replace('"', " ").replace("$", " dolares ").replace("\n", ". ")[:2000]
            components.html(f"""
            <button onclick="hablarIA()" style="background:#1c2128; border:1px solid #58a6ff;
                border-radius:6px; padding:6px 14px; color:#58a6ff; font-size:0.8rem;
                cursor:pointer; margin-top:8px; width:100%;">
                🔊 Escuchar análisis
            </button>
            <script>
            function hablarIA() {{
                if (!('speechSynthesis' in window)) return;
                window.speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance(`{voz_safe}`);
                u.lang='es-MX'; u.rate=0.92; u.pitch=1.0;
                function sv() {{
                    var vs=window.speechSynthesis.getVoices();
                    var e=vs.find(function(v){{return v.lang&&v.lang.startsWith('es');}});
                    if(e) u.voice=e;
                    window.speechSynthesis.speak(u);
                }}
                if(window.speechSynthesis.getVoices().length>0){{sv();}}
                else{{window.speechSynthesis.onvoiceschanged=sv;}}
            }}
            window.speechSynthesis.getVoices();
            </script>
            """, height=50)

            if st.button("🗑️ Limpiar análisis", key="limpiar_ia_sidebar"):
                st.session_state["sidebar_resultado_ia"] = None
                st.session_state["sidebar_analisis_solicitado"] = False
                st.rerun()

    st.markdown("---")
    st.markdown("### 🚀 Herramientas de Élite")
    st.link_button("Ir a AI.Lino PRO (Viterbi)", "https://ailinopro-maquina-dinero-lino.streamlit.app/",
                   use_container_width=True)
    st.caption("Usa el Motor Pro para confirmar señales de entrada y salida con precisión HMM.")
    st.markdown("---")
    st.link_button("🎁 Apoyar el proyecto", "https://buymeacoffee.com/Hugo.lino", use_container_width=True)

# ── HEADER ───────────────────────────────────────
col_h1, col_h2 = st.columns([8, 2])
with col_h1:
    st.title("🧠 AI.lino")
    st.markdown("### Simulador de Mercado · Análisis VIP · Comunidad de Estrategias")
with col_h2:
    # Botón salir solo visible si está autenticado (Modo Portafolio)
    if st.session_state.get("autenticado"):
        nombre_usr = st.session_state.get("usuario_nombre", "")
        st.write("<br>", unsafe_allow_html=True)
        st.caption(f"🔐 Sesión VIP: {nombre_usr}")
        if st.button("🔒 Salir", use_container_width=True):
            st.session_state["autenticado"] = False
            st.rerun()

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

    # ── LOGIN solo para Modo Portafolio (antes de ejecutar) ──────
    if "Portafolio" in modo and not st.session_state.get("autenticado"):
        pantalla_login()
        st.stop()

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

                # ── Datos base ───────────────────────────────
                precio_actual = df_1y['Close'].iloc[-1]
                techo_y       = df_1y['High'].max()
                piso_anual    = df_1y['Low'].min()

                # ── PISO MENSUAL: Low del mes calendario anterior ──
                hoy = pd.Timestamp.now(tz=df_1y.index.tz)
                mes_ant  = hoy.month - 1 if hoy.month > 1 else 12
                anio_ant = hoy.year if hoy.month > 1 else hoy.year - 1
                hist_mes_ant = df_1y[
                    (df_1y.index.month == mes_ant) & (df_1y.index.year == anio_ant)
                ]
                piso_m = float(hist_mes_ant['Low'].min()) if not hist_mes_ant.empty else float(df_1y.tail(22)['Low'].min())

                # ── EMA Mensual: EMA20 sobre los últimos ~20 días hábiles ──
                ema_mensual = float(df_1y['Close'].ewm(span=20, adjust=False).mean().iloc[-1])

                # ── Info fundamental ─────────────────────────
                try:
                    info = stock.info
                    nombre_empresa = info.get('longName', ticker_limpio)
                    sector = info.get('sector', 'N/A')
                    pais   = info.get('country', 'N/A')
                except:
                    info = {}
                    nombre_empresa = ticker_limpio
                    sector = 'N/A'
                    pais   = 'N/A'

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

                # ── MOTOR PRO + BOT DE VOZ ────────────────────
                estado_pro, rebote_pro, caida_pro = motor_pro_viterbi(
                    df_1y, analisis["rsi"], analisis["puntos"]
                )
                es_portafolio = "Portafolio" in modo
                rendimiento_bot = ((precio_actual / (total_inv / cant) - 1) * 100
                                   if es_portafolio and cant > 0 and total_inv > 0
                                   else 0)
                msg_bot, emoji_bot, color_bot = bot_sentencia_lino(
                    es_portafolio, estado_pro, rebote_pro,
                    rendimiento_bot, analisis["ma200"], precio_actual, analisis["rsi"]
                )
                render_bot_voz(msg_bot, emoji_bot, color_bot, ticker_limpio)

                col_r, col_a = st.columns(2)
                with col_r:
                    st.markdown("#### ✅ Señales Positivas")
                    for r in (analisis['razones'] or ["- Sin señales positivas detectadas"]):
                        st.markdown(f"- {r}")
                with col_a:
                    st.markdown("#### ⚠️ Alertas y Riesgos")
                    for a in (analisis['alertas'] or ["- Sin alertas detectadas"]):
                        st.markdown(f"- {a}")

                st.markdown("---")

                # ─────────────────────────────────────────────
                # PANEL ANALÍTICO — con Piso Mensual y EMA Mensual
                # ─────────────────────────────────────────────
                st.markdown("## 📐 Panel Analítico")

                i1, i2, i3, i4, i5 = st.columns(5)
                i1.metric("💲 Precio Actual",  f"${precio_actual:,.2f}")
                i2.metric("📊 RSI (14D)",       f"{analisis['rsi']:.1f}",
                          delta="Sobrevendido" if analisis['rsi'] < 35 else ("Sobrecomprado" if analisis['rsi'] > 65 else "Neutral"))
                i3.metric("📈 MA50",            f"${analisis['ma50']:,.2f}",
                          delta=f"{((precio_actual / analisis['ma50']) - 1) * 100:.1f}% vs precio")
                i4.metric("🔺 Techo Anual",    f"${techo_y:,.2f}")
                i5.metric("🔻 Piso Anual",     f"${piso_anual:,.2f}")

                # ── FILA 2: Piso Mensual + EMA Mensual + BB ──────── NUEVO
                p1, p2, p3, p4, p5 = st.columns(5)
                p1.metric("📅 Piso Mensual",   f"${piso_m:,.2f}",
                          delta=f"{((precio_actual / piso_m) - 1) * 100:.1f}% vs precio")
                p2.metric("〰️ EMA Mensual (20D)", f"${ema_mensual:,.2f}",
                          delta=f"{((precio_actual / ema_mensual) - 1) * 100:.1f}% vs precio")
                if analisis['ma200'] is not None:
                    p3.metric("📉 MA200",       f"${analisis['ma200']:,.2f}",
                              delta=f"{((precio_actual / analisis['ma200']) - 1) * 100:.1f}% vs precio")
                else:
                    p3.metric("📉 MA200",       "N/D", delta="Historial insuficiente")
                if analisis['pe_ratio']:
                    p4.metric("📋 P/E Ratio",   f"{analisis['pe_ratio']:.1f}")
                    p5.metric("📊 BB Superior",  f"${analisis['bb_up']:,.2f}")
                else:
                    p4.metric("📊 BB Superior",  f"${analisis['bb_up']:,.2f}")
                    p5.metric("📊 BB Inferior",  f"${analisis['bb_low']:,.2f}")

                st.markdown("---")

                # ─────────────────────────────
                # MODO EXPLORADOR
                # ─────────────────────────────
                if "Explorador" in modo:
                    st.markdown(f"## 🔍 Tablero AI.lino: {nombre_empresa}")
                    acciones_posibles = inversion_sim / precio_actual
                    st.info(
                        f"💼 Con **${inversion_sim:,.2f}** puedes comprar "
                        f"**{acciones_posibles:.4f}** títulos al precio actual de **${precio_actual:,.2f}**"
                    )
                    st.markdown("#### 📈 Histórico 1 Año")
                    st.line_chart(df_1y['Close'])
                    if not df_1m.empty:
                        st.markdown("#### 📡 Radar Último Mes (1H)")
                        st.line_chart(df_1m['Close'])

                # ─────────────────────────────
                # MODO PORTAFOLIO — Suite VIP
                # ─────────────────────────────
                else:
                    precio_promedio  = total_inv / cant if cant > 0 else 0
                    valor_actual     = precio_actual * cant
                    ganancia_perdida = valor_actual - total_inv
                    rendimiento      = (ganancia_perdida / total_inv * 100) if total_inv > 0 else 0

                    st.markdown(f"## 💎 Suite VIP AI.lino: {nombre_empresa}")

                    # ── Fila principal de portafolio ──────────────────
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Tu Promedio",    f"${precio_promedio:,.2f}")
                    m2.metric("Precio Mercado", f"${precio_actual:,.2f}",
                              delta=f"{((precio_actual / precio_promedio) - 1) * 100:.1f}%" if precio_promedio > 0 else None)
                    m3.metric("Rendimiento",    f"{rendimiento:.2f}%")
                    m4.metric("Valor Hoy",      f"${valor_actual:,.2f}")

                    # ── NUEVA FILA: Piso Mensual + EMA Mensual ──────── NUEVO
                    v1, v2, v3 = st.columns(3)
                    v1.metric("📅 Piso Mensual",      f"${piso_m:,.2f}",
                              delta=f"{((precio_actual / piso_m) - 1) * 100:.1f}% vs precio actual")
                    v2.metric("〰️ EMA Mensual (20D)", f"${ema_mensual:,.2f}",
                              delta=f"{((precio_actual / ema_mensual) - 1) * 100:.1f}% vs precio actual")
                    if analisis['ma200'] is not None:
                        v3.metric("📉 MA200 (Anual)",  f"${analisis['ma200']:,.2f}",
                                  delta=f"{((precio_actual / analisis['ma200']) - 1) * 100:.1f}% vs precio actual")
                    else:
                        v3.metric("📉 MA200 (Anual)",  "N/D")

                    # ── TradingView ──────────────────────────────────
                    # Construir símbolo correcto para TradingView
                    if ticker_limpio.endswith(".MX"):
                        base = ticker_limpio.replace(".MX", "")
                        # Acciones con serie: GMEXICOB -> GMEXICO/B, AMXL -> AMX/L, etc.
                        series_map = {
                            "GMEXICOB":  "GMEXICO%2FB",
                            "AMXL":      "AMX%2FL",
                            "BIMBOA":    "BIMBO%2FA",
                            "FEMSAUBD":  "FEMSA%2FUBD",
                            "CEMEXCPO":  "CEMEX%2FCPO",
                            "GFNORTEO":  "GFNORTE%2FO",
                            "WALMEX":    "WALMEX",
                            "NAFTRAC":   "NAFTRAC",
                            "PE&OLES":   "PE%26OLES",
                            "PEOLES":    "PE%26OLES",
                            "ALSEA":     "ALSEA",
                            "LIVEPOLC1": "LIVEPOL%2FC-1",
                            "GCARSOA1":  "GCARSO%2FA1",
                            "KIMBERA":   "KIMBER%2FA",
                            "TLEVICPO":  "TLEVISA%2FCPO",
                            "GRUMAB":    "GRUMA%2FB",
                            "PINFRA":    "PINFRA",
                            "OMAB":      "OMA%2FB",
                        }
                        # URL-encode el símbolo para el iframe
                        base_tv = series_map.get(base, base.replace("&", "%26").replace("/", "%2F"))
                        tv_symbol = f"BMV:{base_tv}"
                    elif ticker_limpio.endswith(".L"):
                        base = ticker_limpio.replace(".L", "")
                        tv_symbol = f"LSE:{base}"
                    elif ticker_limpio.endswith(".DE"):
                        base = ticker_limpio.replace(".DE", "")
                        tv_symbol = f"XETR:{base}"
                    elif ticker_limpio.endswith(".AS"):
                        base = ticker_limpio.replace(".AS", "")
                        tv_symbol = f"EURONEXT:{base}"
                    elif ticker_limpio.endswith(".PA"):
                        base = ticker_limpio.replace(".PA", "")
                        tv_symbol = f"EURONEXT:{base}"
                    elif "-USD" in ticker_limpio or "-EUR" in ticker_limpio:
                        tv_symbol = ticker_limpio.replace("-", "")
                    else:
                        tv_symbol = ticker_limpio  # NASDAQ/NYSE ya funcionan directo
                    # TradingView iframe — funciona con TODOS los mercados
                    tv_widget = f"""
                    <div style="height:430px; width:100%;">
                    <iframe
                        src="https://www.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=D&theme=dark&style=1&locale=es&toolbar_bg=%23161b22&hide_side_toolbar=0&allow_symbol_change=1&saveimage=0&calendar=0&hotlist=0&details=1&news=0&studies=%5B%5D&show_popup_button=1&popup_width=1000&popup_height=650"
                        style="width:100%; height:430px; border:none; border-radius:12px;"
                        allowtransparency="true"
                        scrolling="no"
                        allowfullscreen="">
                    </iframe>
                    </div>"""
                    components.html(tv_widget, height=440)

                    st.markdown("---")

                    # ═══════════════════════════════════════════════════
                    # CENTRO DE COMANDO — RESCATE INTELIGENTE AI.lino
                    # Fusión de: Mapa de Escalones + Motor de Rescate
                    # ═══════════════════════════════════════════════════
                    ma200_val    = analisis.get("ma200")
                    narrativa_sc = narrativas[categoria]
                    piso_roto    = precio_actual < piso_m

                    st.markdown("## 🎯 Centro de Comando — Rescate Inteligente AI.lino")

                    # ── Resumen de situación actual ───────────────────
                    if rendimiento < 0:
                        col_sit1, col_sit2, col_sit3 = st.columns(3)
                        col_sit1.metric("📉 Pérdida actual",
                                        f"${abs(valor_actual - total_inv):,.2f}",
                                        delta=f"{rendimiento:.1f}%")
                        col_sit2.metric("💰 Tu promedio de compra", f"${precio_promedio:,.2f}")
                        col_sit3.metric("📌 Precio actual",
                                        f"${precio_actual:,.2f}",
                                        delta=f"{((precio_actual/precio_promedio)-1)*100:.1f}%")

                        # ── Escudo de contexto ─────────────────────────
                        if piso_roto:
                            st.error(f"🚨 **PISO MENSUAL ROTO** — El precio **${precio_actual:,.2f}** ya está por debajo del piso de **${piso_m:,.2f}**. Operar ahora es de alto riesgo. Usa los escalones de abajo como guía.")
                        else:
                            dist_piso_pct = ((precio_actual - piso_m) / precio_actual) * 100
                            color_piso = "🟢" if dist_piso_pct > 5 else "🟡"
                            st.info(f"{color_piso} **Piso mensual ${piso_m:,.2f} aún se mantiene** · Distancia: {dist_piso_pct:.1f}% · Stop Loss sugerido: **${piso_m * 0.97:,.2f}** (3% bajo el piso)")

                        # Filosofía Lynch
                        st.markdown(f"""
                        <div class="card">
                            <b>📖 Filosofía activa: {narrativa_sc['estilo']}</b><br>
                            <span style="color:#8b949e;">{narrativa_sc['mensaje']}</span>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("---")

                        # ── Escalones integrados con simulación ────────
                        st.markdown("### 🪜 Mapa de Escalones → Simulación por Nivel")
                        st.caption(f"Cada escalón = mínimo real de un mes · Objetivo de salida: **{narrativa_sc['nombre_meta']}** ({narrativa_sc['meta_pct']*100-100:.0f}%)")

                        escalones = calcular_escalones(df_1y, precio_actual, piso_m, piso_anual,
                                                       narrativa_sc, cant if cant > 0 else 1,
                                                       total_inv if total_inv > 0 else precio_actual)

                        if escalones:
                            for esc in escalones:
                                es_trampa = (ma200_val is not None and esc["nuevo_promedio"] > ma200_val)

                                # Colores y estilos según trampa o viable
                                borde_color = "#8b0000" if es_trampa else esc["nivel_color"]
                                bg_gradient = "linear-gradient(135deg,#2d0a0a,#1c1010)" if es_trampa else "#1c2128"

                                # Badge urgencia
                                if "PRECIO EN ZONA" in esc["alerta"]:
                                    urgencia = "🔴 DECIDIR AHORA"
                                    urgencia_bg = "#f85149"
                                elif "CERCA" in esc["alerta"]:
                                    urgencia = "🟡 PREPARAR CAPITAL"
                                    urgencia_bg = "#d29922"
                                else:
                                    urgencia = f"🔵 {esc['dist_pct']:.1f}% de distancia"
                                    urgencia_bg = "#1f3a5c"

                                # Veredicto texto plano (sin HTML anidado)
                                if es_trampa:
                                    veredicto_icono = "⛔"
                                    veredicto_titulo = "NIVEL NO RECOMENDADO — TRAMPA MA200"
                                    veredicto_bg = "#3d0000"
                                    veredicto_borde = "#8b0000"
                                    veredicto_texto = (
                                        f"Tu nuevo promedio ${esc['nuevo_promedio']:,.2f} quedaría "
                                        f"ARRIBA de la MA200 ${ma200_val:,.2f}. "
                                        f"El precio chocará con esa resistencia antes de que puedas salir en tablas. "
                                        f"Espera un escalón más abajo."
                                    )
                                else:
                                    veredicto_icono = "✅"
                                    veredicto_titulo = "NIVEL VIABLE"
                                    veredicto_bg = "#0d2b1a"
                                    veredicto_borde = "#2ea043"
                                    if ma200_val:
                                        veredicto_texto = (
                                            f"Tu nuevo promedio ${esc['nuevo_promedio']:,.2f} quedaría "
                                            f"BAJO la MA200 ${ma200_val:,.2f} — camino libre hacia el objetivo."
                                        )
                                    else:
                                        veredicto_texto = f"Tu nuevo promedio ${esc['nuevo_promedio']:,.2f} — sin resistencia MA200 detectada."

                                reduccion_pct = ((esc['nuevo_promedio'] / precio_promedio) - 1) * 100

                                # Render: cabecera de la tarjeta
                                st.markdown(
                                    f"""<div style="background:{bg_gradient}; border-left:6px solid {borde_color};
                                    border-radius:12px; padding:16px 20px; margin-bottom:4px;">
                                    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:8px;">
                                        <b style="color:{borde_color}; font-size:1rem;">{esc['nivel_nombre']}</b>
                                        <span style="background:{urgencia_bg}; color:white; padding:2px 10px;
                                        border-radius:6px; font-size:0.8rem; font-weight:700;">{urgencia}</span>
                                    </div>
                                    <div style="color:#8b949e; font-size:0.85rem; margin-bottom:10px;">
                                        📍 Soporte: <b style="color:#e6edf3;">${esc['precio']:,.2f}</b>
                                        &nbsp;·&nbsp; Mínimo de <b style="color:#e6edf3;">{esc['nombre_mes']}</b>
                                        &nbsp;·&nbsp; A <b style="color:#e6edf3;">{esc['dist_pct']:.1f}%</b> del precio actual
                                    </div>
                                    <div style="font-size:0.92rem; line-height:2.0; color:#e6edf3;">
                                        💵 Capital a inyectar: <b>${esc['capital_extra']:,.2f}</b>
                                        &nbsp;·&nbsp; Títulos nuevos: <b>{esc['nuevos_titulos']:.4f}</b><br>
                                        📊 Nuevo promedio: <b>${esc['nuevo_promedio']:,.2f}</b>
                                        &nbsp;·&nbsp; Cambio vs hoy: <b>{reduccion_pct:.1f}%</b><br>
                                        🎯 Meta {narrativa_sc['nombre_meta']}: <b>${esc['precio_meta']:,.2f}</b>
                                        &nbsp;→&nbsp; Ganancia estimada: <b>${esc['ganancia_meta']:,.2f}</b>
                                    </div>
                                    </div>""",
                                    unsafe_allow_html=True
                                )
                                # Render: veredicto como bloque separado
                                st.markdown(
                                    f"""<div style="background:{veredicto_bg}; border:1px solid {veredicto_borde};
                                    border-radius:8px; padding:10px 16px; margin-bottom:16px; font-size:0.9rem; color:#e6edf3;">
                                    {veredicto_icono} <b>{veredicto_titulo}:</b> {veredicto_texto}
                                    </div>""",
                                    unsafe_allow_html=True
                                )
                            st.warning("No hay suficiente historial mensual para calcular escalones.")

                        st.markdown("---")
                        st.warning(f"💡 **Consejo Lynch — {narrativa_sc['estilo']}:** {narrativa_sc['consejo']}")

                    elif rendimiento > 0:
                        st.success(f"🎉 **¡En ganancia! +${ganancia_perdida:,.2f} ({rendimiento:.2f}%)**")
                        precio_meta_obj = precio_promedio * narrativa_sc["meta_pct"]
                        if precio_actual >= precio_meta_obj:
                            st.balloons()
                            st.success(f"🏆 **¡Alcanzaste el objetivo {narrativa_sc['nombre_meta']}!** Considera tomar ganancias parciales.")
                        else:
                            falta = precio_meta_obj - precio_actual
                            st.info(
                                f"🎯 Objetivo {narrativa_sc['nombre_meta']}: **${precio_meta_obj:,.2f}** · "
                                f"Faltan **${falta:,.2f}** ({((precio_meta_obj / precio_actual) - 1) * 100:.1f}%)"
                            )

                        # ── CALCULADORA DE LIQUIDACIÓN REAL ──────────
                        st.markdown("---")
                        st.markdown("### 💸 Calculadora de Liquidación Real — GBM México")
                        st.caption("Simula cuánto efectivo limpio recibirías según el precio y los títulos que quieras vender.")
                        calc_col1, calc_col2 = st.columns(2)
                        with calc_col1:
                            precio_venta_sim = st.number_input(
                                "💲 Precio de venta a simular ($):",
                                min_value=0.01,
                                value=float(round(precio_actual, 2)),
                                format="%.2f",
                                key="precio_venta_sim"
                            )
                        with calc_col2:
                            titulos_vender = st.number_input(
                                "📦 Títulos que deseas vender:",
                                min_value=0.0001,
                                max_value=float(cant),
                                value=float(cant),
                                format="%0.4f",
                                key="titulos_vender_sim",
                                help=f"Tienes {cant:.4f} títulos en total"
                            )
                        if precio_venta_sim > 0 and titulos_vender > 0:
                            # Calcular precio promedio ponderado solo de los títulos vendidos
                            precio_compra_sim = total_inv / cant if cant > 0 else 0
                            limpio, g_bruta, com, isr = calcular_efectivo_real(
                                precio_venta_sim, precio_compra_sim, titulos_vender
                            )
                            inversion_parcial = precio_compra_sim * titulos_vender
                            pct_venta = (titulos_vender / cant * 100) if cant > 0 else 0

                            st.caption(f"Vendiendo **{titulos_vender:.4f}** títulos ({pct_venta:.1f}% de tu posición)")
                            liq1, liq2, liq3, liq4 = st.columns(4)
                            liq1.metric("💵 Efectivo Real", f"${limpio:,.2f}",
                                        help="Lo que llega a tu cuenta después de comisión e ISR")
                            liq2.metric("📈 Ganancia Bruta", f"${g_bruta:,.2f}")
                            liq3.metric("🏦 Comisión GBM", f"${com:,.2f}",
                                        help="0.25% + IVA 16% sobre el monto de venta")
                            liq4.metric("🏛️ ISR (10%)", f"${isr:,.2f}",
                                        help="10% sobre ganancia neta")
                            if g_bruta > 0:
                                st.success(f"✅ Ganancia neta real después de impuestos: **${g_bruta - com - isr:,.2f}**")
                                # Mostrar posición restante
                                titulos_restantes = cant - titulos_vender
                                if titulos_restantes > 0:
                                    valor_restante = titulos_restantes * precio_actual
                                    st.info(f"📊 Posición restante: **{titulos_restantes:.4f}** títulos · Valor actual: **${valor_restante:,.2f}**")
                            else:
                                st.warning(f"⚠️ Después de comisiones e ISR aún estarías en pérdida neta en esta venta.")


                # ═══════════════════════════════════════════════
                # REPORTE AI.lino — IA Real + fallback estático
                # ═══════════════════════════════════════════════
                st.markdown("---")
                st.markdown("## 📰 Reporte AI.lino — Análisis Situacional")
                st.caption(f"Generado para {nombre_empresa} · {ticker_limpio} · Sector: {sector}")

                # Datos del reporte
                caida_anual_pct  = ((precio_actual / techo_y) - 1) * 100
                rebote_anual_pct = ((precio_actual / piso_anual) - 1) * 100
                macd_val_r = (df_1y['Close'].ewm(span=12,adjust=False).mean().iloc[-1]
                              - df_1y['Close'].ewm(span=26,adjust=False).mean().iloc[-1])
                vol_ratio  = df_1y['Volume'].iloc[-1] / df_1y['Volume'].rolling(20).mean().iloc[-1]
                tend_r     = "alcista" if precio_actual > analisis['ma50'] else "bajista"
                ma200_pos_r = ("por encima de" if analisis['ma200'] and precio_actual > analisis['ma200']
                               else "por debajo de" if analisis['ma200'] else "sin dato de")
                estado_hmm_r = estado_pro if 'estado_pro' in locals() else "LATERAL"

                # Intentar IA real (Claude API) si hay key configurada
                reporte_txt = None
                try:
                    api_key = st.secrets.get("anthropic", {}).get("api_key", "")
                    if api_key:
                        import urllib.request, json as _json
                        prompt_ia = (
                            f"Eres un analista financiero senior de mercados Mexico, EE.UU. y Europa. "
                            f"Escribe un reporte profesional pero humano sobre {nombre_empresa} ({ticker_limpio}). "
                            f"Tono directo, con criterio propio, sin frases genericas. Especifico con numeros. "
                            f"Datos: precio {precio_actual:.2f}, RSI {analisis['rsi']:.1f}, "
                            f"MA50 {analisis['ma50']:.2f}, MA200 {str(round(analisis['ma200'],2)) if analisis['ma200'] else 'N/D'}, "
                            f"tendencia {tend_r}, piso mensual {piso_m:.2f}, piso anual {piso_anual:.2f}, "
                            f"techo {techo_y:.2f}, distancia al techo {abs(caida_anual_pct):.1f}%, "
                            f"MACD {'positivo' if macd_val_r > 0 else 'negativo'}, volumen {vol_ratio:.2f}x promedio, "
                            f"P/E {analisis['pe_ratio']:.1f if analisis['pe_ratio'] else 'N/D'}, "
                            f"semaforo: {analisis['decision']} score {analisis['puntos']:+d} puntos, "
                            f"estado motor: {estado_hmm_r}, rebote confirmado: {'SI' if rebote_pro else 'NO'}. "
                            f"4 secciones: 1.SITUACION ACTUAL 2.LO QUE DICEN LOS INDICADORES "
                            f"3.EL RIESGO REAL 4.CONCLUSION Y ACCION. Max 350 palabras. Sin markdown."
                        )
                        payload = _json.dumps({
                            "model": "claude-sonnet-4-20250514",
                            "max_tokens": 800,
                            "messages": [{"role": "user", "content": prompt_ia}]
                        }).encode()
                        req = urllib.request.Request(
                            "https://api.anthropic.com/v1/messages", data=payload,
                            headers={"Content-Type": "application/json",
                                     "x-api-key": api_key,
                                     "anthropic-version": "2023-06-01"}, method="POST"
                        )
                        with urllib.request.urlopen(req, timeout=25) as resp:
                            reporte_txt = _json.loads(resp.read())["content"][0]["text"]
                except Exception:
                    reporte_txt = None

                # Fallback: reporte estático si no hay IA
                if not reporte_txt:
                    rsi_desc_r = ("en zona de sobreventa — posible oportunidad" if analisis['rsi'] < 35
                                  else "en sobrecompra — precaución" if analisis['rsi'] > 65
                                  else "en zona neutral")
                    bb_pos_r = ("bajo la banda inferior — zona de rebote potencial"
                                if precio_actual < analisis['bb_low']
                                else "sobre la banda superior — sobreextendido"
                                if precio_actual > analisis['bb_up'] else "dentro de las bandas Bollinger")
                    macd_dir_r = "positivo, confirmando presión compradora" if macd_val_r > 0 else "negativo, sugiriendo presión vendedora"
                    pe_desc_r = (f"P/E de {analisis['pe_ratio']:.1f}x — " +
                                 ("valuación atractiva." if analisis['pe_ratio'] < 15
                                  else "valuación razonable." if analisis['pe_ratio'] < 30
                                  else "valuación elevada.")) if analisis['pe_ratio'] else "P/E no disponible en Yahoo Finance."

                    if analisis['color'] == 'verde':
                        conclusion_r = (f"{nombre_empresa} presenta configuración técnica favorable. "
                                        f"Soporte mensual en ${piso_m:,.2f} y anual en ${piso_anual:,.2f}. "
                                        "Una ruptura sostenida sobre la MA200 " + (f"${analisis['ma200']:,.2f}" if analisis['ma200'] else 'nivel clave') + " confirmaria continuacion alcista.")
                    elif analisis['color'] == 'rojo':
                        conclusion_r = (f"{nombre_empresa} muestra señales de debilidad. "
                                        f"Riesgo de extensión hacia el piso anual ${piso_anual:,.2f}. "
                                        f"No agregar posiciones hasta estabilización sobre MA50 ${analisis['ma50']:,.2f}.")
                    else:
                        conclusion_r = (f"{nombre_empresa} en zona de decisión. "
                                        f"Soporte más cercano: ${piso_m:,.2f} (piso mensual). "
                                        f"Catalizador de entrada: cierre sobre MA50 ${analisis['ma50']:,.2f} con volumen.")

                    reporte_txt = (
                        "SITUACION ACTUAL\n"
                        f"{nombre_empresa} ({ticker_limpio}) cotiza en ${precio_actual:,.2f}, "
                        f"en tendencia {tend_r} de corto plazo, operando {ma200_pos_r} su MA200. "
                        f"Respecto a su rango anual, se encuentra {abs(caida_anual_pct):.1f}% abajo del techo "
                        f"y {rebote_anual_pct:.1f}% arriba del piso.\n\n"
                        "LO QUE DICEN LOS INDICADORES\n"
                        f"RSI en {analisis['rsi']:.1f} - {rsi_desc_r}. "
                        f"Precio {bb_pos_r}. MACD {macd_dir_r}. "
                        f"Volumen reciente: {vol_ratio:.2f}x el promedio de 20 dias. {pe_desc_r}\n\n"
                        "EL RIESGO REAL\n"
                        f"Semaforo AI.lino: {analisis['decision']} (score {analisis['puntos']:+d} pts). "
                        f"Motor Pro clasifica estado como {estado_hmm_r}. "
                        f"{'Rebote confirmado por volumen.' if rebote_pro else 'Sin confirmacion de rebote aun.'} "
                        f"Stop Loss sugerido: ${piso_m * 0.97:,.2f} (3% bajo piso mensual).\n\n"
                        "CONCLUSION Y ACCION\n"
                        f"{conclusion_r}"
                    )

                # Renderizar reporte
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0d1117,#161b22);
                     border:1px solid #30363d; border-radius:16px;
                     padding:28px 32px; line-height:1.9; color:#e6edf3;
                     font-size:1rem; white-space:pre-line;">{reporte_txt}</div>
                """, unsafe_allow_html=True)

                # Bocina — leer reporte completo
                reporte_voz = reporte_txt.replace("'", " ").replace('"', " ").replace("$", " dolares ").replace("\n", ". ")
                reporte_voz_safe = reporte_voz[:1800]
                components.html(f"""
                <div style="text-align:right; margin-top:8px;">
                    <button onclick="leerReporteAI()" title="Escuchar reporte completo"
                        style="background:#161b22; border:1px solid #58a6ff; border-radius:8px;
                        padding:10px 20px; color:#58a6ff; font-size:0.95rem; cursor:pointer;
                        transition:all 0.2s;">
                        🔊 Escuchar reporte completo
                    </button>
                </div>
                <script>
                function leerReporteAI() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('Tu navegador no soporta sintesis de voz.');
                        return;
                    }}
                    window.speechSynthesis.cancel();
                    var texto = `{reporte_voz_safe}`;
                    var u = new SpeechSynthesisUtterance(texto);
                    u.lang = 'es-MX';
                    u.rate = 0.92;
                    u.pitch = 1.0;
                    function setVoice() {{
                        var voices = window.speechSynthesis.getVoices();
                        var esp = voices.find(function(v) {{ return v.lang && v.lang.startsWith('es'); }});
                        if (esp) u.voice = esp;
                        window.speechSynthesis.speak(u);
                    }}
                    if (window.speechSynthesis.getVoices().length > 0) {{
                        setVoice();
                    }} else {{
                        window.speechSynthesis.onvoiceschanged = setVoice;
                    }}
                }}
                </script>
                """, height=65)

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
            autor      = st.text_input("Tu Nombre o Nickname:", placeholder="ej. Lobo de Wall Street")
            activo     = st.text_input("Activo / Símbolo:", placeholder="ej. BTC-USD, GMEXICO, S&P 500").upper()
            cat_comm   = st.selectbox("Categoría:", list(narrativas.keys()))
            estrategia = st.text_area("Tu Estrategia Detallada:", placeholder="ej. Comprar si rompe la resistencia de los $X, buscando el techo en $Y. Stop Loss en $Z.", height=120)
            publicar   = st.form_submit_button("📢 Publicar en Comunidad")
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
                <small>Activo: {estr['activo']} | Categoría: {estr.get('categoria', '—')} | Publicado: {estr['fecha']}</small><br><br>
                {estr['estrategia']}
            </div>
            """, unsafe_allow_html=True)
