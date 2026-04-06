Hugo Hernández <hugo.lino1093@gmail.com>	6 de abril de 2026 a las 10:46 am
Para: Hugo Hernández <Hugo.dary7@gmail.com>
importar streamlit como st
Importar yfinance como yf
importar pandas como pd
import numpy as np
import streamlit.components.v1 as components
importar fecha y hora

# ───────────────────────────── ───────────────
# 1. CONFIGURACIÓN
# ───────────────────────────── ───────────────
st.set_page_config(page_title= "AI.lino", page_icon="🧠", layout="wide")

# ───────────────────────────── ───────────────
# 2. ESTILOS
# ───────────────────────────── ───────────────
st.markdown("""
<style>
@import url(' https://fonts.googleapis. com/css2?family=Space+Grotesk: wght@400;600;700&display=swap' );

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    fondo: gradiente lineal(135 grados, #0d1117 0%, #161b22 50%, #0d1117 100%);
    color: #e6edf3;
}

h1 { color: #58a6ff !important; font-size: 2.8rem !important; font-weight: 700 !important; }
h2, h3 { color: #c9d1d9 !important; font-weight: 600 !important; }

div[data-testid=" stMetricValue"] {
    color: #58a6ff !importante;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

.semaforo-verde {
    fondo: gradiente lineal(135deg, #0d3321, #1a5c3a);
    borde: 2px sólido #2ea043;
    radio de borde: 16px;
    relleno: 24px;
    alineación de texto: centro;
    box-shadow: 0 0 30px rgba(46,160,67,0.3);
}
.semaforo-rojo {
    fondo: gradiente lineal(135deg, #3d0000, #6b1010);
    borde: 2px sólido #f85149;
    radio de borde: 16px;
    relleno: 24px;
    alineación de texto: centro;
    box-shadow: 0 0 30px rgba(248,81,73,0.3);
}
.semaforo-amarillo {
    fondo: gradiente lineal(135deg, #3d2d00, #6b4c00);
    borde: 2px sólido #d29922;
    radio de borde: 16px;
    relleno: 24px;
    alineación de texto: centro;
    box-shadow: 0 0 30px rgba(210,153,34,0.3);
}
.semaforo-azul {
    fondo: gradiente lineal(135deg, #001f3d, #0d2b4e);
    borde: 2px sólido #58a6ff;
    radio de borde: 16px;
    relleno: 24px;
    alineación de texto: centro;
    box-shadow: 0 0 30px rgba(88,166,255,0.3);
}

.tarjeta {
    fondo: #161b22;
    borde: 1px sólido #30363d;
    radio de borde: 12px;
    relleno: 20px;
    margen inferior: 16px;
}

.rescate-card {
    fondo: #1c2128;
    borde izquierdo: 4px sólido #58a6ff;
    radio de borde: 8px;
    relleno: 16px;
    margen: 8px 0;
    interlineado: 1,8;
}

.stButton>botón {
    fondo: gradiente-lineal(135deg, #238636, #2ea043) !importante;
    color: blanco !importante;
    borde: ninguno !importante;
    radio de borde: 8px !importante;
    font-weight: 700 !important;
    font-size: 1rem !important;
    relleno: 12px 24px !importante;
    transición: ¡todos 0.2s!importante;
}
.stButton>botón:hover {
    transformar: translateY(-2px) !importante;
    box-shadow: 0 4px 20px rgba(46,160,67,0.4) !important;
}

.tarjeta-estrategia {
    fondo: #1c2128;
    borde: 1px sólido #30363d;
    radio de borde: 10px;
    relleno: 16px;
    margen inferior: 12px;
}

etiqueta div[data-testid="stSelectbox"],
etiqueta div[data-testid="stTextInput"],
div[data-testid=" stNumberInput"] etiqueta {
    color: #8b949e !importante;
    font-weight: 600 !important;
}

.stAlert { border-radius: 10px !important; }

.escalon-card {
    radio de borde: 12px;
    relleno: 16px 20px;
    margen: 8px 0;
    interlineado: 1,8;
    borde izquierdo: 6px sólido #ccc;
}
.escalon-activo {
    fondo: gradiente lineal(135deg, #1a1f2e, #1c2540);
    color del borde izquierdo: #58a6ff !importante;
    box-shadow: 0 0 20px rgba(88,166,255,0.2);
}
.escalon-pendiente {
    fondo: #1c2128;
    color del borde izquierdo: #30363d !importante;
    opacidad: 0,85;
}
.login-box {
    ancho máximo: 400px;
    margen: 60px automático;
    fondo: #161b22;
    borde: 1px sólido #30363d;
    radio de borde: 16px;
    relleno: 40px;
    box-shadow: 0 0 40px rgba(88,166,255,0.15);
}
</style>
"", unsafe_allow_html=True)

# ───────────────────────────── ───────────────
# 3. SISTEMA DE INICIO DE SESIÓN
# ───────────────────────────── ───────────────
def verificar_login(usuario, contraseña):
    intentar:
        devolver (usuario.strip() == st.secrets["auth"]["username"] y
                contraseña == st.secrets["auth"]["password"] )
    excepto Excepción:
        devolver Falso

def pantalla_login():
    st.markdown("""
    <div style='text-align:center; padding:50px 0 20px 0;'>
        <span style='font-size:3.5rem;'>🧠 </span>
        <h1 style='color:#58a6ff; margin:10px 0;'>AI.lino</h1>
        <p estilo='color:#8b949e; font-size:1.1rem;'>Motor de Inversión — Acceso Privado</p>
    </div>
    "", unsafe_allow_html=True)
    col = st.columns([1, 1.1, 1])[1]
    con col:
        con st.form("login_form"):
            st.markdown("#### 🔐 Iniciar Sesión")
            usuario = st.text_input("Usuario", placeholder="tu usuario")
            contraseña = st.text_input("Contraseña", type="password", placeholder="••••••••")
            entrar = st.form_submit_button("Entrar →", use_container_width=True)
            si entrar:
                if verificar_login(usuario, contraseña):
                    st.session_state["autenticado" ] = True
                    st.session_state["usuario_ nombre"] = st.secrets["auth"].get(" nombre", usuario)
                    st.rerun()
                demás:
                    st.error("❌ Usuario o contraseña incorrectos.")

Si "autenticado" no está en st.session_state:
    st.session_state["autenticado" ] = Falso

# ───────────────────────────── ───────────────
# FUNCIÓN: ESCALONES DE SOPORTE
# ───────────────────────────── ───────────────
def calcular_escalones(df_1y, precio_actual, piso_m, piso_anual, narrativa, cant, total_inv):
    """
    Calcula los mínimos reales de cada mes del año (de más reciente a más antiguo),
    filtra solo los que están DEBAJO del precio actual (pisos ya rotos o en riesgo),
    y los vincula con los 3 niveles de rescate.
    Retorna lista de escalones con su nivel sugerido y estado de alerta.
    """
    hoy = pd.Timestamp.now(tz= df_1y. index.tz )
    escalones_raw = []

    # Recolectar mínimo de cada mes en el historial (hasta 12 meses atrás)
    para i en rango(1, 13):
        mes = (hoy.month - i - 1) % 12 + 1
        anio = hoy.año si hoy.mes - i > 0 else hoy.año - 1
        # ajuste fino de año
        desplazamiento = hoy.mes - i
        Si offset <= 0:
            anio = hoy.año - 1
            mes = 12 + desplazamiento
        demás:
            anio = hoy.año
            mes = desplazamiento

        bloque = df_1y[(df_1y.index.month == mes) & (df_1y.index.year == anio)]
        si no bloque.empty:
            low_mes = float(bloque['Low'].min())
            nombre_m = pd.Timestamp(año=anio, mes=mes, día=1).strftime("%b %Y")
            escalones_raw.append((low_mes, nombre_m))

    # Eliminar duplicados y ordenar de mayor a menor
    vistos = set()
    escalones_uniq = []
    para v, n en sorted(escalones_raw, reverse=True):
        clave = redondear(v, 2)
        Si la clave no está en vistos:
            vistos.add(clave)
            escalones_uniq.append((v, n))

    # Solo los que están por DEBAJO del precio actual (soporte roto o en riesgo)
    debajo = [(v, n) for v, n in escalones_uniq si v < precio_actual]

    # Agregar piso anual al final si no estás ya
    if piso_anual < precio_actual y no cualquiera(abs(v - piso_anual) < 1.0 for v, _ in debajo):
        debajo.append((piso_anual, "🔻 Piso Anual"))

    # Tomar máximo 4 escalones más relevantes
    debajo = debajo[:4]

    # Vincular cada escala con nivel de rescate
    nivel_etiquetas = [
        ("Nivel 1 — Conservador (25%)", "#2ea043"),
        ("Nivel 2 — Moderado (50%)", "#d29922"),
        ("Nivel 3 — Agresivo (100%)", "#f85149"),
        ("Zona Extrema / Stop Loss", "#8b0000"),
    ]

    precio_promedio = total_inv / no puedo si no puedo > 0 sino 0
    meta_pct = narrativa["meta_pct"]

    resultado = []
    para idx, (precio_esc, nombre_m) en enumerar(debajo):
        nivel_nombre, nivel_color = nivel_labels[idx] if idx < len(nivel_labels) else nivel_labels[-1]

        # Calcular simulación si se entra en este escalón
        pct_rescate = [0,25, 0,50, 1,00, 1,00][idx]
        capital_extra = total_inv * pct_rescate
        nuevos_titulos = capital_extra / precio_esc si precio_esc > 0 sino 0
        titulos_finales = cant + nuevos_titulos
        inv_final = total_inv + capital_extra
        nuevo_promedio = inv_final / titulos_finales si titulos_finales > 0 sino 0
        precio_meta = nuevo_promedio * meta_pct
        ganancia_meta = (precio_meta - nuevo_promedio) * titulos_finales

        # Estado de alerta
        dist_pct = ((precio_actual - precio_esc) / precio_actual) * 100
        Si dist_pct <= 2:
            alerta = "🔴 PRECIO EN ZONA — ¡Decidir ahora!"
            estado = "activo"
        elif dist_pct <= 6:
            alerta = "🟡 CERCA — Preparar capital"
            estado = "activo"
        demás:
            alerta = f"🔵 A {dist_pct:.1f}% de distancia"
            estado = "pendiente"

        resultado.append({
            "precio": precio_esc,
            "nombre_mes": nombre_m,
            "nivel_nombre": nivel_nombre,
            "nivel_color": nivel_color,
            "alerta": alerta,
            "estado": estado,
            "dist_pct": dist_pct,
            "capital_extra": capital_extra,
            "nuevo_promedio": nuevo_promedio,
            "precio_meta": precio_meta,
            "ganancia_meta": ganancia_meta,
            "nuevos_titulos": nuevos_titulos,
        })

    devolver resultado

# ───────────────────────────── ───────────────
# 4. DICCIONARIO LYNCH
# ───────────────────────────── ───────────────
narrativas = {
    "🔄 Cíclica (Minería, Chips, Autos)": {
        "estilo": "Estrategia de Supervivencia Cíclica",
        "mensaje": "Las empresas cíclicas dependen del ritmo del mercado. Promediar es válido solo si el ciclo no ha terminado.",
        "consejo": "No te enamoras del activo. Busca tu punto de equilibrio y evalúa si el ciclo aún tiene combustible.",
        "meta_pct": 1.15, "nombre_meta": "Objetivo Lynch Cíclico (+15%)"
    },
    "🚀 Startup / Cripto (Crecimiento Alto / Volatilidad)": {
        "estilo": "Ajuste de Exposición Volátil",
        "mensaje": "Volatilidad extrema. Al promediar multiplica el potencial de rebote, pero también el riesgo de caída.",
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
        "mensaje": "Promediar en un ETF es comprar el mercado a descuento. Alimentas tu compuesto interés.",
        "consejo": "El tiempo es tu mejor aliado. Cada peso extra hoy es una bola de nieve más grande mañana.",
        "meta_pct": 1.08, "nombre_meta": "Crecimiento de Índice (+8%)"
    }
}

# ───────────────────────────── ───────────────
# 4. FUNCIONES CORE
# ───────────────────────────── ───────────────
def limpiar_ticker(ticker_input):
    dicc = {
        # México
        "PEÑOLES": "PE& OLES.MX ", "GMEXICO": " GMEXICOB.MX ",
        "FIBRAMQ": " FMTY.MX ", "WALMEX": " WALMEX.MX ",
        "AMXL": " AMXL.MX ", "FEMSAUBD": " FEMSAUBD.MX ",
        "NAFTRAC": " NAFTRAC.MX ",
        # Cripto
        "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD",
        # ETFs
        "S&P 500": "VOO", "SP500": "VOO",
        # Europa nombres comunes
        "MONDI": "MNDI.L", "ASML": " ASML.AS ", "ADIDAS": " ADS.DE ",
        "SAP": " SAP.DE ", "LVMH": " MC.PA ", "SIEMENS": " SIE.DE ",
        "NESTLE": "NESN.SW", "ROCHE": "ROG.SW", "SHELL": "SHEL.L",
        "VOLKSWAGEN": " VOW3.DE ", "BMW": " BMW.DE ",
    }
    t = ticker_input.upper().strip()
    si t en dicc:
        devolver dicc[t]
    # Si ya trae sufijo de mercado lo devuelve tal cual
    si "." en t:
        devolver t
    # Cripto con guion escrito manualmente
    Si "-USD" está en t o "-EUR" está en t:
        devolver t
    # Empresas mexicanas con diagonal
    si "/" en t:
        return t.replace("/", "") + ".MX"
    devolver t

def calcular_rsi(serie, periodo=14):
    delta = serie.diff()
    gan = delta.clip(lower=0)
    por = -delta.clip(upper=0)
    avg_gan = gan.rolling(periodo).mean()
    avg_per = por.rolling(periodo).mean()
    rs = avg_gan / avg_per.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    retorno rsi

def calcular_macd(serie):
    ema12 = serie.ewm(span=12, ajustar=False).mean()
    ema26 = serie.ewm(span=26, ajustar=False).mean()
    MACD = EMA12 - EMA26
    señal = macd.ewm(span=9, ajustar=False).mean()
    devolver macd, señal

def calcular_bb(serie, periodo=20):
    media = serie.rolling(periodo).media()
    std = serie.rolling(periodo).std()
    superior = media + (2 * desviación estándar)
    inferior = media - (2 * desviación estándar)
    retorno superior, medios, inferior

def analizar_semaforo(df, precio_actual, info, categoria):
    puntos = 0
    razones = []
    alertas = []

    rsi_serie = calcular_rsi(df['Cerrar'])
    rsi = rsi_serie.iloc[-1]

    Si rsi < 30:
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
    demás:
        razones.append(f"🔵 RSI en {rsi:.1f} — Zona neutral")

    macd, señal_macd = calcular_macd(df['Close'])
    si macd.iloc[-1] > señal_macd.iloc[-1] y macd.iloc[-2] <= señal_macd.iloc[-2]:
        puntos += 2
        razones.append("✅ MACD cruzó al alza — señal de impulso positivo")
    elif macd.iloc[-1] > señal_macd.iloc[-1]:
        puntos += 1
        razones.append("✅ MACD por encima de señal — tendencia alcista activa")
    elif macd.iloc[-1] < señal_macd.iloc[-1] y macd.iloc[-2] >= señal_macd.iloc[-2]:
        puntos -= 2
        alertas.append("🔴 MACD cruzó a la baja — señal de impulso negativo")
    demás:
        puntos -= 1
        alertas.append("⚠️ MACD por debajo de señal — vendedora de presión")

    ma50 = df['Close'].rolling(50).mean() .iloc[-1]
    ma200 = df['Close'].rolling(200).mean( ).iloc[-1] if len(df) >= 200 else None

    si precio_actual > ma50:
        puntos += 1
        razones.append(f"✅ Precio (${precio_actual:.2f}) sobre MA50 (${ma50:.2f})")
    demás:
        puntos -= 1
        alertas.append(f"⚠️ Precio bajo MA50 — tendencia de corto plazo bajista")

    Si ma200 no es None:
        Si precio_actual > ma200:
            puntos += 1
            razones.append(f"✅ Precio sobre MA200 (${ma200:.2f}) — tendencia larga alcista")
        demás:
            puntos -= 1
            alertas.append(f"⚠️ Precio bajo MA200 (${ma200:.2f}) — tendencia larga bajista")

    techo = df['High'].max()
    piso = df['Low'].min()
    rango = techo - piso
    posicion_pct = ((precio_actual - piso) / rango * 100) si rango > 0 sino 50

    Si posicion_pct < 25:
        puntos += 2
        razones.append(f"✅ Precio en zona baja del rango anual ({posicion_pct:.0f}%) — posible piso")
    elif posicion_pct > 75:
        puntos -= 2
        alertas.append(f"⚠️ Precio en zona alta del rango anual ({posicion_pct:.0f}%) — riesgo de corrección")
    demás:
        razones.append(f"🔵 Precio en zona media del rango ({posicion_pct:.0f}%)")

    bb_up, bb_mid, bb_low = calcular_bb(df['Close'])
    si precio_actual < bb_low.iloc[-1]:
        puntos += 2
        razones.append(f"✅ Precio bajo Banda Bollinger inferior — zona de rebote potencial")
    elif precio_actual > bb_up.iloc[-1]:
        puntos -= 2
        alertas.append(f"🔴 Precio sobre Banda Bollinger superior — sobreextendido")

    es_cripto = any(c in categoria for c in ["Cripto", "Startup"])
    pe_ratio = Ninguno
    si no es_cripto y info:
        intentar:
            pe_ratio = info.get('trailingPE', None)
            márgenes_de_beneficio = info.get('profitMargins', None)
            crecimiento_de_ingresos = info.get('crecimiento_de_ingresos', None)
            deuda_capital = info.get('debtToEquity', None)

            Si pe_ratio y pe_ratio > 0:
                Si pe_ratio < 15:
                    puntos += 2
                    razones.append(f"✅ P/E de {pe_ratio:.1f} — valoración atractiva (Lynch: busca <15)")
                elif pe_ratio < 25:
                    puntos += 1
                    razones.append(f"✅ P/E de {pe_ratio:.1f} — valuación razonable")
                elif pe_ratio > 50:
                    puntos -= 2
                    alertas.append(f"🔴 P/E de {pe_ratio:.1f} — caro, fundamentales débiles vs precio")
                demás:
                    alertas.append(f"⚠️ P/E de {pe_ratio:.1f} — valuación elevada")

            Si profit_margins y profit_margins > 0,15:
                puntos += 1
                razones.append(f"✅ Margen de ganancia {profit_margins*100:.1f}% — empresa rentable")
            elif profit_margins and profit_margins < 0:
                puntos -= 1
                alertas.append(f"⚠️ Empresa con pérdidas — margen negativo")

            Si revenue_growth y revenue_growth > 0,10:
                puntos += 1
                razones.append(f"✅ Crecimiento de ingresos {revenue_growth*100:.1f}% — empresa expandiéndose")

            Si debt_equity y debt_equity > 200:
                puntos -= 1
                alertas.append(f"⚠️ Deuda/Capital elevada ({debt_equity:.0f}) — riesgo financiero")
        excepto:
            aprobar

    # ── ESCUDO DE VOLUMEN ────────────────────────
    vol_avg = df['Volume'].rolling(20).mean( ).iloc[-1]
    vol_hoy = df['Volumen'].iloc[-1]

    Si vol_hoy > vol_avg * 1.8 y df['Close'].iloc[-1] < df['Close'].iloc[-2]:
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

    Si puntos >= 6:
        color="verde"; emoji = "🟢"; decisión = "INYECTAR CAPITAL"
        descripcion = "Múltiples señales técnicas y fundamentales positivas alineadas. Es momento de considerar una entrada."
    elif puntos >= 2:
        color="azul"; emoji = "🔵"; decisión = "NEUTRAL — ESPERAR"
        descripcion = "Señales mixtas sin dirección clara. Observa más antes de comprometer capital."
    elif puntos >= -2:
        color = "amarillo"; emoji = "🟡"; decisión = "PUEDE SEGUIR CAYENDO"
        descripcion = "Señales con sesgo bajista. El precio podría continuar corrigiendo. Paciencia."
    demás:
        color = "rojo"; emoji = "🔴"; decisión = "NO COMPRAR AHORA"
        descripcion = "Múltiples señales negativas. Esperar confirmación de piso antes de entrar."

    devolver {
        "color": color, "emoji": emoji, "decision": decisión,
        "descripcion": descripcion, "puntos": puntos,
        "razones": razones, "alertas": alertas,
        "rsi": rsi, "ma50": ma50, "ma200": ma200,
        "techo": techo, "piso": piso, "posicion_pct": posicion_pct,
        "pe_ratio": pe_ratio,
        "bb_up": bb_up.iloc[-1], "bb_low": bb_low.iloc[-1]
    }

def calcular_rescate(cant_actual, inv_total_orig, precio_mercado, cat_sel, techo_y, piso_m):
    Si cant_actual <= 0 o inv_total_orig <= 0:
        devolver Ninguno

    precio_promedio = inv_total_orig / cant_actual
    perdida_actual = (precio_mercado - precio_promedio) * cant_actual
    pct_perdida = ((precio_mercado / precio_promedio) - 1) * 100

    narrativa = narrativas[cat_sel]
    meta_pct = narrativa["meta_pct"]

    distancia_piso = ((precio_mercado - piso_m) / precio_mercado) * 100
    stop_loss_sugerido = piso_m * 0.97

    niveles = []
    porcentajes = [0,25, 0,50, 1,00]
    nombres = ["Nivel 1 — Conservador (25%)", "Nivel 2 — Moderado (50%)", "Nivel 3 — Agresivo (100%)"]

    para pct, nombre en zip(porcentajes, nombres):
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

    devolver {
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


# ───────────────────────────── ───────────────
# MOTOR PRO VITERBI (simplificado sin HMM externo)
# ───────────────────────────── ───────────────
def motor_pro_viterbi(df, rsi_actual, score_semaforo):
    caida_reciente = (df["Cerrar"].iloc[-1] / df["Alto"].max() - 1) * 100
    vol_avg = df["Volume"].rolling(20).mean( ).iloc[-1]
    volumen_stop = df["Volumen"].iloc[-1] > vol_avg * 1.5

    estado = "LATERAL"
    Si score_semaforo >= 6:
        estado = "ALCISTA"
    elif score_semaforo <= -2:
        estado = "BAJISTA"

    rebote_confirmado = (
        caída_reciente < -3.0
        y volumen_stop
        y df["Cerrar"].iloc[-1] > df["Abrir"].iloc[-1]
    )
    retorno estado, rebote_confirmado, caida_reciente

# ───────────────────────────── ───────────────
# CALCULADORA DE LIQUIDACIÓN REAL (GBM + ISR MX)
# ───────────────────────────── ───────────────
def calcular_efectivo_real(precio_ venta, precio_compra, titulos):
    inversion = precio_compra * titulos
    venta_bruta = precio_venta * titulos
    ganancia_bruta = venta_bruta - inversión
    comision_gbm = venta_bruta * 0.0025 * 1.16 # 0.25% + IVA 16%
    impuesto_isr = max(0, (ganancia_bruta - comision_gbm) * 0.10) # 10% ISR
    efectivo_limpio = venta_bruta - comision_gbm - impuesto_isr
    devolución efectivo_limpio, ganancia_bruta, comision_gbm, impuesto_isr

# ───────────────────────────── ───────────────
# BOT DE ESTRATEGIA — VEREDICTO MAESTRO
# ───────────────────────────── ───────────────
def bot_sentencia_lino(es_ portafolio, estado_pro, rebote, rendimiento, ma200, precio_actual, rsi):
    """Genera el mensaje de voz/texto del Bot y el HTML del widget con bocina."""
    si es_portafolio:
        Si el rendimiento es < -10:
            si rebote:
                msg = (f"Ejecuta Rescate. La caída fue dura pero el volumen confirma rebote. "
                       f"No esperes más, baja tu promedio ahora.")
                emoji = "🔥"
                color = "#2ea043"
            elif ma200 y precio_actual < ma200:
                msg = ("Alto. Estás en zona de pérdida y bajo la MA200. "
                       "No metas más dinero. Es una trampa. Espera soporte real.")
                emoji = "🛑"
                color = "#f85149"
            demás:
                msg = ("Paciencia. El mercado está sangrando. "
                       "Mantén disciplina. No operes por emoción.")
                emoji = "⏳"
                color = "#d29922"
        elif rendimiento > 5:
            msg = ("Momento de cobrar. Vas en verde. "
                   "Considera tomar el cincuenta por ciento de ganancias para reinvertir en oportunidades de piso.")
            emoji = "💰"
            color = "#2ea043"
        demás:
            msg = ("Posición estable. Monitorea el soporte mensual y espera confirmación antes de mover capital.")
            emoji = "📡"
            color = "#58a6ff"
    demás:
        if estado_pro == "ALCISTA" y rebote:
            msg = ("Entrada de élite detectada. Confirmación de giro alcista. Alta probabilidad. Considere entrar ahora.")
            emoji = "🎯"
            color = "#2ea043"
        elif estado_pro == "BAJISTA":
            msg = ("Motor detecta debilidad estructural. Aunque veas señales verdes, espera mejor confirmación.")
            emoji = "⚠️"
            color = "#d29922"
        demás:
            msg = ("Escaneando mercado. No hay señales de alta probabilidad. Un ganador sabe cuándo no jugar.")
            emoji = "📡"
            color = "#58a6ff"

    mensaje de retorno, emoji, color

def render_bot_voz(msj, emoji, color, ticker):
    """Renderiza el widget del bot con botón de bocina y Web Speech API."""
    msg_js = msg.replace("'", " ").replace('"', ' ').replace("\n", " ")
    componentes.html(f"""
    <div style="background:linear- gradient(135deg,#161b22,# 1c2128); border:2px solid {color};
         border-radius:16px; padding:20px 24px; margin:12px 0; display:flex;
         align-items:flex-start; gap:16px;">
        <div style="font-size:2.2rem; line-height:1;">{emoji}</div>
        <div style="flex:1;">
            <div style="color:{color}; font-weight:700; font-size:0.85rem; margin-bottom:4px;">
                🤖 VEREDICTO MAESTRO AI.lino · {ticker}
            </div>
            <div style="color:#e6edf3; font-size:1rem; line-height:1.6;" id="bot_msg_{ticker.replace('. ','_')}">
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
    función hablarBot() {{
        si ('speechSynthesis' en window) {{
            ventana.síntesisDeVoz.cancelar( );
            var u = new SpeechSynthesisUtterance('{ msg_js}');
            u.lang = 'es-MX';
            u.rate = 0,95;
            u.pitch = 1.0;
            var voces = window.speechSynthesis.getVoices ();
            var esp = voices.find(v => v.lang && v.lang.startsWith('es'));
            si (esp) u.voice = esp;
            ventana.síntesisDeVoz.hablar( u);
        }} demás {{
            alert('Tu navegador no soporta síntesis de voz.');
        }}
    }}
    // Pre-cargar voces
    ventana.síntesisDeVoz.obtenerVoces ();
    </script>
    "", altura=140)

# ───────────────────────────── ───────────────
# 5. ESTADO DE LA SESIÓN
# ───────────────────────────── ───────────────
Si 'community_strategies' no está en st.session_state:
    st.session_state['community_strategys '] = [
        {
            'autor': 'Lino', 'activo': 'BTC-USD',
            'categoria': '🚀 Inicio/Cripto',
            'estrategia': 'Hacer DCA mensual hasta los $100k. Comprar fuerte si rompe el piso de los $50k.',
            'fecha': '2026-03-16'
        }
    ]

# ───────────────────────────── ───────────────
# 6. ENCABEZADO
# ───────────────────────────── ───────────────
# ── BARRA LATERAL ────────────────────────────── ───────
con st.sidebar:
    st.markdown("## 🧠 AI.lino")
    st.caption("Motor de Inversión Inteligente")
    st.markdown("---")
    st.markdown("### 🚀 Herramientas de Élite")
    st.link_button("Ir a AI.Lino PRO (Viterbi)", " https://ailinopro-maquina- dinero-lino.streamlit.app/ ",
                   use_container_width=True)
    st.caption("Utilice el Motor Pro para confirmar señales de entrada y salida con precisión HMM.")
    st.markdown("---")
    st.link_button("🎁 Apoyar el proyecto", " https://buymeacoffee.com/ Hugo.lino ", use_container_width=True)

# ── ENCABEZADO ───────────────────────────── ─────────
col_h1, col_h2 = st.columns([8, 2])
con col_h1:
    st.title("🧠 AI.lino")
    st.markdown("### Simulador de Mercado · Análisis VIP · Comunidad de Estrategias")
con col_h2:
    # Botón salir solo visible si está autenticado (Modo Portafolio)
    si st.session_state.get(" autenticado"):
        nombre_usr = st.session_state.get("usuario_ nombre", "")
        st.write("<br>", unsafe_allow_html=True)
        st.caption(f"🔐 Sesión VIP: {nombre_usr}")
        if st.button("🔒 Salir", use_container_width=True):
            st.session_state["autenticado" ] = Falso
            st.rerun()

st.markdown("---")

# ───────────────────────────── ───────────────
# 7. MODOS
# ───────────────────────────── ───────────────
modo = st.radio(
    "Qué deseas hacer hoy?",
    ["🔍 Modo Explorador (Gratis)", "💼 Modo Portafolio (Suite Premium)", "🤝 Comunidad de Estrategias"],
    horizontal=Verdadero
)

# ═════════════════════════════ ═════════════════
# MODOS EXPLORADOR Y PORTAFOLIO
# ═════════════════════════════ ═════════════════
if "Comunidad" not in modo:
    col1, col2 = st.columns([1, 2])
    con col1:
        ticker_input = st.text_input("Símbolo (ej. TSLA, GMEXICO, BTC, SOL):", "TSLA")
        ticker_limpio = limpiar_ticker(ticker_input)
    con col2:
        categoria = st.selectbox("Categoría de Activo (Estilo Peter Lynch):", list(narrativas.keys()))

    if "Explorador" in modo:
        inversion_sim = st.number_input("💰 Capital que deseas simular (USD/MXN):", min_value=100.0, value=10000.0)
        cant = 0.0
        total_inv = 0.0
    demás:
        c1, c2 = st.columns(2)
        con c1:
            cant = st.number_input("📦 Títulos / Fracciones que tienes:", min_value=0.0, value=10.0, format="%0.8f")
        con c2:
            total_inv = st.number_input("💵 Costo Total Invertido ($):", min_value=0.01, value=5000.0)
        inversión_sim = 0.0

    # ── INICIAR SESIÓN solo para Modo Portafolio (antes de ejecutar) ──────
    if "Portafolio" in modo and not st.session_state.get(" autenticado"):
        pantalla_login()
        st.stop()

    ejecutar = st.button("📊 Ejecutar Motor AI.lino", use_container_width=False)

    si ejecutar:
        with st.spinner("Conectando con mercados en tiempo real..."):
            intentar:
                stock = yf.Ticker(ticker_limpio)
                df_1y = stock.history(period="1y")
                df_1m = stock.history(period="1mo", interval="1h")

                si df_1y.empty:
                    st.error(f"❌ No se encontraron datos para '{ticker_input}'. Verifica el símbolo.")
                    st.stop()

                # ── Datos base ────────────────────────────── ─
                precio_actual = df_1y['Close'].iloc[-1]
                techo_y = df_1y['Alto'].max()
                piso_anual = df_1y['Low'].min()

                # ── PISO MENSUAL: Bajo del mes calendario anterior ──
                hoy = pd.Timestamp.now(tz= df_1y. index.tz )
                mes_ant = hoy.month - 1 si hoy.month > 1 sino 12
                anio_ant = hoy.año si hoy.mes > 1 else hoy.año - 1
                hist_mes_ant = df_1y[
                    (df_1y.index.month == mes_ant) & (df_1y.index.year == anio_ant)
                ]
                piso_m = float(hist_mes_ant['Low'].min( )) if not hist_mes_ant.empty else float(df_1y.tail(22)['Low']. min())

                # ── EMA Mensual: EMA20 sobre los últimos ~20 días hábiles ──
                ema_mensual = float(df_1y['Close'].ewm(span= 20, adjust=False).mean().iloc[-1])

                # ── Información fundamental ─────────────────────────
                intentar:
                    información = stock.info
                    nombre_empresa = info.get('nombre largo', ticker_limpio)
                    sector = info.get('sector', 'N/A')
                    país = info.get('país', 'N/A')
                excepto:
                    información = {}
                    nombre_empresa = ticker_limpio
                    sector = 'N/A'
                    país = 'N/A'

                st.success(f"🟢 Datos obtenidos en tiempo real · **{nombre_empresa}** · Sector: {sector}")

                # ────────────────────────────
                # SEMÁFORO DE DECISIÓN
                # ────────────────────────────
                analisis = analizar_semaforo(df_1y, precio_actual, info, categoria)

                st.markdown("## 🚦 Semáforo de Decisión AI.lino")
                clase_css = f"semaforo-{analisis['color']} "
                st.markdown(f"""
                <div class="{clase_css}">
                    <h1 style="font-size:3.5rem; margin:0;">{análisis['emoji']} </h1>
                    <h2 style="color:white; margin:8px 0;">{análisis['decisión']}</ h2>
                    <p style="color:#ccc; font-size:1.1rem; margin:0;">{análisis[' descripcion']}</p>
                    <p style="color:#aaa; margin-top:12px; font-size:0.9rem;">Puntuación técnica: <b>{analisis['puntos']:+d} puntos</b></p>
                </div>
                "", unsafe_allow_html=True)

                st.write("")

                #──MOTOR PRO + BOT DE VOZ ────────────────────
                estado_pro, rebote_pro, caida_pro = motor_pro_viterbi(
                    df_1y, análisis["rsi"], análisis["puntos"]
                )
                es_portafolio = "Portafolio" en modo
                rendimiento_bot = ((precio_actual / (total_inv / cant) - 1) * 100
                                   si es_portafolio y cant > 0 y total_inv > 0
                                   de lo contrario 0)
                msg_bot, emoji_bot, color_bot = bot_sentencia_lino(
                    es_portafolio, estado_pro, rebote_pro,
                    rendimiento_bot, analisis["ma200"], precio_actual, analisis["rsi"]
                )
                render_bot_voz(msg_bot, emoji_bot, color_bot, ticker_limpio)

                col_r, col_a = st.columns(2)
                con col_r:
                    st.markdown("#### ✅ Señales Positivas")
                    para r in (análisis['razones'] o ["- Sin señales positivas detectadas"]):
                        st.markdown(f"- {r}")
                con col_a:
                    st.markdown("#### ⚠️ Alertas y Riesgos")
                    para a in (análisis['alertas'] o ["- Sin alertas detectadas"]):
                        st.markdown(f"- {a}")

                st.markdown("---")

                # ───────────────────────────── ───────────────
                # PANEL ANALÍTICO — con Piso Mensual y EMA Mensual
                # ───────────────────────────── ───────────────
                st.markdown("## 📐 Panel Analítico")

                i1, i2, i3, i4, i5 = st.columns(5)
                i1.metric("💲 Precio Actual", f"${precio_actual:,.2f}")
                i2.metric("📊 RSI (14D)", f"{análisis['rsi']:.1f}",
                          delta="Sobrevendido" if analisis['rsi'] < 35 else ("Sobrecomprado" if analisis['rsi'] > 65 else "Neutral"))
                i3.metric("📈 MA50", f"${analisis['ma50']:,.2f}",
                          delta=f"{((precio_actual / analisis['ma50']) - 1) * 100:.1f}% vs precio")
                i4.metric("🔺 Techo Anual", f"${techo_y:,.2f}")
                i5.metric("🔻 Piso Anual", f"${piso_anual:,.2f}")

                # ── FILA 2: Piso Mensual + EMA Mensual + BB ──────── NUEVO
                p1, p2, p3, p4, p5 = st.columns(5)
                p1.metric("📅 Piso Mensual", f"${piso_m:,.2f}",
                          delta=f"{((precio_actual / piso_m) - 1) * 100:.1f}% vs precio")
                p2.metric("〰️ EMA Mensual (20D)", f"${ema_mensual:,.2f}",
                          delta=f"{((precio_actual / ema_mensual) - 1) * 100:.1f}% vs precio")
                Si análisis['ma200'] no es None:
                    p3.metric("📉 MA200", f"${analisis['ma200']:,.2f}",
                              delta=f"{((precio_actual / analisis['ma200']) - 1) * 100:.1f}% vs precio")
                demás:
                    p3.metric("📉 MA200", "N/D", delta="Historial insuficiente")
                si análisis['pe_ratio']:
                    p4.metric("📋 Relación precio/beneficio", f"{analisis['pe_ratio']:.1f}" )
                    p5.metric("📊 BB Superior", f"${analisis['bb_up']:,.2f}")
                demás:
                    p4.metric("📊 BB Superior", f"${analisis['bb_up']:,.2f}")
                    p5.metric("📊 BB Inferior", f"${analisis['bb_low']:,.2f}")

                st.markdown("---")

                # ────────────────────────────
                # MODO EXPLORADOR
                # ────────────────────────────
                if "Explorador" in modo:
                    st.markdown(f"## 🔍 Tablero AI.lino: {nombre_empresa}")
                    acciones_posibles = inversión_sim / precio_actual
                    st.info (
                        f"💼 Con **${inversion_sim:,.2f}** puedes comprar "
                        f"**{acciones_posibles:.4f}** títulos al precio actual de **${precio_actual:,.2f}**"
                    )
                    st.markdown("#### 📈 Histórico 1 Año")
                    st.line_chart(df_1y['Close'])
                    si no df_1m.empty:
                        st.markdown("#### 📡 Radar Último Mes (1H)")
                        st.line_chart(df_1m['Close'])

                # ────────────────────────────
                #MODO PORTAFOLIO — Suite VIP
                # ────────────────────────────
                demás:
                    precio_promedio = total_inv / no puedo si no puedo > 0 sino 0
                    valor_actual = precio_actual * no puedo
                    ganancia_perdida = valor_actual - total_inv
                    rendimiento = (ganancia_perdida / total_inv * 100) si total_inv > 0 sino 0

                    st.markdown(f"## 💎 Suite VIP AI.lino: {nombre_empresa}")

                    # ── Fila principal de portafolio ──────────────────
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Tu Promedio", f"${precio_promedio:,.2f}")
                    m2.metric("Precio Mercado", f"${precio_actual:,.2f}",
                              delta=f"{((precio_actual / precio_promedio) - 1) * 100:.1f}%" if precio_promedio > 0 else Ninguno)
                    m3.metric("Rendimiento", f"{rendimiento:.2f}%")
                    m4.metric("Valor Hoy", f"${valor_actual:,.2f}")

                    # ── NUEVA FILA: Piso Mensual + EMA Mensual ──────── NUEVO
                    v1, v2, v3 = st.columns(3)
                    v1.metric("📅 Piso Mensual", f"${piso_m:,.2f}",
                              delta=f"{((precio_actual / piso_m) - 1) * 100:.1f}% vs precio actual")
                    v2.metric("〰️ EMA Mensual (20D)", f"${ema_mensual:,.2f}",
                              delta=f"{((precio_actual / ema_mensual) - 1) * 100:.1f}% vs precio actual")
                    Si análisis['ma200'] no es None:
                        v3.metric("📉 MA200 (Anual)", f"${analisis['ma200']:,.2f}",
                                  delta=f"{((precio_actual / analisis['ma200']) - 1) * 100:.1f}% vs precio actual")
                    demás:
                        v3.metric("📉 MA200 (Anual)", "N/D")

                    # ── TradingView ────────────────────────────── ────
                    # Construir el símbolo correcto para TradingView
                    si ticker_limpio.endswith(".MX"):
                        base = ticker_limpio.replace(".MX", "")
                        tv_symbol = f"BMV:{base}"
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
                    demás:
                        tv_symbol = ticker_limpio # NASDAQ/NYSE ya funcionan directo
                    tv_widget = f"""
                    <div class="tradingview-widget- container">
                    <div id="tv_chart"></div>
                    <script src=" https://s3.tradingview. com/tv.js "></script>
                    <script>
                    nuevo TradingView.widget({{
                        "ancho": "100%", "alto": 420,
                        "símbolo": "{símbolo_tv}",
                        "intervalo": "D",
                        "tema": "oscuro",
                        "estilo": "1",
                        "locale": "es",
                        "toolbar_bg": "#161b22",
                        "hide_side_toolbar": false,
                        "container_id": "tv_chart"
                    }});
                    </script></div>"""
                    componentes.html(tv_widget, altura=430)

                    st.markdown("---")

                    # ═════════════════════════════ ═════════════════════
                    # CENTRO DE COMANDO — RESCATE INTELIGENTE AI.lino
                    # Fusión de: Mapa de Escalones + Motor de Rescate
                    # ═════════════════════════════ ═════════════════════
                    ma200_val = analisis.get("ma200")
                    narrativa_sc = narrativas[categoria]
                    piso_roto = precio_actual < piso_m

                    st.markdown("## 🎯 Centro de Comando — Rescate Inteligente AI.lino")

                    # ── Resumen de situación actual ───────────────────
                    Si el rendimiento es menor que 0:
                        col_sit1, col_sit2, col_sit3 = st.columns(3)
                        col_sit1.metric("📉 Pérdida actual",
                                        f"${abs(valor_actual - total_inv):,.2f}",
                                        delta=f"{rendimiento:.1f}%")
                        col_sit2.metric("💰 Tu promedio de compra", f"${precio_promedio:,.2f}")
                        col_sit3.metric("📌 Precio actual",
                                        f"${precio_actual:,.2f}",
                                        delta=f"{((precio_actual/ precio_promedio)-1)*100:.1f}%" )

                        # ── Escudo de contexto ─────────────────────────
                        si piso_roto:
                            st.error(f"🚨 **PISO MENSUAL ROTO** — El precio **${precio_actual:,.2f}** ya está por debajo del piso de **${piso_m:,.2f}**. Operar ahora es de alto riesgo. Usa los escalones de abajo como guía.")
                        demás:
                            dist_piso_pct = ((precio_actual - piso_m) / precio_actual) * 100
                            color_piso = "🟢" si dist_piso_pct > 5 sino "🟡"
                            st.info (f"{color_piso} **Piso mensual ${piso_m:,.2f} aún se mantiene** · Distancia: {dist_piso_pct:.1f}% · Stop Loss sugerido: **${piso_m * 0.97:,.2f}** (3% bajo el piso)")

                        # Filosofía Lynch
                        st.markdown(f"""
                        <div class="card">
                            <b>📖 Filosofía activa: {narrativa_sc['estilo']}</b>< br>
                            <span style="color:#8b949e;">{ narrativa_sc['mensaje']}</ span>
                        </div>
                        "", unsafe_allow_html=True)

                        st.markdown("---")

                        # ── Escalones integrados con simulación ────────
                        st.markdown("### 🪜 Mapa de Escalones → Simulación por Nivel")
                        st.caption(f"Cada escalón = mínimo real de un mes · Objetivo de salida: **{narrativa_sc['nombre_meta'] }** ({narrativa_sc['meta_pct']* 100-100:.0f}%)")

                        escalones = calcular_escalones(df_1y, precio_actual, piso_m, piso_anual,
                                                       narrativa_sc, no puede si no puede > 0 sino 1,
                                                       total_inv si total_inv > 0 sino precio_actual)

                        si escalones:
                            para esc en escaleras:
                                es_trampa = (ma200_val no es Ninguno y esc["nuevo_promedio"] > ma200_val)

                                # Colores y estilos según trampa o viable
                                borde_color = "#8b0000" if es_trampa else esc["nivel_color"]
                                bg_gradient = "linear-gradient(135deg,# 2d0a0a,#1c1010)" if es_trampa else "#1c2128"

                                # Insignia urgencia
                                si "PRECIO EN ZONA" en esc["alerta"]:
                                    urgencia = "🔴 DECIDIR AHORA"
                                    urgencia_bg = "#f85149"
                                elif "CERCA" en esc["alerta"]:
                                    urgencia = "🟡 PREPARAR CAPITAL"
                                    urgencia_bg = "#d29922"
                                demás:
                                    urgencia = f"🔵 {esc['dist_pct']:.1f}% de distancia"
                                    urgencia_bg = "#1f3a5c"

                                # Veredicto texto plano (sin HTML anidado)
                                si es_trampa:
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
                                demás:
                                    veredicto_icono = "✅"
                                    veredicto_titulo = "NIVEL VIABLE"
                                    veredicto_bg = "#0d2b1a"
                                    veredicto_borde = "#2ea043"
                                    si ma200_val:
                                        veredicto_texto = (
                                            f"Tu nuevo promedio ${esc['nuevo_promedio']:,.2f} quedaría "
                                            f"BAJO la MA200 ${ma200_val:,.2f} — camino libre hacia el objetivo."
                                        )
                                    demás:
                                        veredicto_texto = f"Tu nuevo promedio ${esc['nuevo_promedio']:,.2f} — sin resistencia MA200 detectada."

                                reduccion_pct = ((esc['nuevo_promedio'] / precio_promedio) - 1) * 100

                                # Render: cabecera de la tarjeta
                                st.markdown(
                                    f"""<div style="background:{bg_gradient }; border-left:6px solid {borde_color};
                                    border-radius:12px; padding:16px 20px; margin-bottom:4px;">
                                    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:8px;">
                                        <b style="color:{borde_color}; font-size:1rem;">{esc['nivel_ nombre']}</b>
                                        <span style="background:{urgencia_ bg}; color:white; padding:2px 10px;
                                        border-radius:6px; font-size:0.8rem; font-weight:700;">{urgencia}</ span>
                                    </div>
                                    <div style="color:#8b949e; font-size:0.85rem; margin-bottom:10px;">
                                        📍 Soporte: <b style="color:#e6edf3;">${esc[' precio']:,.2f}</b>
                                        ·  Mínimo de <b style="color:#e6edf3;">{esc[' nombre_mes']}</b>
                                        ·  A <b style="color:#e6edf3;">{esc[' dist_pct']:.1f}%</b> del precio actual
                                    </div>
                                    <div style="font-size:0.92rem; line-height:2.0; color:#e6edf3;">
                                        💵 Capital a inyectar: ​​<b>${esc['capital_extra']:,. 2f}</b>
                                        ·  Títulos nuevos: <b>{esc['nuevos_titulos']:.4f} </b><br>
                                        📊 Nuevo promedio: <b>${esc['nuevo_promedio']:,. 2f}</b>
                                        ·  Cambio vs hoy: <b>{reduccion_pct:.1f}%</b> <br>
                                        🎯 Meta {narrativa_sc['nombre_meta']}: <b>${esc['precio_meta']:,.2f}< /b>
                                        →  Ganancia estimada: <b>${esc['ganancia_meta']:,. 2f}</b>
                                    </div>
                                    </div>""",
                                    unsafe_allow_html=Verdadero
                                )
                                # Render: veredicto como bloque separado
                                st.markdown(
                                    f"""<div style="antecedentes:{veredicto_ bg}; borde:1px sólido {veredicto_borde};
                                    border-radius:8px; padding:10px 16px; margin-bottom:16px; font-size:0.9rem; color:#e6edf3;">
                                    {veredicto_icono} <b>{veredicto_titulo}:</b> {veredicto_texto}
                                    </div>""",
                                    unsafe_allow_html=Verdadero
                                )
                            st.warning("No hay suficiente historial mensual para calcular escalones.")

                        st.markdown("---")
                        st.warning(f"💡 **Consejo Lynch — {narrativa_sc['estilo']}:** {narrativa_sc['consejo']}")

                    elif rendimiento > 0:
                        st.success(f"🎉 **¡En ganancia! +${ganancia_perdida:,.2f} ({rendimiento:.2f}%)**")
                        precio_meta_obj = precio_promedio * narrativa_sc["meta_pct"]
                        si precio_actual >= precio_meta_obj:
                            globos st.balloons()
                            st.success(f"🏆 **¡Alcanzaste el objetivo {narrativa_sc['nombre_meta']}! ** Considera tomar ganancias parciales.")
                        demás:
                            falta = precio_meta_obj - precio_actual
                            st.info (
                                f"🎯 Objetivo {narrativa_sc['nombre_meta']}: **${precio_meta_obj:,.2f}** · "
                                f"Faltan **${falta:,.2f}** ({((precio_meta_obj / precio_actual) - 1) * 100:.1f}%)"
                            )

                        # ── CALCULADORA DE LIQUIDACIÓN REAL ──────────
                        st.markdown("---")
                        st.markdown("### 💸 Calculadora de Liquidación Real — GBM México")
                        st.caption("Simula cuánto efectivo limpio recibirías según el precio y los títulos que quieras vender.")
                        calc_col1, calc_col2 = st.columns(2)
                        con calc_col1:
                            precio_venta_sim = st.number_input(
                                "💲 Precio de venta similar ($):",
                                min_value=0.01,
                                valor=flotante(redondear(precio_actual , 2)),
                                formato="%.2f",
                                clave="precio_venta_sim"
                            )
                        con calc_col2:
                            titulos_vender = st.number_input(
                                "📦 Títulos que deseas vender:",
                                min_value=0.0001,
                                valor_máximo=flotante(no puede),
                                valor=flotante(no puede),
                                formato="%0.4f",
                                clave="titulos_vender_sim",
                                help=f"Tienes {cant:.4f} títulos en total"
                            )
                        si precio_venta_sim > 0 y titulos_vender > 0:
                            # Calcular precio promedio ponderado solo de los títulos vendidos
                            precio_compra_sim = total_inv / no puedo si no puedo > 0 sino 0
                            limpio, g_bruta, com, isr = calcular_efectivo_real(
                                precio_venta_sim, precio_compra_sim, titulos_vender
                            )
                            inversion_parcial = precio_compra_sim * titulos_vender
                            pct_venta = (titulos_vender / cant * 100) si no puede > 0 sino 0

                            st.caption(f"Vendiendo **{titulos_vender:.4f}** títulos ({pct_venta:.1f}% de tu posición)")
                            liq1, liq2, liq3, liq4 = st.columns(4)
                            liq1.metric("💵 Efectivo Real", f"${limpio:,.2f}",
                                        help="Lo que llega a tu cuenta después de comisión e ISR")
                            liq2.metric("📈 Ganancia Bruta", f"${g_bruta:,.2f}")
                            liq3.metric("🏦 Comisión GBM", f"${com:,.2f}",
                                        help="0.25% + IVA 16% sobre el monto de venta")
                            liq4.metric("🏛️ ISR (10%)", f"${isr:,.2f}",
                                        help="10% sobre ganancia neta")
                            Si g_bruta > 0:
                                st.success(f"✅ Ganancia neta real después de impuestos: **${g_bruta - com - isr:,.2f}**")
                                # Mostrar posición restante
                                titulos_restantes = no puedo - titulos_vender
                                si titulos_restantes > 0:
                                    valor_restante = titulos_restantes * precio_actual
                                    st.info (f"📊 Posición restante: **{titulos_restantes:.4f}** títulos · Valor actual: **${valor_restante:,.2f}**")
                            demás:
                                st.warning(f"⚠️ Después de comisiones e ISR aún estarías en pérdida neta en esta venta.")


                # ═════════════════════════════ ═════════════════
                # REPORTE IA — ANÁLISIS NARRATIVO DE LA EMPRESA
                # ═════════════════════════════ ═════════════════
                st.markdown("---")
                st.markdown("## 📰 Reporte AI.lino — Análisis Situacional")
                st.caption(f"Generado con los datos actuales de {nombre_empresa} · {ticker_limpio} · Sector: {sector}")

                # Construir contexto para el informe
                ma200_txt = f"${analisis['ma200']:,.2f}" if analis['ma200'] else "no disponible"
                pe_txt = f"{analisis['pe_ratio']:.1f}x" if analisis['pe_ratio'] else "no disponible"
                tend_txt = "ALCISTA" if precio_actual > analisis['ma50'] else "BAJISTA"
                ma200_pos = ("por encima" if analisis['ma200'] y precio_actual > analisis['ma200']
                              else "por debajo" if analisis['ma200'] else "sin dato")
                vol_txt = ("con volumen elevado — posible movimiento institucional"
                              Si df_1y['Volume'].iloc[-1] > df_1y['Volume'].rolling(20). mean().iloc[-1] * 1.3
                              de lo contrario "con volumen normal")
                rsi_desc = ("en zona de sobreventa" if analisis['rsi'] < 35
                              else "en sobrecompra" if analisis['rsi'] > 65 else "en zona neutral")
                bb_pos = ("bajo la banda inferior — zona de rebote potencial"
                              si precio_actual < análisis['bb_low']
                              else "sobre la banda superior — sobreextendido"
                              if precio_actual > analisis['bb_up'] else "dentro de las bandas")
                caida_anual = ((precio_actual / techo_y) - 1) * 100
                rebote_anual = ((precio_actual / piso_anual) - 1) * 100
                estado_hmm = estado_pro si 'estado_pro' en dir() sino "LATERAL"

                # Párrafo 1: Situación técnica actual
                p1 = (
                    f"{nombre_empresa} ({ticker_limpio}) cotiza actualmente en **${precio_actual:,.2f}**, "
                    f"en tendencia {tend_txt} de corto plazo, operando {ma200_pos} de su MA200 ({ma200_txt}). "
                    f"El RSI de 14 días se encuentra en **{analisis['rsi']:.1f}**, {rsi_desc}, "
                    f"y el precio se ubica {bb_pos}. "
                    f"Respecto a su rango anual, el activo se encuentra un **{abs(caida_anual):.1f}%** "
                    f"{'por debajo de' if caida_anual < 0 else 'por encima de'} su máximo y un "
                    f"**{rebote_anual:.1f}%** por encima de su mínimo anual."
                )

                # Párrafo 2: Lectura del volumen y momento
                macd_val, señal_val = df_1y['Close'].ewm(span=12, adjust=False).mean().iloc[-1] - df_1y['Close'].ewm(span=26, adjust=False).mean().iloc[-1], 0
                macd_dir = "positivo" si macd_val > 0 sino "negativo"
                p2 = (
                    f"El volumen reciente ópera {vol_txt}. "
                    f"El MACD muestra impulso {macd_dir}, "
                    f"{'confirmando presión compradora' if macd_dir == 'positivo' else 'sugiriendo presión vendedora'}. "
                    f"El Motor Pro Viterbi clasifica el estado actual del activo como **{estado_hmm}**"
                    f"{', con señal de rebote confirmada por volumen' if rebote_pro else ', sin confirmación de rebote aún'}."
                )

                # Párrafo 3: Contexto fundamental
                si análisis['pe_ratio']:
                    Si análisis['pe_ratio'] < 15:
                        fund_txt = f"Su P/E de {pe_txt} la ubica en zona de valor atractiva según el método Lynch."
                    elif análisis['pe_ratio'] < 30:
                        fund_txt = f"Su P/E de {pe_txt} es razonable para el sector {sector}."
                    demás:
                        fund_txt = f"Su P/E de {pe_txt} refleja valuación elevada — el mercado paga prima por crecimiento esperado."
                demás:
                    fund_txt = f"No se dispone de P/E actualizado para {ticker_limpio} en Yahoo Finance."

                p3 = (
                    f"Desde la perspectiva fundamental, {fund_txt} "
                    f"El semáforo AI.lino emite señal **{analisis['decision']}** "
                    f"con un puntaje técnico de **{análisis['puntos']:+d} puntos**. "
                    f"{'Los fundamentos y la técnica están alineados favorablemente.' if analisis['puntos'] >= 4 else 'Se recomienda esperar mayor confluencia de señales antes de operar.'}"
                )

                # Párrafo 4: Conclusión operativa
                if análisis['color'] == 'verde':
                    conclusión = (
                        f"En conclusión, {nombre_empresa} presenta una configuración técnica favorable. "
                        f"Los niveles de soporte clave a monitorear son el piso mensual en **${piso_m:,.2f}** "
                        f"y el piso anual en **${piso_anual:,.2f}**. "
                        f"Una ruptura sostenida por encima de la MA200 ({ma200_txt}) confirmaría la continuación alcista."
                    )
                análisis elif['color'] == 'rojo':
                    conclusión = (
                        f"En conclusión, {nombre_empresa} muestra señales de debilidad técnica. "
                        f"El riesgo principal es una extensión de la caída hacia el piso anual en **${piso_anual:,.2f}**. "
                        f"Se recomienda no agregar posiciones hasta que el precio estabilice sobre su MA50 (${analisis['ma50']:,.2f})."
                    )
                demás:
                    conclusión = (
                        f"En conclusión, {nombre_empresa} se encuentra en una zona de decisión. "
                        f"El soporte más cercano es **${piso_m:,.2f}** (piso mensual). "
                        f"El catalizador para una entrada de menor riesgo sería un cierre por encima de la MA50 (${analisis['ma50']:,.2f}) "
                        f"con volumen superior al promedio."
                    )

                # Renderizar el reporte
                st.markdown(f"""
                <div style="background:linear- gradient(135deg,#0d1117,# 161b22); border:1px solid #30363d;
                     border-radius:16px; padding:28px 32px; line-height:1.9; color:#e6edf3;">
                    <p style="margin-bottom:14px;">{ p1}</p>
                    <p style="margin-bottom:14px;">{ p2}</p>
                    <p style="margin-bottom:14px;">{ p3}</p>
                    <p style="margin-bottom:0; border-top:1px solid #30363d; padding-top:14px;
                       color:#58a6ff;">{conclusión} </p>
                </div>
                "", unsafe_allow_html=True)

                # Botón de voz para el reporte completo
                reporte_completo = f"{p1} {p2} {p3} {conclusión}"
                reporte_js = reporte_completo.replace("'", " ").replace('"', ' ').replace("**", "").replace("$", " dólares ")
                componentes.html(f"""
                <div style="text-align:right; margin-top:8px;">
                    <button onclick="leerReporte()" title="Escuchar informe completo"
                        style="background:#30363d; border:1px solid #58a6ff; border-radius:8px;
                        relleno:8px 16px; color:#58a6ff; tamaño de fuente:0.9rem; cursor:pointer;">
                        🔊 Escuchar reporte completo
                    </button>
                </div>
                <script>
                función leerReporte() {{
                    si ('speechSynthesis' en window) {{
                        ventana.síntesisDeVoz.cancelar( );
                        var u = new SpeechSynthesisUtterance('{ reporte_js}');
                        u.lang = 'es-MX'; u.rate = 0.92; u.pitch = 1.0;
                        var voces = window.speechSynthesis.getVoices ();
                        var esp = voices.find(v => v.lang && v.lang.startsWith('es'));
                        si (esp) u.voice = esp;
                        ventana.síntesisDeVoz.hablar( u);
                    }}
                }}
                ventana.síntesisDeVoz.obtenerVoces ();
                </script>
                "", altura=60)

            excepto Exception como e:
                st.error(f"⚠️ Error inesperado: {e}")
                st.info ("Verifica que el símbolo sea correcto. Ejemplos: TSLA, AAPL, BTC-USD, GMEXICOB.MX , ETH-USD, SOL-USD")

# ═════════════════════════════ ═════════════════
# COMUNIDAD
# ═════════════════════════════ ═════════════════
demás:
    st.markdown("## 🤝 Comunidad de Estrategias AI.lino")
    st.caption("Comparte y aprende de las mejores jugadas de la comunidad.")

    col_c1, col_c2 = st.columns([1, 2])

    con col_c1:
        st.markdown("### 📝 Publica tu Estrategia")
        con st.form("crear_estrategia"):
            autor = st.text_input("Tu Nombre o Nickname:", placeholder="ej. Lobo de Wall Street")
            activo = st.text_input("Activo / Símbolo:", placeholder="ej. BTC-USD, GMEXICO, S&P 500").upper()
            cat_comm = st.selectbox("Categoría:", list(narrativas.keys()))
            estrategia = st.text_area("Tu Estrategia Detallada:", placeholder="ej. Comprar si rompe la resistencia de los $X, buscando el techo en $Y. Stop Loss en $Z.", height=120)
            publicar = st.form_submit_button("📢 Publicar en Comunidad")
            si publicar:
                si autor y activo y estrategia:
                    st.session_state['community_strategys '].insert(0, {
                        'autor': autor, 'activo': activo,
                        'categoria': cat_comm, 'estrategia': estrategia,
                        'fecha': str(datetime.date.today())
                    })
                    st.success("✅ Estrategia publicada.")
                    st.rerun()
                demás:
                    st.warning("Completa todos los campos antes de publicar.")

    con col_c2:
        st.markdown("### 📡 Feed de Estrategias Públicas")
        para estr en st.session_state['community_strategys ']:
            st.markdown(f"""
            <div class="strategy-card">
                <b>👤 Autor: {estr['autor']}</b><br>
                <small>Activo: {estr['activo']} | Categoría: {estr.get('categoria', '—')} | Publicado: {estr['fecha']}</small><br>< br>
                {estr['estrategia']}
            </div>
            "", unsafe_allow_html=True)
