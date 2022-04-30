# Homework

Implementujte aplikaci, ktera bude pravidelne prochazet zpravodajske servery a ukladat si titulky a URL jednotlivych clanku. Aplikace si data bude ukladat do sve DB a publikuje REST API, pres ktere se bude dat v databazi clanku vyhledavat podle klicovych slov. V pripade nedostupnosti zpravodajskeho serveru se s tim aplikace vyrovna.

Implementujte testy na jednotlive komponenty.

Pro implementaci jsme poskytli zaklad aplikace, kam je potreba doplnit funkcni kod. Potrebne prerekvizity, aby to cele fungovalo:

- Python 3.8, `pip`
- docker a docker-compose

Pokud by vam nevyhovovala pouzita kostra aplikace, pripadne jste chteli pouzit jiny framework, je to mozne. 

## Setup

```bash
# vytvoreni virtualniho prostredi
python3.8 -m venv .venv

# instalace balicku
.venv/bin/pip install -U pip
.venv/bin/pip install -U pipenv
.venv/bin/pipenv install

# spusteni dockeru s DB
docker-compose down -t1
docker-compose up -d --build

# vytvoreni prazdne DB
.venv/bin/python -m app.setup
```

## Spusteni vysledne aplikace

Komponenty:

```bash
.venv/bin/python -m app.scraper
.venv/bin/python -m app.api
```

Otestovani REST API:

```bash
curl --request POST 'http://localhost:5000/articles/find' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "keywords": [
            "babiš",
            "prymul"
        ]
    }'
```


## Jednotlive kroky
- nacist titulky a URL clanku z: `idnes.cz`, `ihned.cz`, `bbc.com`
    - implementovat v `app.news`
    - otestovat pomoci `python -m pytest -k news_test`
- pravidelne (napr. kazdou minutu) stahovat clanky; nove (kontrola dle URL clanku) si data do DB
    - implementovat v `app.scraper`
    - otestovat pomoci `python -m pytest -k scraper_test`
- publikovat nasledujici REST API, ktere umoznuje vyhledavat v ulozenych clancich podle keywords
    - implementovat v `app.api`
    - otestovat pomoci cURL
    
    `POST /articles/find`

    
        {
            "keywords": ["monkey", "dog", "snail"]
        }
        
    Priklad vysledku pro dana keywords:

        {
            "articles: [
                { "text": "Big monkey got caught in London", "url": "https://www.bbc.com/..." },
                { "text": "Is this dog really cute?", "url": "https://www.bbc.com/..." },
                { "text": "Dog vs Snail – which is better?", "url": "https://www.bbc.com/..." }
            ]
        }
        
# Pro implementaci pouzijte
- web scraping: `requests`
- ORM: `sqlalchemy`
- web API: `flask`
- pro parsovani HTML, validaci REST requestu, scheduling – dle vasi volby, vhodne jsou napr. `beautifulsoup4`, `marshmallow`
