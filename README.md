# cfdi-descarga-masiva-de-xml
 La aplicación automatiza el proceso de autenticación, solicitud de descarga y verificación del estado de la solicitud, permitiendo al usuario descargar los CFDI emitidos o recibidos en un rango de fechas específico.

## Descripción

Este proyecto es una aplicación de escritorio desarrollada en Python utilizando la librería Tkinter. Está diseñada para facilitar la descarga masiva de Comprobantes Fiscales Digitales por Internet (CFDI) desde el Servicio de Administración Tributaria (SAT) de México. La aplicación automatiza el proceso de autenticación, solicitud de descarga y verificación del estado de la solicitud, permitiendo al usuario descargar los CFDI emitidos o recibidos en un rango de fechas específico.



## Instalación

Simplemente haga doble clic en el archivo CFDI_Manager.exe (o el nombre del ejecutable) para ejecutar la aplicación



## Uso

Para utilizar CFDI Manager, sigue estos pasos:

1.  **RFC del Contribuyente:** Ingresa tu Registro Federal de Contribuyentes (RFC) en el campo correspondiente.

2.  **Archivos CER y KEY:**
    *   Selecciona los archivos `.cer` y `.key` de tu FIEL.
    *   Utiliza los botones "Examinar" para buscar los archivos en tu computadora.
    *   **Importante:** Asegúrate de mantener estos archivos en un lugar seguro, ya que son críticos para la autenticación.

3.  **Contraseña de la FIEL:** Ingresa la contraseña de tu FIEL.

4.  **Carpeta de Descarga:** Selecciona la carpeta donde se guardarán los archivos ZIP con los CFDI descargados.

5.  **Tipo de Descarga:**
    *   Selecciona "Emitidos" para descargar los CFDI que tú has emitido.
    *   Selecciona "Recibidos" para descargar los CFDI que has recibido.

6.  **Rango de Fechas:**
    *   Ingresa la fecha de inicio y la fecha final del rango de fechas para la descarga.
    *   El formato debe ser YYYY-MM-DD (Ejemplo: 2023-10-26).

7.  **Iniciar Descarga:** Haz clic en el botón "Ejecutar Descarga" para iniciar el proceso.

8.  **Registro de Procesos:** El área de registro mostrará mensajes sobre el progreso de la descarga y los posibles errores.

9.  **Limpiar:**
    *   Haz clic en "Limpiar Log" para borrar el registro de procesos.
    *   Haz clic en "Limpiar Campos" para borrar los campos de entrada.


# Guía para Contribuidores - Descargador de CFDI



¡Gracias por tu interés en contribuir al proyecto del Descargador de CFDI! Tu ayuda es valiosa para mejorar esta herramienta.



## ¿Cómo puedo contribuir?



Hay varias maneras en las que puedes contribuir:



### Reportar errores (Bugs)



* Utiliza el sistema de seguimiento de errores (Issues) de GitHub (si el proyecto está alojado ahí) para reportar bugs. Si no hay un repositorio público, contacta a los mantenedores directamente.

* Por favor, proporciona la siguiente información al reportar un error:



* **Título del error:** Descriptivo y conciso.

* **Descripción detallada:** Explica el problema claramente.

* **Pasos para reproducir:** Lista los pasos necesarios para que otros puedan reproducir el error.

* **Comportamiento esperado vs. real:** Describe qué debería pasar y qué está pasando en realidad.

* **Información del entorno:** Sistema operativo, versión de Python, versiones de las dependencias (incluyendo `cfdiclient`).

* **Capturas de pantalla:** Si son útiles para ilustrar el error.



### Sugerir mejoras (Features)



* Utiliza el sistema de seguimiento de errores (Issues) de GitHub (o similar) para sugerir nuevas funcionalidades o mejoras.

* Describe claramente la mejora propuesta y su justificación. Explica cómo beneficiaría a los usuarios.



### Contribuir con código



1. **Fork del repositorio:** Haz un "fork" del repositorio en GitHub (si aplica).



2. **Creación de una rama (Branch):** Crea una nueva rama para tu trabajo. Usa un nombre descriptivo (ej: `feature/nueva-funcionalidad`, `bugfix/correccion-error`).



3. **Desarrollo del código:**



* **Estilo de código:** Sigue las convenciones de estilo de código de Python (PEP 8). Utiliza un linter como `flake8` o `pylint` para verificar tu código.

* **Documentación:** Documenta tu código usando docstrings. Asegúrate de que las funciones, clases y módulos estén bien documentados.

* **Pruebas:** Escribe pruebas unitarias para tu código. Utiliza el módulo `unittest` o `pytest` de Python. Asegúrate de que las pruebas cubran los casos importantes y que pasen todas las pruebas antes de enviar tu código.



4. **Commit de los cambios:** Haz commits pequeños y descriptivos. Usa mensajes de commit claros y concisos que expliquen qué has cambiado. (Ejemplo: "Fix: Corregido error de formato de fecha en la descarga").



5. **Push de la rama:** Sube tu rama a tu repositorio fork.



6. **Creación de un Pull Request (PR):** Abre un Pull Request (PR) contra la rama principal (`main` o `master`) del repositorio original. Describe los cambios que has realizado en el PR.



7. **Revisión del código:** Tu código será revisado por los mantenedores del proyecto. Responde a los comentarios y realiza los cambios necesarios.



8. **Merge del PR:** Una vez que la revisión sea satisfactoria, tu PR será mergeado al repositorio principal.



### Contribuir con documentación



* Si encuentras errores en la documentación o quieres agregar información, puedes enviar un PR con los cambios.



## Licencia

MIT License



Copyright (c) 2025 Ravens Developers by Grupo AISA



Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.
