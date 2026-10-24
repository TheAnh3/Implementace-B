# Implementace B

Jednoduchá aplikace pro správu poznámek vytvořená v rámci experimentu zaměřeného na porovnání různých přístupů k vývoji softwaru.

## Funkce

Aplikace poskytuje HTTP API pro:

- kontrolu dostupnosti aplikace,
- zobrazení všech poznámek a konkrétní poznámky,
- vytváření nových poznámek,
- úpravu a odstraňování existujících poznámek.

Vstupní data se validují a API vrací odpovídající HTTP stavové kódy při úspěšných operacích i chybových situacích. Chybové odpovědi mají jednotný formát JSON.

## Technologie

- Python 3.10+
- FastAPI
- Pydantic
- pytest

## Spuštění

Vytvořte a aktivujte virtuální prostředí:

```bash
python -m venv .venv
source .venv/bin/activate
```

Ve Windows aktivujte prostředí příkazem `.venv\Scripts\activate`.

Nainstalujte závislosti aplikace:

```bash
python -m pip install -e ".[test]"
```

Spusťte aplikaci z kořenové složky projektu:

```bash
uvicorn app.main:app --reload
```

API poběží na `http://127.0.0.1:8000`. Interaktivní dokumentace je dostupná na `http://127.0.0.1:8000/docs`.

## Testování

Automatizované jednotkové a integrační testy spustíte příkazem:

```bash
python -m pytest -v
```

## Poznámky

Data poznámek se uchovávají pouze v paměti aplikace. Po jejím restartování se uložené poznámky odstraní.

Projekt slouží k experimentálnímu porovnání implementací a není určen jako produkční systém.
