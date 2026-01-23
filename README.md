# Signal Bot

Bot para Signal con fact-checking IA.

## Comandos

| Comando | Descripción |
|---------|-------------|
| `!help` | lista de comandos |
| `!groupid` | muestra ID del grupo (se borra en 60s) |
| `!chat \| !grok` | fact-check al chat |
| `!tldr` | resumen del chat |

## Deploy (Docker)

```bash
cp sample.env .env
# editar .env
docker compose up -d
```

### Variables de entorno

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `PHONE_NUMBER` | ✅ | Número registrado en Signal |
| `GROQ_API_KEY` | ✅ | API key de Groq |
| `REDIS_URI` | ✅ | URI de Redis |
| `ALLOWED_GROUPS` | ❌ | Whitelist grupos (vacío = todos) |

### Registrar cuenta Signal

Primera vez, linkear con QR:
```bash
curl "http://localhost:8080/v1/qrcodelink?device_name=bot"
```
Escanear desde Signal > Dispositivos vinculados.

## Dev local

```bash
pip install -r requirements.txt
python -m app.main
```
