# Guía de Integración de IA - JoxAI Banking Chatbot

Esta guía te ayudará a integrar **Anthropic Claude** o **OpenAI GPT** para que el chatbot responda con IA real en lugar de respuestas mock.

---

## 📋 Opciones de IA Disponibles

El sistema soporta 3 modos:

1. **Mock** (por defecto): Respuestas predefinidas para desarrollo/testing
2. **Anthropic Claude**: IA conversacional avanzada (recomendado)
3. **OpenAI GPT**: IA de OpenAI (GPT-4, GPT-5)

---

## 🚀 Opción 1: Integrar Anthropic Claude (Recomendado)

### Paso 1: Obtener API Key

1. Ve a https://console.anthropic.com/
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" y genera una nueva key
4. Copia el API key (comienza con `sk-ant-...`)

### Paso 2: Configurar en Replit

#### Método A: Usando Replit Secrets (Recomendado)

1. En Replit, abre la pestaña "Secrets" (🔒 en el panel izquierdo)
2. Agrega las siguientes secrets:
   ```
   Key: ANTHROPIC_API_KEY
   Value: sk-ant-api03-tu-key-aquí
   
   Key: AI_PROVIDER
   Value: anthropic
   
   Key: ANTHROPIC_MODEL (opcional)
   Value: claude-sonnet-4-20250514
   ```

#### Método B: Usando archivo .env (Solo desarrollo local)

Si estás en VS Code o local, crea `.env` en `banking_chatbot/backend/`:

```env
ANTHROPIC_API_KEY=sk-ant-api03-tu-key-aquí
AI_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

**⚠️ IMPORTANTE**: Asegúrate que `.env` esté en `.gitignore`

### Paso 3: Instalar Dependencias (si no están)

```bash
cd banking_chatbot/backend
pip install anthropic httpx
```

### Paso 4: Reiniciar el Servidor

```bash
# Detén el servidor (Ctrl+C)
# Inicia de nuevo
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### Paso 5: Probar

1. Abre el widget demo: http://localhost:5000/widget-demo
2. Envía un mensaje: "Hola, ¿qué tarjetas de crédito ofrecen?"
3. Deberías recibir una respuesta de Claude

---

## 🔵 Opción 2: Integrar OpenAI GPT

### Paso 1: Obtener API Key

1. Ve a https://platform.openai.com/
2. Inicia sesión o crea una cuenta
3. Ve a "API keys" y genera una nueva key
4. Copia el API key (comienza con `sk-...`)

### Paso 2: Configurar en Replit

#### Método A: Usando Replit Secrets (Recomendado)

1. Abre la pestaña "Secrets" (🔒)
2. Agrega:
   ```
   Key: OPENAI_API_KEY
   Value: sk-tu-key-de-openai-aquí
   
   Key: AI_PROVIDER
   Value: openai
   
   Key: OPENAI_MODEL (opcional)
   Value: gpt-5
   ```

#### Método B: Usando archivo .env (Solo desarrollo local)

```env
OPENAI_API_KEY=sk-tu-key-de-openai-aquí
AI_PROVIDER=openai
OPENAI_MODEL=gpt-5
```

### Paso 3: Instalar Dependencias

```bash
cd banking_chatbot/backend
pip install openai httpx
```

### Paso 4: Reiniciar y Probar

Igual que con Anthropic - reinicia el servidor y prueba el widget.

---

## 🧪 Modo de Desarrollo (Mock)

Si quieres usar respuestas mock para desarrollo sin gastar créditos de IA:

### Configuración

```env
AI_PROVIDER=mock
```

O simplemente no configures ningún API key - el sistema usa mock por defecto.

---

## ⚙️ Configuración Avanzada

### Personalizar el System Prompt

Edita `banking_chatbot/backend/app/services/ai_service.py`:

```python
# Línea ~60 (Anthropic) o ~140 (OpenAI)
system_prompt = """Tu prompt personalizado aquí

Ejemplo:
Eres un asistente de JoxAI Bank especializado en:
- Productos financieros premium
- Atención personalizada
- Inversiones y wealth management

Tono: Profesional pero cercano
Idioma: Español
..."""
```

### Ajustar Parámetros del Modelo

En `ai_service.py`:

**Para Anthropic:**
```python
# Línea ~180
json={
    "model": self.model,
    "max_tokens": 1024,  # Ajusta según necesidad
    "temperature": 0.7,  # Añadir para más creatividad (0.0-1.0)
    "system": system_prompt,
    "messages": messages
}
```

**Para OpenAI:**
```python
# Línea ~280
json={
    "model": self.model,
    "messages": messages,
    "max_tokens": 1024,
    "temperature": 0.7  # Ajusta creatividad (0.0-2.0)
}
```

### Agregar Detección de Intents

El sistema ya detecta automáticamente cuando escalar a agente humano. Puedes agregar más lógica:

```python
# En ai_service.py, después de obtener la respuesta:

# Detectar intents específicos
message_lower = message.lower()
if "urgente" in message_lower or "emergencia" in message_lower:
    suggest_escalation = True
    
# Agregar al metadata
return {
    "content": content,
    "metadata": {
        "model": self.model,
        "provider": "anthropic",
        "suggest_escalation": suggest_escalation,
        "intent": "urgent" if "urgente" in message_lower else None
    }
}
```

---

## 🔍 Verificar que la IA está Funcionando

### Método 1: Revisar Logs del Backend

```bash
# Deberías ver en la terminal:
INFO: AI Provider: anthropic
INFO: Model: claude-sonnet-4-20250514
```

### Método 2: Endpoint de Prueba

```bash
# Prueba directa del AI service
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-123",
    "message": "¿Qué servicios bancarios ofrecen?",
    "context": {}
  }'
```

Si funciona con IA real, la respuesta será más detallada y natural.

### Método 3: Verificar Metadata

En las respuestas del chatbot, revisa el campo `metadata`:

```json
{
  "message": "...",
  "metadata": {
    "model": "claude-sonnet-4-20250514",
    "provider": "anthropic"
  }
}
```

Si ves `"provider": "anthropic"` o `"provider": "openai"`, ¡está funcionando!

---

## 💰 Costos y Consideraciones

### Anthropic Claude
- **Claude 3.5 Sonnet**: ~$3 por millón de tokens input, ~$15 por millón output
- **Claude Sonnet 4**: ~$3 por millón de tokens input, ~$15 por millón output
- Conversación promedio: ~1000 tokens = $0.015-0.018

### OpenAI GPT
- **GPT-4**: ~$5 por millón de tokens input, ~$15 por millón output
- **GPT-5**: ~$2.50 por millón de tokens input, ~$10 por millón output
- Conversación promedio: ~1000 tokens = $0.0125

### Recomendaciones de Ahorro

1. **Usa mode mock en desarrollo** - solo activa IA en producción
2. **Limita max_tokens** - reduce a 512 para respuestas más cortas
3. **Implementa rate limiting** - evita spam
4. **Cachea respuestas comunes** - FAQ predefinidas
5. **Monitorea uso** - revisa dashboards de Anthropic/OpenAI

---

## 🐛 Troubleshooting

### Error: "ANTHROPIC_API_KEY no configurada"

**Solución:**
- Verifica que la secret esté creada en Replit
- Reinicia el servidor después de agregar secrets
- Verifica el nombre exacto: `ANTHROPIC_API_KEY`

### Error: "Invalid API key"

**Solución:**
- Verifica que el API key sea correcto
- Asegúrate que empiece con `sk-ant-` (Anthropic) o `sk-` (OpenAI)
- Verifica que la key tenga créditos disponibles

### Error: "Rate limit exceeded"

**Solución:**
- Has alcanzado el límite de requests por minuto
- Espera 1 minuto y vuelve a intentar
- Upgrade tu plan en Anthropic/OpenAI

### El chatbot sigue usando respuestas mock

**Solución:**
```bash
# Verifica las variables de entorno
echo $AI_PROVIDER
echo $ANTHROPIC_API_KEY

# Si están vacías, revisa tus Secrets en Replit
# Reinicia el servidor
```

### Respuestas en inglés

**Solución:**
- El system prompt debe especificar español
- Edita `ai_service.py` y asegúrate que diga "Responde siempre en español"

---

## 📊 Monitoring y Analytics

### Ver Uso de IA en Admin Panel

El sistema registra cada llamada a IA en el metadata. Para ver estadísticas:

1. Ve a Admin Panel → Analytics
2. Revisa "AI Usage" (próximamente)
3. O consulta los logs:

```bash
# Filtrar llamadas a IA
grep "AI Provider" logs/*.log
```

### Dashboard de Anthropic/OpenAI

- **Anthropic**: https://console.anthropic.com/dashboard
- **OpenAI**: https://platform.openai.com/usage

Aquí puedes ver:
- Tokens consumidos
- Costos por día/mes
- Rate limits
- Uso por modelo

---

## 🚀 Próximos Pasos

Una vez que la IA esté funcionando:

1. **Implementar RAG** (Retrieval Augmented Generation)
   - Conecta una base de conocimientos
   - Usa embeddings para búsqueda semántica
   - Mejora precisión de respuestas

2. **Function Calling**
   - Permite que la IA ejecute acciones (consultar saldo, transferir)
   - Claude y GPT-4 soportan function calling
   - Integra con APIs bancarias

3. **Streaming de Respuestas**
   - Respuestas en tiempo real (como ChatGPT)
   - Mejor UX para el usuario
   - Implementar con Server-Sent Events (SSE)

4. **Fine-tuning**
   - Entrena el modelo con conversaciones bancarias
   - Mejora respuestas específicas del dominio
   - OpenAI soporta fine-tuning de GPT-4

5. **Multilingual Support**
   - Detecta idioma del usuario
   - Responde en el idioma detectado
   - Expande a mercados internacionales

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **Anthropic Claude**: https://docs.anthropic.com/
- **OpenAI GPT**: https://platform.openai.com/docs/
- **FastAPI Async**: https://fastapi.tiangolo.com/async/

### Ejemplos de Código

Ver `banking_chatbot/backend/app/services/ai_service.py` para la implementación completa.

### Comunidad y Soporte

- **Anthropic Discord**: https://discord.gg/anthropic
- **OpenAI Community**: https://community.openai.com/
- **Replit Discord**: https://replit.com/discord

---

## ✅ Checklist de Integración

- [ ] API key obtenida (Anthropic o OpenAI)
- [ ] Secret configurada en Replit (ANTHROPIC_API_KEY o OPENAI_API_KEY)
- [ ] AI_PROVIDER configurado (anthropic, openai, o mock)
- [ ] Dependencias instaladas (httpx)
- [ ] Servidor reiniciado
- [ ] Probado en widget demo
- [ ] Respuestas verificadas (metadata incluye provider y model)
- [ ] Costos monitoreados en dashboard de IA
- [ ] System prompt personalizado (opcional)
- [ ] Rate limiting implementado (recomendado)

---

**¿Listo para empezar?** 

```bash
# 1. Obtén tu API key
# 2. Agrégala a Secrets en Replit
# 3. Configura AI_PROVIDER=anthropic
# 4. Reinicia el servidor
# 5. ¡Prueba el chatbot!
```

🎉 **¡Tu chatbot ahora tiene IA real!**

---

**Última actualización**: Octubre 4, 2025  
**Versión**: 1.0  
**Autor**: JoxAI Team
