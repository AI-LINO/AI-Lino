import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components
import datetime
import requests

# 1. CONFIGURACIÓN Y DISEÑO
st.set_page_config(page_title="AI.lino Premium & Community", page_icon="🧠", layout="wide")

if 'community_strategies' not in st.session_state:
    st.session_state['community_strategies'] = [
        {
            'autor': 'Lino',
            'activo': 'BTC-USD',
            'categoria': '🚀 Startup / Cripto',
            'estrategia': 'Hacer DCA mensual hasta los $100k. Comprar fuerte si rompe el piso de los $50k.',
            'fecha': '2026-03-16'
        }
    ]

st.markdown("""
<style>
    .stApp {
        background-color: #e5e5f7; opacity: 0.9;
        background-image: repeating-radial-gradient(circle at 0 0, transparent 0, #e5e5f7 10px), repeating-linear-gradient(#d2d2d255, #d2d2d2);
        background-size: 20px 20px;
    }
    h1 { color: #1a1a1a !important; font-size: 3.5rem !important; }
    h2, h3, h4 { color: #2c3e50 !important; font-weight: bold !important; }
    p, span, label { color: #1a1a1a !important; font-weight: 600 !important; }
    div[data-testid="stMetricValue"] { color: #007bff !important; font-size: 2.2rem !important; font-weight: 800 !important; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea { background-color: #ffffff !important; color: #1a1a1a !important; border: 2px solid #2c3e50 !important; border-radius: 8px !important; }
    .stButton>button { background-color: #2c3e50 !important; color: white !important; border-radius: 8px !important; padding: 0.6rem 2rem !important; font-weight: bold !important; }
    .info-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); font-size: 1.05rem; line-height: 1.6; margin-bottom: 20px; }
    .premium-box { background-color: #1a1a1a; color: #f1c40f; padding: 15px; border-radius: 10px; border-left: 5px solid #f1c40f; margin-top: 10px;}
    .risk-box { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 2px solid #e74c3c; margin-top: 10px; }
    .strategy-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-top: 5px solid #007bff; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .strategy-autor { font-weight: bold; font-size: 1.1rem; color: #007bff; }
    .strategy-meta { font-size: 0.9rem; color: #6c757d; }
    .stFormSubmitButton>button { background-color: #007bff !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

modo_presentador = st.sidebar.toggle("🎥 Modo Presentador (Para grabar)")
if modo_presentador:
    st.markdown("<style>header {visibility: hidden;} .stRadio {display: none;}</style>", unsafe_allow_html=True)

header_title_col, header_btn_col = st.columns([8, 2])

with header_title_col:
    st.title("🧠 AI.lino")
    st.markdown("### Simulador de Mercado, Análisis VIP y Comunidad de Estrategias")

with header_btn_col:
    st.write("<br>", unsafe_allow_html=True)
    st.link_button("🎁 Donar para apoyar", "https://buymeacoffee.com/Hugo.lino", use_container_width=True)

st.markdown("---")

modo = st.radio("¿Qué deseas hacer hoy?", 
                ["🔍 Modo Explorador (Gratis)", "💼 Modo Portafolio (Suite Premium)", "🤝 Comunidad de Estrategias"], 
                horizontal=True)

if "Comunidad" not in modo:
    col1, col2 = st.columns([1, 2])
    with col1:
        ticker_input = st.text_input("Símbolo (ej. TSLA, GMEXICO, SOL):", "TSLA").upper().strip()
        dicc = { "S&P 500": "VOO", "SP500": "VOO", "IPC": "^MXX", "BMV": "^MXX", "NASDAQ": "QQQ", "BTC": "BTC-USD", "BITCOIN": "BTC-USD", "PEÑOLES": "PE&OLES.MX", "PE&OLES": "PE&OLES.MX", "GMEXICO": "GMEXICOB.MX", "GRUPO MEXICO": "GMEXICOB.MX" }
        ticker_limpio = dicc.get(ticker_input, ticker_input.replace(" ", ""))

    with col2:
        categoria = st.selectbox("Categoría de Activo (Estilo Peter Lynch):", 
                                 ["🔄 Cíclica (Minería, Chips, Autos)", "🚀 Startup / Cripto (Crecimiento Alto / Volatilidad)", "🛡️ Defensiva (Consumo, Fibras)", "🏛️ ETF / Índice (Inversión Pasiva)"])

    if "Explorador" in modo:
        inversion_sim = st.number_input("💰 Capital a simular (MXN/USD):", min_value=100.0, value=10000.0, step=500.0)
    else:
        c1, c2 = st.columns(2)
        with c1: cant = st.number_input("Títulos o Fracciones que tienes:", min_value=0.00000000, value=10.0, step=0.00000001, format="%0.8f")
        with c2: total_inv = st.number_input("Costo Total Invertido:", min_value=0.01, value=5000.0)

if "Comunidad" not in modo:
    if st.button("📊 Ejecutar Motor AI.lino"):
        with st.spinner("Procesando datos del mercado en servidores seguros..."):
            try:
                stock = yf.Ticker(ticker_limpio)
                df_y = stock.history(period="1y")
                
                if df_y.empty and not "-" in ticker_limpio and not ticker_limpio.startswith("^"):
                    ticker_prueba = f"{ticker_limpio}-USD"
                    stock_prueba = yf.Ticker(ticker_prueba)
                    if not stock_prueba.history(period="1y").empty:
                        ticker_limpio, stock, df_y = ticker_prueba, stock_prueba, stock_prueba.history(period="1y")

                if df_y.empty and not ticker_limpio.endswith(".MX") and not ticker_limpio.startswith("^"):
                    ticker_prueba = f"{ticker_limpio}.MX"
                    stock_prueba = yf.Ticker(ticker_prueba)
                    if not stock_prueba.history(period="1y").empty:
                        ticker_limpio, stock, df_y = ticker_prueba, stock_prueba, stock_prueba.history(period="1y")

                if df_y.empty and not ticker_limpio.endswith(".MX") and not ticker_limpio.startswith("^"):
                    ticker_prueba = f"{ticker_limpio}B.MX"
                    stock_prueba = yf.Ticker(ticker_prueba)
                    if not stock_prueba.history(period="1y").empty:
                        ticker_limpio, stock, df_y = ticker_prueba, stock_prueba, stock_prueba.history(period="1y")

                if df_y.empty:
                    st.error(f"❌ No se encontraron datos para '{ticker_input}'.")
                else:
                    df_m = df_y.tail(22)
                    techo_y = df_y['High'].max()
                    piso_m = df_m['Low'].min()
                    
                    API_KEY = "D6t23k1r01qoqoirutj0d6t23k1r01qoqoirutjg"
                    try:
                        finnhub_quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={ticker_limpio}&token={API_KEY}", timeout=3).json()
                        precio_actual = finnhub_quote['c'] if ('c' in finnhub_quote and finnhub_quote['c'] != 0) else df_y['Close'].iloc[-1]
                        
                        finnhub_profile = requests.get(f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker_limpio}&token={API_KEY}", timeout=3).json()
                        nombre_empresa = finnhub_profile.get('name', ticker_limpio)
                        descripcion = f"Sector: {finnhub_profile.get('finnhubIndustry', 'Mercado General')}. País: {finnhub_profile.get('country', 'N/A')}." if 'finnhubIndustry' in finnhub_profile else "Información corporativa cargada vía terminal segura."
                    except:
                        precio_actual = df_y['Close'].iloc[-1]
                        nombre_empresa = ticker_limpio
                        descripcion = "Información corporativa cargada vía terminal segura."
                    
                    pe_ratio = "Optimizado (Sin métricas lentas)"

                    capital_disponible = inversion_sim if "Explorador" in modo else total_inv
                    acciones_posibles = capital_disponible / precio_actual
                    
                    st.success("🟢 Conexión de Alta Velocidad establecida (API Privada Activa).")
                    st.info(f"🏷️ **Precio actual de {ticker_limpio}:** \${precio_actual:,.2f}\n\n"
                            f"💼 Con tu capital de **\${capital_disponible:,.2f}**, te alcanza para comprar **{acciones_posibles:.4f}** acciones (fracciones).")
                    
                    if "Explorador" in modo:
                        st.markdown(f"## 📡 Tablero AI.lino: {nombre_empresa}")
                        g1, g2 = st.columns(2)
                        with g1: st.write("**Histórico (1 Año)**"); st.line_chart(df_y['Close'])
                        with g2: st.write("**Radar (Último Mes)**"); st.line_chart(df_m['Close'])
                        st.info("💡 Desbloquea gráficas interactivas, Reportes Ejecutivos y el Asesor de Riesgos en el **Modo Portafolio (Suite Premium)**.")
                    else:
                        actual_val = precio_actual * cant
                        precio_promedio = total_inv / cant if cant > 0 else 0
                        rend = ((actual_val - total_inv) / total_inv) * 100 if total_inv > 0 else 0
                        ganancia_perdida = actual_val - total_inv
                        
                        # ==========================================
                        # CEREBRO INTERACTIVO DE PÉRDIDAS/GANANCIAS
                        # ==========================================
                        if rend < 0:
                            rebote_esperado = precio_actual * 1.03 
                            if precio_promedio > rebote_esperado:
                                acciones_a_comprar = cant * ((precio_promedio - rebote_esperado) / (rebote_esperado - precio_actual))
                                capital_necesario = acciones_a_comprar * precio_actual
                                
                                st.error(f"📉 **Ups, vas en pérdida de \${abs(ganancia_perdida):,.2f}**\n\n"
                                           f"💡 **Estrategia de Rescate:** Para salir 'tablas' aprovechando un mínimo rebote del 3% (si el precio sube a **\${rebote_esperado:,.2f}**), "
                                           f"necesitarías promediar invirtiendo aprox. **\${capital_necesario:,.2f}** extra a este precio actual.\n\n"
                                           f"⚠️ **OJO:** No promedies a ciegas. Ten en cuenta que el activo puede seguir cayendo hasta su piso mensual de **\${piso_m:,.2f}**.")
                            else:
                                st.error(f"📉 **Ups, vas en pérdida de \${abs(ganancia_perdida):,.2f}**\n\n"
                                           f"💡 **Tranquilidad:** Estás a menos de un 3% de recuperar tu costo. Un levísimo rebote te saca a ganancias. "
                                           f"Mantén la calma, pero pon una alerta por si se acerca al piso mensual de **\${piso_m:,.2f}**.")
                        
                        elif rend > 0:
                            st.success(f"🎉 **¡Felicidades! Llevas una ganancia viva de \${ganancia_perdida:,.2f}**\n\n"
                                       f"💡 **Consejo de Lobo:** Si el precio sigue empujando y toca su techo anual de **\${techo_y:,.2f}** o marca un nuevo máximo, "
                                       f"considera tomar un poco de ganancia (vender una fracción). Nadie quiebra por asegurar ganancias, ¡ese dinero ya es tuyo!")
                        else:
                            st.warning("⚖️ **Estás exactamente 'tablas' (sin pérdidas ni ganancias).**\n\n"
                                    "El mercado está consolidando. Espera a que defina dirección hacia el techo o el piso antes de tomar acción.")
                        # ==========================================
                        
                        st.markdown(f"## 💎 Suite VIP AI.lino: {nombre_empresa}")
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Tu Costo Promedio", f"${precio_promedio:,.2f}")
                        m2.metric("Precio del Mercado", f"${precio_actual:,.2f}")
                        m3.metric("Rendimiento Real", f"{rend:.2f}%")
                        m4.metric("Valor Inversión Hoy", f"${actual_val:,.2f}")
                        
                        st.markdown("---")

                        col_izq, col_der = st.columns([2, 1])
                        with col_izq:
                            st.markdown("### 📈 Gráfica Profesional (TradingView)")
                            tv_symbol = ticker_limpio.replace(".MX", "") if ".MX" in ticker_limpio else ticker_limpio
                            if "BTC" in tv_symbol: tv_symbol = "BINANCE:BTCUSD"
                            elif "ETH" in tv_symbol: tv_symbol = "BINANCE:ETHUSD"
                            elif "-USD" in tv_symbol: tv_symbol = f"BINANCE:{tv_symbol.replace('-USD', 'USD')}"
                            tv_widget = f"""<div class="tradingview-widget-container"><div id="tradingview_lino"></div><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({{ "width": "100%", "height": 400, "symbol": "{tv_symbol}", "interval": "D", "timezone": "Etc/UTC", "theme": "light", "style": "1", "locale": "es", "enable_publishing": false, "hide_top_toolbar": false, "save_image": false, "container_id": "tradingview_lino" }});</script></div>"""
                            components.html(tv_widget, height=410)
                        with col_der:
                            st.markdown("### 🔬 Panel Analítico"); delta = df_y['Close'].diff()
                            ganancia = delta.where(delta > 0, 0).rolling(window=14).mean(); perdida = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                            rsi_actual = (100 - (100 / (1 + (ganancia / perdida)))).iloc[-1]
                            
                            st.info(f"**Métricas Corporativas:** {pe_ratio}")
                            if pd.isna(rsi_actual): st.write("Calculando...")
                            elif rsi_actual < 30: st.success(f"**RSI (14D):** {rsi_actual:.1f} (Sobrevendida)")
                            elif rsi_actual > 70: st.error(f"**RSI (14D):** {rsi_actual:.1f} (Sobrecomprada)")
                            else: st.info(f"**RSI (14D):** {rsi_actual:.1f} (Neutral)")
                            st.markdown("### 🚨 Matriz de Salida"); st.markdown("<div class='risk-box'>", unsafe_allow_html=True)
                            if "ETF" in categoria: st.write("🏛️ **DCA:** Sigue promediando a la baja mes a mes.")
                            else:
                                if rend >= 15: st.write("✅ **Victoria:** Mueve tu Stop Loss a tu costo (\$" + f"{precio_promedio:.2f}" + ").")
                                elif rend > 0 and rend < 15: st.write("⚠️ **Alarma:** Pon alarma si baja a tu costo (\$" + f"{precio_promedio:.2f}" + "). Asegura tu capital.")
                                elif rend < 0 and rend > -8: st.write("📉 **Caída Normal:** Mantén si fundamentales siguen igual. Rompiendo \$" + f"{piso_m:.2f}" + ", evalúa.")
                                else: st.write("🩸 **Salida Urgente:** Caída mayor al 8%. Corta la pérdida y reubica capital.")
                            st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown("### 🎯 Sala de Simulación AI.lino")
                    precio_pensado = st.number_input("🤔 Simula escenario. Entrada Ideal:", value=float(precio_actual), step=0.0001, format="%0.4f")
                    potencial_subida = ((techo_y - precio_pensado) / precio_pensado) * 100
                    riesgo_caida = ((precio_pensado - piso_m) / precio_pensado) * 100 if precio_pensado > piso_m else 0
                    t1, t2, t3 = st.columns(3)
                    if "Cíclica" in categoria:
                        t1.success(f"🟢 **Compra:** Piso mensual: **\${piso_m:,.2f}**. Riesgo: **{riesgo_caida:.1f}%**."); t2.info(f"🔵 **Venta:** Techo anual de **\${techo_y:,.2f}**. Ganancia: **+{potencial_subida:.1f}%**.")
                        t3.error(f"🔴 **Regla:** Promedia a la baja solo si fundamentales siguen sólidos.")
                    elif "Startup" in categoria:
                        t1.success(f"🟢 **Oportunidad:** Piso: **\${piso_m:,.2f}**. Soporta volatilidad extrema."); t2.info(f"🔵 **Visión:** Techo reciente: **\${techo_y:,.2f}**. Busca ganancia **+{potencial_subida:.1f}%**.")
                        t3.error(f"🔴 **Riesgo:** Vende la posición únicamente si la empresa pierde ventaja competitiva.")
                    elif "Defensiva" in categoria:
                        t1.success(f"🟢 **Acumulación:** Piso: **\${piso_m:,.2f}**. Ofrece estabilidad."); t2.info(f"🔵 **Objetivo:** Techo: **\${techo_y:,.2f}** (+**{potencial_subida:.1f}%**). Cobra dividendos.")
                        t3.error(f"🔴 **Bajo:** Mantén la calma durante ajustes generales.")
                    else: 
                        t1.success(f"🟢 **DCA:** Aplicar estrategia DCA es la mejor opción."); t2.info(f"🔵 **Compuesto:** Techo histórico: **\${techo_y:,.2f}** (+**{potencial_subida:.1f}%**).")
                        t3.error(f"🔴 **Aviso:** Históricamente, los índices bursátiles siempre se recuperan.")

                    if "Explorador" not in modo:
                        st.markdown("---"); st.markdown("### 📰 Reporte Ejecutivo del Mercado")
                        precio_inicio_mes = df_m['Close'].iloc[0]; cambio_mes = ((precio_actual - precio_inicio_mes) / precio_inicio_mes) * 100
                        if cambio_mes < -2: comportamiento = "un retroceso evidente y presión bajista constante"
                        elif cambio_mes > 2: comportamiento = "un repunte técnico con sólido optimismo en el volumen de compras"
                        else: comportamiento = "oscilaciones laterales que reflejan cautela por parte de los operadores"
                        reporte = f"<div class='info-box'><b>Análisis de Acción de Precio:</b> En las últimas sesiones, el activo <b>{ticker_limpio}</b> ha mostrado {comportamiento}, registrando una variación del <b>{cambio_mes:.2f}%</b> en el último mes.<br><br>"
                        if "Cíclica" in categoria: reporte += "La dinámica actual refleja la sensibilidad de los capitales ante proyecciones macroeconómicas."
                        elif "Startup" in categoria: reporte += "Por pertenecer a un segmento de alto crecimiento, experimenta ajustes de alta volatilidad."
                        elif "Defensiva" in categoria: reporte += "Dada su estructura defensiva, busca demostrar resiliencia frente a la desaceleración."
                        else: reporte += "Como instrumento pasivo, absorbe impactos estructurales."
                        
                        reporte += f"<br><br><b>Descripción Corporativa:</b><br><i>{descripcion}</i></div>"; st.markdown(reporte, unsafe_allow_html=True)
                    
                    st.markdown("---"); st.markdown("### 🛠️ Las Herramientas de Lino"); st.info("Para ejecutar estas estrategias, utilizo y recomiendo personalmente estos exchanges. Si abres tu cuenta usando mis enlaces, ambos recibimos recompensas:")
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    with col_btn1: st.link_button("📈 Abrir cuenta en GBM+", "https://gbm.com/", use_container_width=True)
                    with col_btn2: st.link_button("🪙 Abrir cuenta en Bitso", "https://bitso.go.link/8XJIz?adj_label=jkrhp", use_container_width=True)
                    with col_btn3: st.link_button("💵 Abrir DolarApp (VIP)", "https://www.arqfinance.com/referrals/general?referralCode=hugohernandez1_ZUC", use_container_width=True)

            except Exception as e:
                st.error(f"⚠️ Error al conectar con el servidor: {e}")
else:
    st.markdown("## 🤝 Comunidad de Estrategias AI.lino")
    st.markdown("Aquí puedes interactuar y compartir tus mejores jugadas con la comunidad. Si eres un operador experimentado, ¡esta es tu zona!")

    col_comm1, col_comm2 = st.columns([1, 2])

    with col_comm1:
        st.markdown("### 📝 Publica tu Estrategia")
        with st.form("crear_estrategia", clear_on_submit=True):
            autor_form = st.text_input("Tu Nombre o Nickname:", placeholder="ej. Lobo de Wall Street")
            activo_form = st.text_input("Activo / Símbolo:", placeholder="ej. BTC-USD, GMEXICO, S&P 500").upper()
            categoria_form = st.selectbox("Categoría:", 
                                         ["🔄 Cíclica", "🚀 Startup / Cripto", "🛡️ Defensiva", "🏛️ ETF / Índice"])
            estrategia_form = st.text_area("Tu Estrategia Detallada:", placeholder="ej. Comprar si rompe la resistencia de los \$X, buscando el techo en \$Y. Stop Loss en \$Z.")
            
            submit_form = st.form_submit_button("📢 Publicar en Comunidad")
            
            if submit_form:
                if not autor_form or not activo_form or not estrategia_form:
                    st.error("⚠️ Por favor, llena todos los campos.")
                else:
                    nueva_jugada = {
                        'autor': autor_form,
                        'activo': activo_form,
                        'categoria': categoria_form,
                        'estrategia': estrategia_form,
                        'fecha': str(datetime.date.today())
                    }
                    st.session_state['community_strategies'].insert(0, nueva_jugada)
                    st.success("✅ ¡Estrategia publicada con éxito! Ya puedes verla en el feed de la comunidad.")
                    st.rerun()

    with col_comm2:
        st.markdown("### 📬 Feed de Estrategias Públicas")
        if not st.session_state['community_strategies']:
            st.info("💡 Aún no hay estrategias publicadas. ¡Sé el primero en compartir tu sabiduría!")
        else:
            for estr in st.session_state['community_strategies']:
                st.markdown(f"""
                <div class="strategy-card">
                    <div class="strategy-autor">👤 Autor: {estr['autor']}</div>
                    <div class="strategy-meta">Activo: {estr['activo']} | Categoría: {estr['categoria']} | Publicado: {estr['fecha']}</div>
                    <p>{estr['estrategia']}</p>
                </div>
                """, unsafe_allow_html=True)
