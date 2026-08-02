"""
Módulo de respaldo en Google Drive.

Streamlit Community Cloud borra el disco local del contenedor cada vez
que se reinicia (por inactividad, por un nuevo deploy o por
mantenimiento). Este módulo hace que el archivo asistencia.xlsx viva
también en un Google Drive personal, así que sin importar cuándo se
reinicie el contenedor, siempre se puede recuperar el histórico
completo.

Uso desde app.py:
    import drive_backup
    drive_backup.descargar_desde_drive(ARCHIVO_EXCEL)   # antes de leer
    drive_backup.subir_a_drive(ARCHIVO_EXCEL)            # después de guardar

Requiere 3 valores guardados en st.secrets (ver INSTRUCCIONES_GOOGLE_DRIVE.md):

    [google_drive]
    client_id = "..."
    client_secret = "..."
    refresh_token = "..."
"""

import io

import streamlit as st

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


NOMBRE_ARCHIVO_DRIVE = "asistencia.xlsx"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _credenciales_configuradas():
    return "google_drive" in st.secrets


def _obtener_credenciales():

    info = st.secrets["google_drive"]

    creds = Credentials(
        token=None,
        refresh_token=info["refresh_token"],
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )

    creds.refresh(Request())

    return creds


def _servicio_drive():

    creds = _obtener_credenciales()

    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _buscar_archivo_id(servicio):

    resultado = servicio.files().list(
        q=f"name='{NOMBRE_ARCHIVO_DRIVE}' and trashed=false",
        spaces="drive",
        fields="files(id, name, modifiedTime)",
        orderBy="modifiedTime desc",
    ).execute()

    archivos = resultado.get("files", [])

    return archivos[0]["id"] if archivos else None


def descargar_desde_drive(ruta_local):
    """Trae la copia más reciente desde Drive y la guarda en ruta_local,
    sobrescribiendo lo que haya localmente. Si todavía no existe nada
    en Drive (primera vez que corre la app), no hace nada: el archivo
    se creará localmente y se subirá la primera vez que se guarde algo.

    Devuelve True si logró sincronizar, False si hubo algún problema
    (en cuyo caso la app sigue funcionando con lo que tenga en disco
    local, para no tumbar el registro de asistencia de un estudiante)."""

    if not _credenciales_configuradas():
        st.sidebar.warning(
            "⚠️ Respaldo en Google Drive no configurado "
            "(faltan las credenciales en Secrets)."
        )
        return False

    try:
        servicio = _servicio_drive()
        archivo_id = _buscar_archivo_id(servicio)

        if archivo_id is None:
            return False

        request = servicio.files().get_media(fileId=archivo_id)
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)

        listo = False
        while not listo:
            _, listo = downloader.next_chunk()

        with open(ruta_local, "wb") as f:
            f.write(buffer.getvalue())

        return True

    except Exception as e:
        st.sidebar.warning(f"⚠️ No se pudo sincronizar desde Google Drive: {e}")
        return False


def subir_a_drive(ruta_local):
    """Sube (crea la primera vez, actualiza las siguientes) el archivo
    local a Google Drive. Se llama justo después de cada wb.save(...)."""

    if not _credenciales_configuradas():
        return False

    try:
        servicio = _servicio_drive()
        archivo_id = _buscar_archivo_id(servicio)

        media = MediaFileUpload(
            ruta_local,
            mimetype=(
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            ),
            resumable=True,
        )

        if archivo_id:
            servicio.files().update(fileId=archivo_id, media_body=media).execute()
        else:
            metadata = {"name": NOMBRE_ARCHIVO_DRIVE}
            servicio.files().create(
                body=metadata, media_body=media, fields="id"
            ).execute()

        return True

    except Exception as e:
        st.sidebar.warning(f"⚠️ No se pudo respaldar en Google Drive: {e}")
        return False
