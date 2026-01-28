# --- Fáze 1: Builder (Příprava závislostí) ---
FROM python:3.11-slim as builder

# Nastavíme pracovní adresář
WORKDIR /app

# Zabráníme vytváření .pyc souborů a bufferování výstupu (lepší logy)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Vytvoříme virtuální prostředí
RUN python -m venv /opt/venv
# Přidáme venv do cesty, abychom mohli volat pip přímo
ENV PATH="/opt/venv/bin:$PATH"

# Zkopírujeme seznam závislostí a nainstalujeme je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Fáze 2: Final (Běh aplikace) ---
FROM python:3.11-slim

# Zkopírujeme předpřipravené virtuální prostředí z fáze 1
COPY --from=builder /opt/venv /opt/venv

# Nastavíme cestu, aby se používal Python z venvu
ENV PATH="/opt/venv/bin:$PATH"

# Nastavíme pracovní adresář
WORKDIR /app

# Zkopírujeme zbytek tvého kódu do kontejneru
COPY . .

# Otevřeme port 8000
EXPOSE 8000

# Spustíme aplikaci
# Pozor: host 0.0.0.0 je v Dockeru nutný (localhost by zvenku nefungoval)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]