# Raven Developers by Grupo AISA 
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import base64
import datetime
import os
import time
import threading
from cfdiclient import Autenticacion, DescargaMasiva, Fiel, SolicitaDescarga, VerificaSolicitudDescarga
import logging
from tkcalendar import DateEntry  

#Clase que representa la interfaz gráfica de usuario (GUI)
class CFDIDownloaderGUI:

    #Inicializa una instancia de la clase
    def __init__(self, root):
        self.root = root # Ventana principal
        self.root.title("CFDI Manager") # Título de la ventana
        self.root.geometry("899x650")  # Restore original window size

        # Variables de control
        self.is_downloading = False 
        self.current_thread = None 

        # Configurar logging
        self.setup_logging()

        # Crear marco principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)

        # Columna izquierda para campos de entrada
        input_column_frame = ttk.Frame(main_frame)
        input_column_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # RFC
        ttk.Label(input_column_frame, text="RFC:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.rfc_entry = ttk.Entry(input_column_frame, width=35)
        self.rfc_entry.grid(row=0, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))

        # Archivo CER
        ttk.Label(input_column_frame, text="Archivo CER (.cer):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cer_entry = ttk.Entry(input_column_frame, width=35)
        self.cer_entry.grid(row=1, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(input_column_frame, text="Examinar", width=10, command=self.browse_cer).grid(row=1, column=2, padx=5, pady=2)

        # Archivo KEY
        ttk.Label(input_column_frame, text="Archivo KEY (.key):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.key_entry = ttk.Entry(input_column_frame, width=35)
        self.key_entry.grid(row=2, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(input_column_frame, text="Examinar", width=10, command=self.browse_key).grid(row=2, column=2, padx=5, pady=2)

        # Contraseña
        ttk.Label(input_column_frame, text="Contraseña:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.password_entry = ttk.Entry(input_column_frame, width=35, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))

        # Carpeta de Descarga
        ttk.Label(input_column_frame, text="Carpeta de Descarga:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.download_dir_entry = ttk.Entry(input_column_frame, width=35)
        self.download_dir_entry.grid(row=4, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(input_column_frame, text="Examinar", width=10, command=self.browse_download_dir).grid(row=4, column=2, padx=5, pady=2)

        # Tipo de Descarga
        ttk.Label(input_column_frame, text="Tipo de Descarga:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.download_type_combobox = ttk.Combobox(input_column_frame, width=32, state="readonly")
        self.download_type_combobox['values'] = ("Emitidos", "Recibidos")
        self.download_type_combobox.grid(row=5, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        self.download_type_combobox.current(0)

        # Marco de Fechas con Calendario
        date_frame = ttk.LabelFrame(main_frame, text="Establezca un rango de fechas para la descarga", padding="5")
        date_frame.grid(row=0, column=3, rowspan=2, padx=20, sticky=(tk.N, tk.S, tk.E, tk.W))
        date_frame.columnconfigure(0, weight=1)

        ttk.Label(date_frame, text="Fecha Inicial").grid(row=0, column=0, pady=2, sticky=tk.W)
        self.start_date_entry = DateEntry(date_frame, width=20, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=1, column=0, pady=2, padx=5, sticky=tk.W)

        ttk.Label(date_frame, text="Fecha Final").grid(row=2, column=0, pady=2, sticky=tk.W)
        self.end_date_entry = DateEntry(date_frame, width=20, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=3, column=0, pady=2, padx=5, sticky=tk.W)

        # Área de Procesos
        ttk.Label(main_frame, text="Registro de Procesos:").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.process_text = scrolledtext.ScrolledText(main_frame, width=70, height=15, state='disabled')
        self.process_text.grid(row=7, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))

        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=3, pady=10, sticky=tk.E)
        self.download_btn = ttk.Button(button_frame, text="Ejecutar Descarga", command=self.start_download)
        self.download_btn.grid(row=0, column=0, padx=5, pady=5)
        self.clear_btn = ttk.Button(button_frame, text="Limpiar Log", command=self.clear_log)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5)
        self.clear_fields_btn = ttk.Button(button_frame, text="Limpiar Campos", command=self.clear_fields)
        self.clear_fields_btn.grid(row=2, column=0, padx=5, pady=5)

        # Etiqueta del desarrollador
        ttk.Label(main_frame, text="Ravens Developers by Grupo AISA").grid(row=9, column=0, columnspan=5, pady=10, sticky=tk.W)

    def setup_logging(self):
        logging.basicConfig(
            filename='cfdi_downloader.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    # *Funciones de los botones
    # *browse_cer: Abre un cuadro de diálogo para seleccionar un archivo CER
    def browse_cer(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos CER", "*.cer")])
        if filename:
            self.cer_entry.delete(0, tk.END)
            self.cer_entry.insert(0, filename)

    # *browse_key: Abre un cuadro de diálogo para seleccionar un archivo KEY
    def browse_key(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos KEY", "*.key")])
        if filename:
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, filename)

    # *browse_download_dir: Abre un cuadro de diálogo para seleccionar una carpeta de descarga
    def browse_download_dir(self):
        directory = filedialog.askdirectory(title="Seleccionar Carpeta de Descarga")
        if directory:
            self.download_dir_entry.delete(0, tk.END)
            self.download_dir_entry.insert(0, directory)

    # *clear_log: Limpia el área de texto de procesos
    def clear_log(self):
        self.process_text.configure(state='normal')
        self.process_text.delete(1.0, tk.END)
        self.process_text.configure(state='disabled')

    # *log_process: Registra un mensaje en el área de texto de procesos y en el archivo de log
    def log_process(self, message):
        self.process_text.configure(state='normal')
        self.process_text.insert(tk.END, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        self.process_text.see(tk.END)
        self.process_text.configure(state='disabled')
        logging.info(message)

    # *validate_inputs: Valida que los campos obligatorios estén completos y que las fechas sean válidas
    def validate_inputs(self):
        required_fields = {
            'RFC': self.rfc_entry.get(),
            'Archivo CER': self.cer_entry.get(),
            'Archivo KEY': self.key_entry.get(),
            'Contraseña': self.password_entry.get(),
            'Fecha Inicial': self.start_date_entry.get(),
            'Fecha Final': self.end_date_entry.get()
        }
        for field, value in required_fields.items():
            if not value.strip():
                self.log_process(f"Error: El campo {field} es obligatorio")
                return False
        try:
            fecha_inicial = datetime.datetime.strptime(self.start_date_entry.get(), '%Y-%m-%d')
            fecha_final = datetime.datetime.strptime(self.end_date_entry.get(), '%Y-%m-%d')
            if fecha_final < fecha_inicial:
                self.log_process("Error: La fecha final no puede ser menor que la fecha inicial")
                return False
        except ValueError:
            self.log_process("Error: Formato de fecha inválido. Use YYYY-MM-DD")
            return False
        return True

    # *start_download: Inicia el proceso de descarga en un hilo separado
    def start_download(self):
        if self.is_downloading:
            self.log_process("Ya hay una descarga en proceso")
            return
        if not self.validate_inputs():
            return
        self.is_downloading = True
        self.download_btn.configure(state='disabled')
        threading.Thread(target=self.download_process, daemon=True).start()

    # *download_process: Proceso de descarga de CFDIs
    def download_process(self):
        #todo NOTA: estos son los errores o estados que puede devolver el proceso de descarga
        #! 0, Token invalido.
        #! 1, Aceptada
        #! 2, En proceso
        #! 3, Terminada
        #! 4, Error
        #! 5, Rechazada
        #! 6, Vencida
        try:
            rfc = self.rfc_entry.get()
            cer_path = self.cer_entry.get()
            key_path = self.key_entry.get()
            password = self.password_entry.get()
            download_dir = self.download_dir_entry.get()
            if not download_dir:
                download_dir = os.getcwd()
                self.log_process("No se seleccionó carpeta de descarga. Usando directorio actual.")
            os.makedirs(download_dir, exist_ok=True)
            cer_der = open(cer_path, 'rb').read()
            key_der = open(key_path, 'rb').read()

            self.log_process("Iniciando proceso de descarga...")
            fiel = Fiel(cer_der, key_der, password)
            auth = Autenticacion(fiel)
            token = auth.obtener_token()
            self.log_process("Token obtenido exitosamente")

            descarga = SolicitaDescarga(fiel)
            fecha_inicial = datetime.datetime.strptime(self.start_date_entry.get(), '%Y-%m-%d').date()
            fecha_final = datetime.datetime.strptime(self.end_date_entry.get(), '%Y-%m-%d').date()

            tipo_descarga = self.download_type_combobox.get()
            if tipo_descarga == "Emitidos":
                solicitud = descarga.solicitar_descarga(
                    token, rfc, fecha_inicial, fecha_final, rfc_emisor=rfc, tipo_solicitud='CFDI'
                )
            else:
                solicitud = descarga.solicitar_descarga(
                    token, rfc, fecha_inicial, fecha_final, rfc_receptor=rfc, tipo_solicitud='CFDI'
                )

            self.log_process(f"Solicitud creada exitosamente: {solicitud['id_solicitud']}")
            
            while True:
                token = auth.obtener_token()
                verificacion = VerificaSolicitudDescarga(fiel)
                verificacion = verificacion.verificar_descarga(token, rfc, solicitud['id_solicitud'])
                estado_solicitud = int(verificacion['estado_solicitud'])
                self.log_process(f"Estado de solicitud: {estado_solicitud}")

                if estado_solicitud <= 2:
                    self.log_process("En proceso, esperando 60 segundos...")
                    time.sleep(60)
                    continue
                elif estado_solicitud == 3:
                    self.log_process("Descarga completada")
                    # Procesamos los paquetes cuando el estado es 3 (Terminada)
                    if 'paquetes' in verificacion and verificacion['paquetes']:
                        for paquete in verificacion['paquetes']:
                            descarga = DescargaMasiva(fiel)
                            descarga_paquete = descarga.descargar_paquete(token, rfc, paquete)
                            filename = os.path.join(download_dir, f'{paquete}.zip')
                            with open(filename, 'wb') as fp:
                                fp.write(base64.b64decode(descarga_paquete['paquete_b64']))
                            self.log_process(f"Paquete descargado en: {filename}")
                    else:
                        self.log_process("No se encontraron paquetes para descargar")
                    break
                elif estado_solicitud == 4:
                    self.log_process("Error en la solicitud")
                    break
                elif estado_solicitud == 5:
                    self.log_process("Solicitud rechazada o no encuentra CFDIs")
                    break
                elif estado_solicitud == 6:
                    self.log_process("Solicitud vencida")
                    break
                else:
                    self.log_process(f"Estado desconocido: {estado_solicitud}")
                    break
                
            self.log_process("Proceso completado.")
        except Exception as e:
            self.log_process(f"Error: {str(e)}")
        finally:
            self.is_downloading = False
            self.download_btn.configure(state='normal')

    # *clear_fields: Limpia los campos de entrada
    def clear_fields(self):
        self.rfc_entry.delete(0, tk.END)
        self.cer_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.download_dir_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.log_process("Todos los campos han sido limpiados")

# *Función principal
if __name__ == "__main__":
    # Crear ventana principal
    root = tk.Tk()
    try:
        # Obtiene la ruta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "icon.ico")
        root.iconbitmap(icon_path)
    except tk.TclError:
        pass
    app = CFDIDownloaderGUI(root)
    root.mainloop()
