# Estado del Arte: IA e Inspección en la Industria Siderúrgica (Tubos sin Costura)

Este documento resume las tecnologías actuales, competidores y soluciones aplicables para la inspección de herramientas (mandriles) y detección de defectos en tubos de acero sin costura a altas temperaturas.

## 1. Tecnologías Aplicables para Inspección Proactiva
Para inspeccionar un mandril de forma automatizada y proactiva, sorteando los problemas de alta temperatura y ambiente adverso (polvo, vibración), la industria emplea:

*   **Perfilometría Láser 3D (Triangulación):** Es el estándar de oro. Escáneres láser de alta velocidad proyectan una línea sobre el mandril y construyen un mapa topográfico 3D (nube de puntos) capaz de detectar rayaduras y deformaciones geométricas de escala milimétrica. Marcas como Keyence o Cognex proveen equipos con carcasas de enfriamiento industrial.
*   **Visión Computacional Infrarroja y Filtros de Banda (Bandpass):** A 1200°C el metal emite luz visible e infrarroja extrema. Para usar cámaras convencionales, se utilizan filtros de paso de banda que bloquean la radiación del calor y dejan pasar únicamente la frecuencia de una iluminación láser dedicada (ej. luz azul o verde de alta intensidad), permitiendo ver la textura de la superficie y el polvo adherido.
*   **Termografía Activa:** Al salir del laminador, el mandril se enfría. Las grietas internas o la rugosidad superficial extrema alteran la forma en la que se disipa el calor. Las cámaras térmicas pueden detectar estos "puntos fríos/calientes" microscópicos como anomalías antes de que haya un daño evidente a nivel visual.

## 2. Tecnologías de Inspección en el Tubo (Tiempo Real)
Aunque el objetivo es el mandril, la detección en el tubo apenas sale del laminador también ha evolucionado:
*   **EMAT (Ultrasonido Electromagnético):** Permite inspeccionar el espesor y defectos internos de los tubos sin necesidad de líquido acoplante, operando sobre metales a más de 600°C.
*   **Sistemas de Corrientes Inducidas (Eddy Current):** Muy utilizados a la salida de las líneas en caliente para detectar defectos superficiales.

## 3. Panorama Competitivo y Referentes de la Industria
*   **Vallourec:** Principal competidor de Tenaris. Han invertido masivamente en Industria 4.0 implementando gemelos digitales (Digital Twins) de sus laminadores y trazabilidad de activos. Usan IA para predecir el desgaste de herramentales basándose en la fricción y temperaturas registradas.
*   **SMS Group / Danieli:** Proveedores líderes de maquinaria siderúrgica. Ya comercializan módulos de plantas inteligentes (ej. sistema CARTA) que integran la lectura láser de las herramientas de laminación y el ajuste dinámico en tiempo real.
*   **Nippon Steel:** Pioneros en aplicar Edge AI (Inteligencia Artificial en el borde) para analizar terabytes de datos de sensores en sus procesos de perforación y laminación. Esto les permite alertar sobre posibles defectos en tiempo real.

## 4. Estrategia Sugerida de Solución para Tenaris
Para lograr el "desperdicio 0" abordando el problema del mandril, se propone la siguiente arquitectura:
1.  **Trazabilidad Unívoca:** Identificación de cada mandril mediante marcas láser o tags RFID para alta temperatura.
2.  **Estación de Escaneo "Al Vuelo":** Aprovechar el transporte mediante grúas para pasar el mandril por un arco de perfilometría 3D sin detener el proceso (integración en el *Takt Time*).
3.  **Gemelo Digital y Machine Learning:** La nube de puntos generada se compara en tiempo real con el CAD original (modelo perfecto). Una red neuronal entrenada con los defectos históricos determina si la rugosidad/rayado supera el umbral crítico.
4.  **Alerta Automatizada:** El sistema se integra con el SCADA y emite una alerta o bloqueo para evitar que ese mandril vuelva a ingresar al horno, enviándolo directamente a rectificación.

