import os
import glob
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

# 1. Configuración de página
st.set_page_config(page_title="Tenaris - AI Vision", page_icon="🔴", layout="wide", initial_sidebar_state="expanded")

# 2. Rutas dinámicas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'runs/detect/mandrel_detector_v1/weights/best.pt')
MUESTRAS_DIR = os.path.join(BASE_DIR, 'webapp/muestras')
LOGO_PATH = os.path.join(BASE_DIR, 'webapp/photos/tenaris_logo.webp')

# 3. CSS Corporativo (Estilo web Tenaris: Blanco, Limpio, Acentos Rojos)
st.markdown("""
    <style>
    /* Ocultar menú de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tipografía y fondos */
    .main-header { font-size: 42px !important; font-weight: 700; color: #222222; margin-bottom: 0px; padding-bottom: 0px; letter-spacing: -0.5px; border-left: 6px solid #009CA6; padding-left: 15px;}
    .color-cyan { color: #009CA6; font-weight: 800; } 
    .color-purple { color: #7A3E93; font-weight: 800; } 
    .color-green { color: #8CC63F; font-weight: 800; } 
    .sub-header { font-size: 18px !important; color: #555555; font-weight: 400; margin-top: 10px; margin-bottom: 30px; padding-left: 21px;}
    
    /* Botones estilo Corporativo */
    div.stButton > button:first-child { 
        background-color: #FFFFFF; 
        color: #222222; 
        border: 1px solid #CCCCCC; 
        border-radius: 4px; 
        padding: 8px 24px; 
        font-weight: 600; 
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        border-color: #7A3E93;
        color: #7A3E93;
        background-color: #F9F0FA;
    }
    
    /* Cajas vacías */
    .empty-box {
        background-color: #F9F9F9;
        padding: 40px;
        border-radius: 4px;
        text-align: center;
        border: 1px dashed #CCCCCC;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

def evaluar_semaforo(boxes):
    peor_estado = "VERDE"
    if len(boxes) == 0: return peor_estado
    for box in boxes:
        conf = float(box.conf[0])
        w_norm, h_norm = float(box.xywhn[0][2]), float(box.xywhn[0][3])
        area_pct = w_norm * h_norm
        estado_actual = "AMARILLO"
        if conf >= 0.65 and area_pct >= 0.01:
            estado_actual = "ROJO"
        if estado_actual == "ROJO": peor_estado = "ROJO"
        elif estado_actual == "AMARILLO" and peor_estado != "ROJO": peor_estado = "AMARILLO"
    return peor_estado

def main():
    if 'img_to_analyze' not in st.session_state:
        st.session_state.img_to_analyze = None

    # -- SIDEBAR --
    with st.sidebar:
        # Cargar logo local de Tenaris
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        else:
            st.markdown("## TENARIS")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("### 📂 Galería de Pruebas")
        
        fotos = glob.glob(os.path.join(MUESTRAS_DIR, '*.*'))
        fotos = [f for f in fotos if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if len(fotos) == 0:
            st.info(f"📁 La galería está vacía.\n\nCopiá imágenes en:\n`{MUESTRAS_DIR}`")
        else:
            for i, foto_path in enumerate(fotos[:4]):
                st.image(foto_path, use_container_width=True)
                if st.button(f"Analizar Muestra {i+1}", key=f"btn_{i}"):
                    img = cv2.imread(foto_path)
                    st.session_state.img_to_analyze = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                st.write("---")
                
        st.write("### 📥 Carga Manual")
        uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img_bgr = cv2.imdecode(file_bytes, 1)
            st.session_state.img_to_analyze = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # -- MAIN --
    st.markdown('<p class="main-header">Línea de Mandriles <span class="color-cyan">|</span> <span class="color-purple">AI</span> <span class="color-green">Vision</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitoreo térmico automatizado para Mantenimiento Predictivo.</p>', unsafe_allow_html=True)
    
    model = load_model()

    if st.session_state.img_to_analyze is not None:
        img_rgb = st.session_state.img_to_analyze
        
        with st.spinner('Procesando (Latencia ultra-baja)...'):
            results = model.predict(img_rgb, conf=0.15, verbose=False)
            
        for r in results:
            estado = evaluar_semaforo(r.boxes)
            im_out = r.plot()
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Cámara Infrarroja (Original)**")
            st.image(img_rgb, use_container_width=True)
        with col2:
            st.markdown("**Motor de Inferencia (YOLOv8)**")
            st.image(im_out, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Cajas de estado corporativas
        if estado == "VERDE":
            st.success("#### 🟢 ESTADO: APTO PARA PRODUCCIÓN \nIntegridad estructural verificada. El ciclo de laminación continúa activo.")
        elif estado == "AMARILLO":
            st.warning("#### 🟡 ESTADO: REVISIÓN HUMANA REQUERIDA \nAnomalía detectada. Desviación a estación de inspección visual.")
        elif estado == "ROJO":
            st.error("#### 🔴 ESTADO: CRÍTICO (DESCARTAR PIEZA) \nFalla severa confirmada. Señal enviada a PLC para recambio de herramienta.")
    else:
        # Estado inicial vacío
        st.markdown("""
        <div class="empty-box">
            <h3 style="color: #666;">Esperando señal de cámara...</h3>
            <p style="color: #888;">Seleccione una imagen del panel lateral o suba un archivo manual para iniciar la inspección de IA.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

