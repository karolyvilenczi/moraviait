
Kedze mi bolo umoznene si zvolit iny framework, resp. postup a kedze 
som chapal zmysel (aj) demonstrovat sposob rozmyslania a schopnosti fo FastaPI som sa rozhodol 
upravit riesenie ktore som pouzival ked som sa ucil z knihy:

Building Data Science Applications with FastAPI

https://www.packtpub.com/product/building-data-science-applications-with-fastapi/9781801079211#:~:text=About%20this%20book,API%20backends%20using%20practical%20examples.

(Pozn: tu neide o ziadne copy paste z github knihy, vsetko je moje dielo.)

Rozsahovo je tu daleko viac, nez pre vypracovanie zadania bolo potrebne, ale znazornujem aj decoupling, stavbu modularneho riesenia, atd.
Nedostatky:
- Testy som implementoval len pre jeden modul, len pre demo (viac casu pre rozsah pohovoru som do toho teraz nechcel investovat). Samozrejme, ze by bolo mozne komplexne rozpracovat jednotlive test case-y, tooling ako pytest, alebo selenium, locust, atd., ale to by bolo casovo narocne.
- Pre logging normalne nepouzivam print ale riadne upraveny modul logging kde posielam rozne levely logov do roznych suborov, do Elasticsearch, ak treba.
- Scraper resp. API nema riesene kontrolu toho, ci sa uz dany article v DB nachadza, alebo nie. Tu by som normalne implementoval nejaky hash toho clanku a ten by bol kontrolovany pred zapisov. Samozrejme by sa to dalo urobit aj komplexnejsie (ten hash by bol v REDIS-e napr.)
- Nemam ulozeny timestamp, kedy bol clanok tahany
- Nie je tam statistika, ktore klucove slovo je kolko krat napr.
- Nie su zapnute indexy v DB
- Kod nie je zdokumentovany (napr. pre Sphynx)
- URL-ka by som vysunul do .env, alebo ulozil do DB, zatial su hardcodovane
-- Mal som problem s hn.cz (ihned.cz), CSS selektory, ktore mi fungovali inde tu nesli (neinvestoval som toho vela casu aby som zistoval preco, ale urcite by sa dal zistit postup cez XPATH napr. )
-- Nie je handling toho, ak mam JS pop-up na cookies (robil som to raz a musel som pouzit selenium na simulovanie klinutia myskou, toto som povazoval nad ramec.)

- ..a nie je ziaden session control a security.
Tak mi to zatial dufam odpustite. :)

Tesim sa na feedback.
KV


# TO start up in a new environment.:

1. run 'make build'
2. run' docker network create dev'
3. run 'make up_all' or 'make up_all_d'

4. To do DB migrations w. Alembic:
4.1. run 'make alembic_init'

In the generated migrations folder configure:
- in env.py

1. comment out '# target_metadata = None' (OR replace w.)
2. insert the following lines (between the # ---)
# -----------------------------------
import app_models

from app_models import app_db
target_metadata = app_db.metadata
# -----------------------------------

- in alebic.ini:
add: 'sqlalchemy.url=postgresql+asyncpg://scraper_user:scraper_pass@srv_postgres:5432/scraper'

4.2. run 'make alembic_gen_first_migration'
( observe the migrations generated in the 'migrations' folder: should contain the SA fields picked up from the app_models)

4.3. run 'make alembic_migrate'

5. run tests (those that are implemented, not all are)

6. use: with Postman or curl:
# -----------------------------------
GET ALL ARTICLES:
curl --location --request GET 'http://127.0.0.1:8000/article/'

GET ARTICLE W. ID 1
curl --location --request GET 'http://127.0.0.1:8000/article/1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title":"My NEW title",
    "content": "My NEW  content"
}'

# -----------------------------------
POST NEW ARTICLE:
curl --location --request POST 'http://127.0.0.1:8000/article' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url":"www.idnes.cz",
    "text": "Big animal got caught in Prague"
}'

# -----------------------------------
POST (FIND) W. KWS: "russia",  "pokoje"
curl --location --request POST 'http://127.0.0.1:8000/article/find/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "keywords": [
        "russia",
        "pokoje"
    ]    
}'

# -----------------------------------
DELETE ARTICLE ID 5
curl --location --request DELETE 'http://127.0.0.1:8000/article/5' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": 2,
    "first_name":"Petrovics",
    "last_name": "Parkerovics",
    "age":25
}'