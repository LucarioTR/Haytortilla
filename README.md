# Haytortilla
## ✈️ Sistema de Gestión y Filtro de Reservas ##
Sistema para y por la Gestión de la empresa **AirTortilla España** que permite leer un archivo CSV de reservas, identificar y agrupar automáticamente a los pasajeros mediante un localizador (PNR), y distribuir los resultados en archivos independientes filtrados por el **país de destino** y la **fecha de la reserva**.
## 📌 Requisitos y Especificaciones

1. **Campos obligatorios del CSV:** `id_reserva`, `origen`, `destino`, `pais_destino_iata`, `nombre_pasajero`, `fecha_reserva`.
2. **Identificación Inequívoca y Localizador (PNR):**
   * Cada reserva cuenta con su `id_reserva` único.
   * Si 2 o más pasajeros coinciden exactamente en **Nombre + Origen + Destino**, se les asigna un mismo **Localizador (PNR de 6 caracteres alfanuméricos)**.
3. **Formato de Salida:**
   * Archivos nombrados bajo el estándar: `AirTortilla_XX_YYYY_MM_DD.csv`
     * `XX`: Código IATA de 2 letras del país de destino (ej. `ES`, `FR`, `GB`, `US`).
     * `YYYY_MM_DD`: Fecha de realización de la reserva.
4. **Modalidades de Ejecución:**
   * **Total (Lote/Batch):** Procesa todo el archivo y genera de golpe todos los CSV agrupados.
   * **Línea a Línea (Streaming):** Procesa e incrementa los archivos iterativamente registro por registro.

---

## 🚀 Instalación y Requisitos

* **Python 3.8+**
* Sin dependencias externas pesadas (utiliza módulos nativos de Python: `csv`, `hashlib`, `collections`, `dataclasses`).

```bash
# Clonar el repositorio
git clone [https://github.com/LucarioTR/airtortilla-reservas.git](https://github.com/LucarioTR/airtortilla-reservas.git)
cd airtortilla-reservas