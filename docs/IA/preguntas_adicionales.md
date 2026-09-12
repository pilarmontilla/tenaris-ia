# Preguntas Estratégicas y Técnicas - Inspección de Mandriles (Tenaris)

A continuación se presenta una batería de preguntas diseñadas para relevar información crítica del staff técnico de Tenaris, con el objetivo de transicionar de un control de calidad reactivo a uno proactivo.

## Viabilidad Técnica
1. **Condiciones Ambientales:** ¿Cuáles son las limitaciones físicas y térmicas (temperatura, vibraciones, polvo suspendido) en la zona donde la grúa transporta o reposa el mandril para la potencial instalación de sensores ópticos o láser?
2. **Escaneo Óptico:** ¿Se ha evaluado previamente el uso de perfilometría láser 3D o visión computacional con cámaras multiespectrales para escanear la topografía del mandril durante su ciclo de transporte sin detener la producción?
3. **Mapeo Térmico y Desgaste:** Dado que el mandril sufre altísima fricción, ¿existe un mapeo conocido que indique en qué zonas específicas (punta, cuerpo medio) ocurren las fallas críticas que luego impactan la cara interna del tubo?
4. **Interferencias Físicas:** El polvo adherido genera errores. ¿Existe actualmente algún sistema de limpieza o soplado automatizado del mandril antes de su uso? ¿Podría integrarse la inspección inmediatamente después de esa limpieza?

## Infraestructura y Datos
5. **Trazabilidad:** ¿Existe actualmente un sistema de identificación (RFID de alta temperatura, códigos grabados, OCR) que permita identificar unívocamente a cada mandril para trazar su historial y vida útil?
6. **Correlación de Datos:** Los defectos se detectan hoy en día al final mediante cámaras de calor. ¿Se cuenta con ese dataset histórico digitalizado para entrenar un modelo de Machine Learning que correlacione el desgaste de un mandril específico con el defecto resultante en el tubo?
7. **Edge Computing:** ¿Con qué infraestructura de red e informática (latencia, servidores locales en planta) cuenta el área del laminador para procesar nubes de puntos 3D o imágenes de alta resolución en tiempo real?
8. **Integración con Sistemas:** ¿Qué sistemas MES/SCADA manejan y qué tan factible es automatizar una alerta que impida sistémicamente el uso de un mandril que el algoritmo haya detectado como defectuoso?

## Proceso
9. **Tiempos Muertos (Takt Time):** ¿Cuál es el tiempo exacto en el que el mandril está "al aire" o en reposo entre una pasada y otra, que podríamos aprovechar para un escaneo automatizado "al vuelo"?
10. **Ventanas de Mantenimiento:** Sabiendo que los domingos no se lamina, ¿se podría aprovechar esa ventana de 24 horas para realizar calibraciones automáticas del sistema de visión o escaneos profundos del stock de mandriles?
11. **Toma de Decisión Actual:** ¿Cuál es el proceso heurístico del operario hoy? ¿Qué características visuales exactas (rugosidad, color, profundidad de surcos) busca para determinar si un mandril se descarta o re-utiliza?
12. **Lubricación:** ¿El mandril recibe algún tratamiento o lubricación (ej. grafito) entre pasadas que pueda generar falsos positivos al intentar visualizar su superficie metálica directamente?

## Viabilidad Económica
13. **Impacto del Desperdicio:** Con una tasa de 5% a 10% de defectos actuales, ¿cuál es el costo promedio anualizado de este scrap (o retrabajo) para poder justificar y dimensionar el ROI del sistema de IA?
14. **CAPEX de Implementación:** ¿Considerarían más viable financieramente una solución basada en cámaras fijas monitorizando el trayecto de las grúas (menor impacto de instalación) o un pórtico/túnel de escaneo dedicado en una estación de reposo?
15. **Costos de Herramental:** ¿Cuál es el costo unitario de cada mandril y cómo se compara su vida útil real actual frente a la vida útil teórica que se podría alcanzar con mantenimiento predictivo?

