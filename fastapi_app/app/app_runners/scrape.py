import json
import requests

from bs4 import BeautifulSoup
from lxml import etree

from app_models.m_articles import ArticleCRUD

# ---------------------------------------------------------------

# ---------------------------------------------------------------
class Scrape():

    def __init__(self, symbol):
        print(f"Scraper init...")
        
        yahoo_fin_url = f"https://finance.yahoo.com/quote/AAPL?p={symbol}"
    
        elements_to_scrape = {}    
        
        try:
            f = open("app_runners/scrape_elements.json")        
        except Exception as e:
            print(f"Could not open file: {e}")
        else:
            data = f.read()
            print(data)
            elements_to_scrape = json.loads(data)
            print(data)

        finally:
            f.close()
        
        HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

        print(f"About 2 scrape {yahoo_fin_url}")

        try:
            r = requests.get(url = yahoo_fin_url, headers=HEADERS)
        except Exception as e:
            print(f"Could not load url {yahoo_fin_url}: {e}")
        else:
            if (r.url != yahoo_fin_url): 
                # redir. occured (perhaps invalid symbol)
                raise requests.TooManyRedirects()
            
            r.raise_for_status()

            self.soup = BeautifulSoup(r.content, "html.parser")
            self.dom = etree.HTML(str(self.soup))

            self.__summary = {}
            print(elements_to_scrape)
            if elements_to_scrape is not None:
                for el in elements_to_scrape["elements"]:
                    print(f"scraping {el}")
                    # tag = self.soup.select_one(el["from"])
                    tag = self.dom.xpath(el["from"])[0].text

                    if tag is not None:
                        print(f"Tag: {tag}")
                        self.__summary[el["to"]] = tag
        
    
    async def summary(self):
        print(f"Returning summary...")
        return self.__summary      



# ---------------------------------------------------------------
async def run_scraper():
    resp = await ArticleCRUD.get_all()

    
    s = Scrape(symbol="AAPL")
    print(s.summary())

    print(f">>>>>>>>> {resp}")
    return resp


# ===============================================================
if __name__ == "__main__":
    msg = f"{__name__} started directly"    
    print(msg)




    # print(sys.path)
else:
    msg = f"{__name__} started as a module."
    print(msg)
    # print(sys.path)
