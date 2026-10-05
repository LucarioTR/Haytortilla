import csv
import hashlib
from collections import defaultdict
from dataclasses import dataclass

def generar_pnr(texto: str) -> str:
    """Crea un localizador alfanumérico único de 6 caracteres."""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()[:6].upper()

@dataclass
class Reserva:
    id_reserva: str
    origen: str
    destino: str
    pais_destino: str
    pasajero: str
    fecha: str
    pnr: str = ""

    @property
    def clave(self) -> str:
        """Clave para identificar pasajeros coincidentes."""
        return f"{self.pasajero.strip().lower()}|{self.origen.strip().upper()}|{self.destino.strip().upper()}"

class AirTortillaProcessor:
    def __init__(self, archivo_csv: str):
        self.archivo_csv = archivo_csv

    def _obtener_conteos(self) -> dict:
        """Cuenta las ocurrencias de cada combinación Nombre+Origen+Destino."""
        conteos = defaultdict(int)
        with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                clave = f"{row['nombre_pasajero'].strip().lower()}|{row['origen'].strip().upper()}|{row['destino'].strip().upper()}"
                conteos[clave] += 1
        return conteos

    def _crear_reserva(self, row: dict, conteos: dict) -> Reserva:
        """Construye el objeto Reserva asignando el PNR correcto."""
        r = Reserva(
            id_reserva=row['id_reserva'],
            origen=row['origen'],
            destino=row['destino'],
            pais_destino=row['pais_destino_iata'],
            pasajero=row['nombre_pasajero'],
            fecha=row['fecha_reserva']
        )
        # Si coincide 2 o más veces, comparten PNR. Si no, PNR único por id_reserva.
        r.pnr = generar_pnr(r.clave) if conteos[r.clave] >= 2 else generar_pnr(f"{r.clave}|{r.id_reserva}")
        return r

    def procesar_total(self):
        """Modalidad 1: Procesamiento en lote (guarda todos los ficheros de salida)."""
        conteos = self._obtener_conteos()
        agrupados = defaultdict(list)

        with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                r = self._crear_reserva(row, conteos)
                fecha_fmt = r.fecha.replace("-", "_")
                nombre_fichero = f"AirTortilla_{r.pais_destino.upper()}_{fecha_fmt}.csv"
                agrupados[nombre_fichero].append(r)

        # Escribir cada fichero agrupado por país y fecha
        for nombre_fichero, reservas in agrupados.items():
            with open(nombre_fichero, mode='w', newline='', encoding='utf-8') as f_out:
                writer = csv.writer(f_out)
                writer.writerow(['ID_Reserva', 'Localizador_PNR', 'Origen', 'Destino', 'Pasajero', 'Fecha'])
                for r in reservas:
                    writer.writerow([r.id_reserva, r.pnr, r.origen, r.destino, r.pasajero, r.fecha])
            print(f" Archivo generado: {nombre_fichero} ({len(reservas)} reservas)")

    def procesar_linea_a_linea(self):
        """Modalidad 2: Procesamiento en streaming (línea a línea)."""
        conteos = self._obtener_conteos()

        with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                r = self._crear_reserva(row, conteos)
                
                fecha_fmt = r.fecha.replace("-", "_")
                nombre_fichero = f"AirTortilla_{r.pais_destino.upper()}_{fecha_fmt}.csv"
                
                # Escribir/Anexar fila a fila
                existe = False
                try:
                    open(nombre_fichero, 'r').close()
                    existe = True
                except FileNotFoundError:
                    pass

                with open(nombre_fichero, mode='a', newline='', encoding='utf-8') as f_out:
                    writer = csv.writer(f_out)
                    if not existe:
                        writer.writerow(['ID_Reserva', 'Localizador_PNR', 'Origen', 'Destino', 'Pasajero', 'Fecha'])
                    writer.writerow([r.id_reserva, r.pnr, r.origen, r.destino, r.pasajero, r.fecha])
                
                yield r


# --- INTERFAZ POR CONSOLA (CLI) ---
if __name__ == "__main__":
    archivo = input("Ruta del archivo CSV [defecto: reservas_entrada.csv]: ").strip() or "reservas_entrada.csv"
    modo = input("Elige modo -> 1: Total (Lote) | 2: Línea a línea: ").strip()

    proc = AirTortillaProcessor(archivo)

    if modo == "1":
        print("\n--- Procesando en Total ---")
        proc.procesar_total()
    elif modo == "2":
        print("\n--- Procesando Línea a Línea ---")
        for i, res in enumerate(proc.procesar_linea_a_linea(), start=1):
            print(f"[{i}] {res.pasajero} -> {res.destino} ({res.pais_destino}) | PNR: {res.pnr}")
    else:
        print("Opción no válida.")