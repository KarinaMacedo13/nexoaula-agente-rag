# Despliegue en Oracle Cloud Infrastructure (OCI)

La vía más simple para cumplir el desafío es usar **OCI Compute** con Docker. Este procedimiento deja la aplicación accesible en el puerto 8501.

## 1. Crear la instancia

- Crea una VM Ubuntu en OCI Compute.
- Para una prueba académica, una forma Always Free compatible es suficiente cuando esté disponible en tu región.
- Descarga o registra la clave SSH.
- En la VCN o Network Security Group habilita TCP 22 desde tu IP y TCP 8501 para la demostración. Para producción, usa HTTPS detrás de un proxy o balanceador.

## 2. Conectarse e instalar Docker

```bash
ssh -i tu_clave.pem ubuntu@IP_PUBLICA
sudo apt-get update
sudo apt-get install -y docker.io git
sudo usermod -aG docker ubuntu
exit
```

Vuelve a conectarte para aplicar el grupo Docker.

## 3. Clonar y configurar

```bash
git clone https://github.com/TU_USUARIO/nexoaula-agente-rag.git
cd nexoaula-agente-rag
cp .env.example .env
nano .env
```

Agrega `GEMINI_API_KEY` sin subir el archivo `.env` al repositorio.

## 4. Construir y ejecutar

```bash
docker build -t nexoaula-agent .
docker run -d --name nexoaula -p 8501:8501 --env-file .env -v "$PWD/data:/app/data" nexoaula-agent
docker logs -f nexoaula
```

Abre `http://IP_PUBLICA:8501`.

## 5. Evidencia exigida

- Captura la aplicación funcionando con la URL o IP visible.
- Guarda la imagen en `docs/evidence/oci_deploy.png`.
- Añade la URL pública y la captura al README antes de entregar.
- Revisa que el repositorio sea público y que no contenga claves.

## 6. Mejoras opcionales

- Guardar documentos en OCI Object Storage.
- Guardar secretos en OCI Vault.
- Usar un dominio, HTTPS y Nginx.
- Enviar logs a OCI Logging.
- Automatizar despliegue con GitHub Actions u OCI DevOps.
