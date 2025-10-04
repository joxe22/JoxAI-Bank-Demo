# Guía: Ejecutar JoxAI Banking Chatbot en Visual Studio Code

Esta guía te ayudará a configurar y ejecutar el proyecto completo en Visual Studio Code.

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

- **Python 3.11+** - [Descargar](https://www.python.org/downloads/)
- **Node.js 18+** y npm - [Descargar](https://nodejs.org/)
- **Visual Studio Code** - [Descargar](https://code.visualstudio.com/)
- **Git** - [Descargar](https://git-scm.com/)

### Verificar instalación:
```bash
python --version   # Python 3.11 o superior
node --version     # v18 o superior
npm --version      # 9.0 o superior
git --version      # 2.0 o superior
```

---

## 🚀 Instalación Inicial

### 1. Clonar el Repositorio

```bash
git clone https://github.com/joxe22/JoxAI-Bank-Demo.git
cd JoxAI-Bank-Demo
```

### 2. Abrir en VS Code

```bash
code .
```

O desde VS Code: `File > Open Folder` → Selecciona la carpeta del proyecto

---

## 🐍 Configuración del Backend (FastAPI)

### 1. Crear Entorno Virtual de Python

**En Windows:**
```bash
cd banking_chatbot/backend
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
cd banking_chatbot/backend
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` en tu terminal.

### 2. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

Esto instalará:
- FastAPI
- Uvicorn
- Pydantic
- Python-Jose (JWT)
- Passlib
- SQLAlchemy
- Y otras dependencias necesarias

### 3. Verificar Instalación

```bash
python -c "import fastapi; print('✓ FastAPI instalado correctamente')"
```

---

## ⚛️ Configuración del Frontend (React)

### 1. Instalar Dependencias de Node.js

```bash
cd ../../banking_chatbot/frontend/admin-panel
npm install
```

Esto instalará:
- React
- React Router
- Vite
- Y otras dependencias del frontend

### 2. Verificar Instalación

```bash
npm list react react-dom
```

---

## 🎯 Ejecutar el Proyecto

Necesitarás **DOS terminales** abiertas en VS Code.

### Terminal 1: Backend (FastAPI)

```bash
cd banking_chatbot/backend
source venv/bin/activate  # En Windows: venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **Deberías ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

🌐 **Prueba el API:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Widget Demo: http://localhost:8000/widget-demo

### Terminal 2: Frontend (React + Vite)

```bash
cd banking_chatbot/frontend/admin-panel
npm run dev
```

✅ **Deberías ver:**
```
VITE v7.x.x ready in XXX ms
Local: http://localhost:5173/
```

🌐 **Abre el Admin Panel:**
- Admin Panel: http://localhost:5173/

---

## 🔑 Credenciales de Acceso

Una vez que la aplicación esté corriendo:

**Admin Panel (http://localhost:5173/)**
- **Admin**: admin@joxai.com / admin123
- **Supervisor**: supervisor@joxai.com / admin123
- **Agente**: agent@joxai.com / admin123

---

## 🛠️ Configuración Avanzada en VS Code

### Extensiones Recomendadas

Instala estas extensiones en VS Code:

1. **Python** (ms-python.python)
2. **Pylance** (ms-python.vscode-pylance)
3. **ESLint** (dbaeumer.vscode-eslint)
4. **Prettier** (esbenp.prettier-vscode)
5. **Thunder Client** (rangav.vscode-thunder-client) - Para probar el API

### Configuración de Debug

Crea `.vscode/launch.json` en la raíz del proyecto:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI Backend",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/banking_chatbot/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/banking_chatbot/backend"
      },
      "console": "integratedTerminal"
    },
    {
      "name": "Launch Chrome for React",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/banking_chatbot/frontend/admin-panel/src"
    }
  ],
  "compounds": [
    {
      "name": "Full Stack Debug",
      "configurations": [
        "Python: FastAPI Backend",
        "Launch Chrome for React"
      ]
    }
  ]
}
```

### Abrir Múltiples Terminales en VS Code

1. Abre terminal: `Ctrl + ` `` (backtick) o `View > Terminal`
2. Divide terminal: Click en el ícono de split (⊞) o `Ctrl + Shift + 5`
3. Terminal izquierda → Backend
4. Terminal derecha → Frontend

---

## 📊 Datos de Demo

Para poblar la base de datos con datos de prueba:

```bash
curl -X POST http://localhost:8000/api/v1/demo/populate-demo-data
```

Esto creará:
- 5 conversaciones de ejemplo
- 3 tickets escalados
- Mensajes de conversación

**Para limpiar los datos:**
```bash
curl -X POST http://localhost:8000/api/v1/demo/clear-demo-data
```

---

## 🏗️ Estructura del Proyecto

```
JoxAI-Bank-Demo/
├── banking_chatbot/
│   ├── backend/              # API FastAPI
│   │   ├── app/
│   │   │   ├── api/v1/      # Endpoints REST
│   │   │   ├── core/        # Configuración y seguridad
│   │   │   ├── models/      # Modelos de datos
│   │   │   ├── schemas/     # Schemas Pydantic
│   │   │   ├── services/    # Lógica de negocio
│   │   │   ├── config.py    # Configuración
│   │   │   ├── dependencies.py
│   │   │   └── main.py      # Punto de entrada
│   │   ├── requirements.txt
│   │   └── venv/            # Entorno virtual Python
│   │
│   └── frontend/
│       ├── admin-panel/     # Panel React
│       │   ├── src/
│       │   │   ├── components/  # Componentes React
│       │   │   ├── pages/       # Páginas/rutas
│       │   │   ├── services/    # API clients
│       │   │   ├── styles/      # CSS
│       │   │   ├── App.jsx
│       │   │   └── main.jsx
│       │   ├── package.json
│       │   ├── vite.config.js
│       │   └── node_modules/
│       │
│       └── widget-demo.html # Demo del widget
│
├── replit.md                # Documentación del proyecto
└── SETUP_VSCODE.md          # Esta guía
```

---

## 🧪 Probar el Sistema Completo

### 1. Verificar Backend
```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@joxai.com","password":"admin123"}'
```

### 2. Verificar Frontend
- Navega a http://localhost:5173/
- Haz login con las credenciales
- Verifica que aparezca el dashboard

### 3. Probar Chat Widget
- Abre http://localhost:8000/widget-demo
- Prueba enviar mensajes
- Verifica que el chatbot responda

---

## 🔧 Solución de Problemas

### Error: "Module not found"
```bash
# Asegúrate de estar en el entorno virtual
cd banking_chatbot/backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Encuentra y mata el proceso usando el puerto
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Error: CORS en el frontend
Verifica que en `backend/app/config.py` CORS_ORIGINS incluya:
```python
CORS_ORIGINS = ["*"]  # Para desarrollo
```

### Frontend no carga estilos
```bash
cd banking_chatbot/frontend/admin-panel
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 🚀 Build para Producción

### Backend
Ya está listo - el backend sirve tanto API como frontend compilado.

### Frontend
```bash
cd banking_chatbot/frontend/admin-panel
npm run build
```

Esto genera `dist/` que el backend servirá automáticamente.

### Ejecutar en Producción
```bash
cd banking_chatbot/backend
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

Todo estará disponible en: http://localhost:5000/

---

## 📚 Recursos Adicionales

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **VS Code Python**: https://code.visualstudio.com/docs/python/python-tutorial

---

## ✅ Checklist de Instalación

- [ ] Python 3.11+ instalado
- [ ] Node.js 18+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual de Python creado y activado
- [ ] Dependencias de Python instaladas (`pip install -r requirements.txt`)
- [ ] Dependencias de Node.js instaladas (`npm install`)
- [ ] Backend corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:5173
- [ ] Login exitoso en el admin panel
- [ ] Widget demo funcionando

¡Todo listo! 🎉

---

**Última actualización**: Octubre 4, 2025
