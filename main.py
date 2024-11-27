from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


import base64

app = FastAPI()

# Declarar pdf_store como variable global
pdf_store = {}

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto según el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Modelo para los datos del PDF
class PDFData(BaseModel):
    nombre: str
    apellido: str
    edad: str
    telefono: str
    correo: str

# Endpoint para crear el PDF
@app.post("/create")
async def create_pdf(data: PDFData):
    try:
        # Generar un código único para identificar el PDF
        document_code = str(uuid4())[:10].upper()

        # Crear el PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        # Obtener ancho y alto de la página
        width, height = letter

        # Agregar el título centrado
        title = "Chelita Software - Fullstack Test"
        c.setFont("Helvetica-Bold", 16)  # Fuente y tamaño
        c.drawCentredString(width / 2, height - 50, title)  # Centrado en la parte superior

        # Agregar los datos del formulario
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 100, f"Nombre: {data.nombre}")
        c.drawString(100, height - 120, f"Apellido: {data.apellido}")
        c.drawString(100, height - 140, f"Edad: {data.edad}")
        c.drawString(100, height - 160, f"Teléfono: {data.telefono}")
        c.drawString(100, height - 180, f"Correo: {data.correo}")

        # Finalizar y guardar el PDF en memoria
        c.save()
        buffer.seek(0)
        pdf_store[document_code] = buffer.read()

        return {"success": True, "document_code": document_code}
    except Exception as e:
        # Capturar cualquier excepción y devolver un error HTTP
        raise HTTPException(status_code=500, detail=f"Error al crear el PDF: {str(e)}")
    
    
# Endpoint para obtener el PDF en Base64
@app.get("/document/{code}")
async def get_pdf(code: str):
    # Verificar si el código existe en pdf_store
    if code in pdf_store:
        pdf_bytes = pdf_store[code]
        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        return {"success": True, "document_b64": pdf_b64}
    return {"success": False, "message": "Documento no encontrado"}