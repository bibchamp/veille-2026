from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import snscrape.modules.twitter as sntwitter
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/veille")
def lancer_veille(mots_cles: str = Query(...)):
    mots = [m.strip().lower() for m in mots_cles.split(',')]
    alertes = []

    # Twitter
    tweets = sntwitter.TwitterSearchScraper(" OR ".join(mots)).get_items()
    for tweet in list(tweets)[:10]:
        contenu = tweet.content.lower()
        if any(m in contenu for m in mots):
            alertes.append({
                "date": str(tweet.date),
                "source": "Twitter",
                "auteur": tweet.user.username,
                "contenu": tweet.content,
                "lien": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
            })

    # Presse locale (RSS exemple)
    feed = feedparser.parse("https://www.clicanoo.re/rss.xml")
    for entry in feed.entries[:10]:
        contenu = entry.title.lower() + ' ' + entry.summary.lower()
        if any(m in contenu for m in mots):
            alertes.append({
                "date": entry.published,
                "source": "Clicanoo",
                "auteur": "Clicanoo",
                "contenu": entry.title,
                "lien": entry.link
            })

    return alertes