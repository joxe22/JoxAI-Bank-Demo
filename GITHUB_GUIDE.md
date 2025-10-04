# Guía: Subir Cambios a GitHub

Esta guía te ayudará a subir tus cambios al repositorio de GitHub.

## 📍 Tu Repositorio

**URL**: https://github.com/joxe22/JoxAI-Bank-Demo

---

## 🔐 Autenticación en GitHub (Importante)

GitHub ya **NO acepta contraseñas** para git push desde 2021. Necesitas usar:

### Opción 1: Personal Access Token (PAT) - Recomendado

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Dale un nombre descriptivo (ej: "JoxAI-Bank-Demo")
4. Selecciona scopes: `repo` (full control)
5. Click "Generate token"
6. **⚠️ COPIA EL TOKEN AHORA** (no podrás verlo de nuevo)
7. Usa este token en lugar de tu contraseña cuando git te la pida

### Opción 2: SSH Key (Más seguro, pero más complejo)

Si prefieres SSH, sigue [esta guía oficial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## 🚀 Subir Cambios a GitHub

### Método 1: Push Directo (Si solo tú trabajas en el repo)

```bash
# 1. Verifica que estés en la rama correcta
git status
git branch

# 2. Agrega todos los archivos modificados
git add .

# 3. Haz commit con un mensaje descriptivo
git commit -m "Configuración completa de despliegue y documentación"

# 4. Sube a GitHub
git push origin main
```

**Cuando te pida credenciales:**
- Username: `joxe22`
- Password: **TU PERSONAL ACCESS TOKEN** (no tu contraseña de GitHub)

---

### Método 2: Pull → Commit → Push (Recomendado para evitar conflictos)

```bash
# 1. Obtén los últimos cambios del repositorio remoto
git pull origin main

# 2. Si hay conflictos, resuélvelos y luego:
git add .
git commit -m "Resueltos conflictos de merge"

# 3. Agrega tus nuevos cambios
git add .

# 4. Haz commit
git commit -m "Añadidas guías de VS Code y despliegue completo"

# 5. Sube a GitHub
git push origin main
```

---

## 📝 Mensajes de Commit Efectivos

Usa mensajes claros y descriptivos:

### ✅ Buenos ejemplos:
```bash
git commit -m "Agregado sistema de autenticación JWT"
git commit -m "Corregido error de CORS en API"
git commit -m "Configuración de despliegue Autoscale completa"
git commit -m "Documentación de instalación en VS Code"
```

### ❌ Malos ejemplos:
```bash
git commit -m "cambios"
git commit -m "fix"
git commit -m "update"
```

---

## 🔄 Flujo de Trabajo Completo (Diario)

Este es el flujo que usarás normalmente:

```bash
# 1. Al empezar a trabajar
git pull origin main

# 2. Trabaja en tu código...
# (editas archivos, creas features, etc.)

# 3. Revisa qué cambió
git status

# 4. Agrega archivos específicos (o todos con .)
git add archivo1.py archivo2.js
# O todos los cambios:
git add .

# 5. Haz commit
git commit -m "Descripción clara de tus cambios"

# 6. Sube a GitHub
git push origin main

# 7. Repite cuando hagas más cambios
```

---

## 📊 Comandos Útiles de Git

### Ver Estado Actual
```bash
git status                 # Ver archivos modificados
git log --oneline -5       # Ver últimos 5 commits
git diff                   # Ver cambios antes de hacer commit
```

### Gestión de Archivos
```bash
git add archivo.py         # Agregar archivo específico
git add .                  # Agregar todos los archivos
git add *.js               # Agregar todos los archivos .js
git restore archivo.py     # Descartar cambios en un archivo
```

### Información del Repositorio
```bash
git remote -v              # Ver URL del repositorio remoto
git branch                 # Ver ramas locales
git branch -a              # Ver todas las ramas (local + remoto)
```

---

## 🌿 Trabajar con Ramas (Branches)

Si quieres trabajar en una nueva feature sin afectar `main`:

```bash
# Crear y cambiar a nueva rama
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commits
git add .
git commit -m "Nueva funcionalidad agregada"

# Subir la rama a GitHub
git push -u origin feature/nueva-funcionalidad

# Volver a main
git checkout main

# Fusionar tu rama a main (después de hacer PR en GitHub)
git merge feature/nueva-funcionalidad
git push origin main
```

---

## ⚠️ Solución de Problemas Comunes

### Error: "Updates were rejected"
Significa que hay cambios en GitHub que no tienes localmente.

**Solución:**
```bash
git pull origin main --rebase
git push origin main
```

### Error: "Authentication failed"
Estás usando tu contraseña en lugar del Personal Access Token.

**Solución:**
1. Genera un Personal Access Token (ver arriba)
2. Usa el token como contraseña

O configura Git para recordar el token:
```bash
git config --global credential.helper store
git push origin main
# (Ingresa username y token, se guardará)
```

### Error: "Merge conflict"
Dos personas editaron el mismo archivo.

**Solución:**
```bash
git status                 # Ver archivos en conflicto
# Edita los archivos manualmente para resolver conflictos
git add archivo-resuelto.py
git commit -m "Resueltos conflictos de merge"
git push origin main
```

### Deshacer el último commit (antes de push)
```bash
git reset --soft HEAD~1    # Mantiene los cambios
# O
git reset --hard HEAD~1    # ⚠️ ELIMINA los cambios
```

---

## 📂 Archivos que NO debes subir a GitHub

Estos archivos ya están en `.gitignore`:

- `venv/` o `env/` - Entornos virtuales de Python
- `node_modules/` - Dependencias de Node.js
- `dist/` - Builds de producción
- `__pycache__/` - Cache de Python
- `.env` - Variables de entorno sensibles
- `*.pyc` - Archivos compilados de Python

### Verificar .gitignore
```bash
cat .gitignore
```

Si falta algo, agrégalo:
```bash
echo "secrets.txt" >> .gitignore
git add .gitignore
git commit -m "Actualizado .gitignore"
```

---

## 🎯 Comandos Rápidos (Copiar y Pegar)

### Subir cambios rápidamente
```bash
git pull origin main && git add . && git commit -m "Actualización" && git push origin main
```

### Ver historial gráfico
```bash
git log --graph --oneline --all
```

### Ver quién modificó cada línea de un archivo
```bash
git blame archivo.py
```

---

## 🔗 Recursos Adicionales

- **GitHub Docs**: https://docs.github.com/en/get-started
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Learn Git Branching** (interactivo): https://learngitbranching.js.org/

---

## ✅ Checklist para Subir Cambios

Antes de hacer push, verifica:

- [ ] `git status` para ver qué cambió
- [ ] `git diff` para revisar cambios específicos
- [ ] Todos los archivos necesarios están en staging (`git add`)
- [ ] Mensaje de commit es claro y descriptivo
- [ ] Hiciste `git pull` antes de `git push` (para evitar conflictos)
- [ ] No estás subiendo archivos sensibles (.env, secrets, etc.)
- [ ] El código funciona localmente antes de subirlo

---

## 🚀 Próximos Pasos

Una vez que subas tus cambios a GitHub:

1. Ve a https://github.com/joxe22/JoxAI-Bank-Demo
2. Verifica que tus commits aparezcan
3. Puedes crear un **Release** para versionar tu código
4. Considera agregar **GitHub Actions** para CI/CD automático

---

**¿Listo para subir tus cambios?** 

```bash
git add .
git commit -m "Proyecto completo configurado para producción"
git push origin main
```

¡Hecho! 🎉

---

**Última actualización**: Octubre 4, 2025
