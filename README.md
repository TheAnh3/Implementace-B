# Notes API

Jednoduché HTTP API pro správu poznámek. Data se uchovávají pouze v paměti procesu, takže po restartu aplikace zmizí.

## Požadavky

- Python 3.10 nebo novější

## Instalace

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

Ve Windows aktivujte prostředí příkazem `.venv\Scripts\activate`.

## Spuštění

```bash
uvicorn app.main:app --reload
```

API poběží na `http://127.0.0.1:8000`. Interaktivní dokumentace je na `/docs`.

## Endpointy

| Metoda | Cesta | Popis |
| --- | --- | --- |
| `GET` | `/health` | Stav aplikace |
| `GET` | `/notes` | Seznam poznámek |
| `GET` | `/notes/{id}` | Jedna poznámka |
| `POST` | `/notes` | Vytvoření poznámky |
| `PUT` | `/notes/{id}` | Nahrazení textu poznámky |
| `DELETE` | `/notes/{id}` | Odstranění poznámky |

Tělo požadavku `POST` a `PUT` je JSON, například:

```json
{"text": "Dokončit úkol"}
```

Text musí obsahovat alespoň jeden znak, který není bílým znakem. Úspěšné vytvoření vrací `201`, úspěšné čtení a úprava `200` a úspěšné odstranění `200` s potvrzením v JSON. Chyby používají JSON ve tvaru `{"error": {"code": "...", "message": "..."}}`; neplatný vstup vrací `422` a chybějící endpoint nebo poznámka `404` s odlišným kódem chyby.

## Testy

```bash
python -m pytest
```

Testy obsahují jednotkové ověření úložiště a integrační ověření HTTP API přes FastAPI `TestClient`.
