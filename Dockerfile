# ==========================================
# ETAP 1: Builder (Budowanie zależności)
# ==========================================
# Używamy tej samej wersji Pythona co u Ciebie lokalnie (3.13)
# Wersja 'slim' jest mniejsza i bezpieczniejsza.
FROM python:3.13-slim AS builder

# Ustawiamy zmienne środowiskowe dla Pythona i Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Dodajemy Poetry do ścieżki systemowej
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalujemy curl (potrzebny do pobrania instalatora Poetry)
# oraz ewentualne zależności systemowe dla bibliotek (np. gcc dla niektórych paczek)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalujemy Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki definiujące zależności (najpierw tylko one, żeby wykorzystać cache Dockera)
COPY pyproject.toml poetry.lock ./

# Instalujemy zależności produkcyjne (bez dev)
# --no-root oznacza, że nie instalujemy Twojego projektu jako paczki, tylko jego zależności
RUN poetry install --only main --no-root

# ==========================================
# ETAP 2: Runtime (Uruchomienie aplikacji)
# ==========================================
# Startujemy z czystego obrazu Pythona
FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Tworzymy użytkownika nie-root dla bezpieczeństwa
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
USER 999

# KLUCZOWE: Kopiujemy gotowe środowisko wirtualne (.venv) z etapu 'builder'
COPY --from=builder --chown=python:python /app/.venv /app/.venv

# Dodajemy środowisko wirtualne do ścieżki systemowej.
# Dzięki temu komenda 'python' automatycznie użyje paczek z venv.
ENV PATH="/app/.venv/bin:$PATH"

# Kopiujemy resztę Twojego kodu aplikacji
COPY --chown=python:python . .

# Informujemy Dockera, na jakim porcie nasza aplikacja będzie słuchać.
# Render/Cloud Run zazwyczaj oczekują nasłuchu na porcie zdefiniowanym w zmiennej $PORT.
# Domyślnie ustawimy 8000, ale aplikacja powinna to respektować.
EXPOSE 8000

# Komenda startowa.
# Skoro aktywowaliśmy venv w PATH, nie musimy pisać 'poetry run'.
# Używamy 'exec', aby proces Pythona był głównym procesem kontenera (PID 1).
# Zakładam, że Twój plik app/main.py ma blok 'if __name__ == "__main__": uvicorn.run(...)'
# który nasłuchuje na hoście 0.0.0.0 (ważne w Dockerze!) i porcie z env.
CMD ["python", "-m", "app.main"]
# ALTERNATYWNA, często lepsza komenda produkcyjna (jeśli powyższa nie zadziała):
# CMD ["exec", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]