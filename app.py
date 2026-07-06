from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from textblob import TextBlob
import re

app = Flask(__name__)


# ============================================
# GET WEBSITE HTML
# ============================================

def get_website_data(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None, f"Failed to access website ({response.status_code})"

        return response.text, "Success"

    except Exception as e:
        return None, str(e)


# ============================================
# CLEAN TEXT
# ============================================

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ============================================
# ADVANCED WEBSITE TYPE DETECTION
# ============================================

def detect_website_type(text, title, meta_description, url):

    content = f"{title} {meta_description} {text}".lower()

    domain = urlparse(url).netloc.lower()

    website_categories = {

        # -----------------------------------
        # SEARCH ENGINES
        # -----------------------------------

        "Search Engine": [
            "search", "web results",
            "images", "videos",
            "maps", "search engine",
            "find results"
        ],

        # -----------------------------------
        # SOCIAL MEDIA
        # -----------------------------------

        "Social Media Website": [
            "followers", "following",
            "like", "share",
            "comment", "post",
            "stories", "reels",
            "chat", "messaging"
        ],

        # -----------------------------------
        # VIDEO / OTT
        # -----------------------------------

        "Video Streaming Website": [
            "watch video", "streaming",
            "movies", "tv shows",
            "episodes", "live streaming",
            "watch online"
        ],

        # -----------------------------------
        # MUSIC
        # -----------------------------------

        "Music Platform": [
            "music", "playlist",
            "listen", "album",
            "artist", "songs",
            "podcast"
        ],

        # -----------------------------------
        # EDUCATION
        # -----------------------------------

        "Education Website": [
            "course", "tutorial",
            "learn", "training",
            "academy", "university",
            "student", "education",
            "certification", "classes"
        ],

        # -----------------------------------
        # CODING
        # -----------------------------------

        "Coding & Developer Website": [
            "repository", "developer",
            "api", "documentation",
            "open source", "programming",
            "software", "code editor",
            "debugging"
        ],

        # -----------------------------------
        # SHOPPING
        # -----------------------------------

        "E-Commerce Website": [
            "buy now", "checkout",
            "shopping cart", "wishlist",
            "product", "offers",
            "discount", "shop",
            "order now"
        ],

        # -----------------------------------
        # AI
        # -----------------------------------

        "AI Website": [
            "artificial intelligence",
            "machine learning",
            "chatbot", "llm",
            "generate text",
            "generate image",
            "ai assistant",
            "deep learning"
        ],

        # -----------------------------------
        # NEWS
        # -----------------------------------

        "News Website": [
            "breaking news",
            "headlines",
            "world news",
            "latest news",
            "journal",
            "politics"
        ],

        # -----------------------------------
        # BLOG
        # -----------------------------------

        "Blog Website": [
            "blog", "read article",
            "posted by",
            "comments",
            "author"
        ],

        # -----------------------------------
        # FORUM
        # -----------------------------------

        "Forum Website": [
            "discussion",
            "community",
            "threads",
            "forum",
            "reply"
        ],

        # -----------------------------------
        # BUSINESS
        # -----------------------------------

        "Business Website": [
            "our services",
            "company",
            "solutions",
            "clients",
            "business",
            "enterprise"
        ],

        # -----------------------------------
        # WEB APPLICATION
        # -----------------------------------

        "Web Application": [
            "dashboard",
            "sign in",
            "login",
            "workspace",
            "admin panel"
        ],

        # -----------------------------------
        # BANKING
        # -----------------------------------

        "Banking Website": [
            "bank", "loan",
            "credit card",
            "account",
            "transaction",
            "net banking"
        ],

        # -----------------------------------
        # FINANCE
        # -----------------------------------

        "Finance Website": [
            "investment",
            "stock market",
            "finance",
            "trading",
            "mutual fund"
        ],

        # -----------------------------------
        # CRYPTO
        # -----------------------------------

        "Cryptocurrency Website": [
            "crypto",
            "bitcoin",
            "blockchain",
            "wallet",
            "token"
        ],

        # -----------------------------------
        # TRAVEL
        # -----------------------------------

        "Travel Website": [
            "hotel", "flight",
            "booking",
            "vacation",
            "tour",
            "destination"
        ],

        # -----------------------------------
        # HEALTHCARE
        # -----------------------------------

        "Healthcare Website": [
            "doctor",
            "hospital",
            "patient",
            "medical",
            "clinic",
            "treatment"
        ],

        # -----------------------------------
        # FOOD DELIVERY
        # -----------------------------------

        "Food Delivery Website": [
            "restaurant",
            "food delivery",
            "menu",
            "order food",
            "dining"
        ],

        # -----------------------------------
        # JOB PORTAL
        # -----------------------------------

        "Job Portal": [
            "jobs",
            "career",
            "vacancy",
            "hiring",
            "recruitment",
            "apply now"
        ],

        # -----------------------------------
        # GAMING
        # -----------------------------------

        "Gaming Website": [
            "game",
            "gaming",
            "multiplayer",
            "esports",
            "play online"
        ],

        # -----------------------------------
        # SPORTS
        # -----------------------------------

        "Sports Website": [
            "live score",
            "sports news",
            "cricket",
            "football",
            "match"
        ],

        # -----------------------------------
        # GOVERNMENT
        # -----------------------------------

        "Government Website": [
            "government",
            "ministry",
            "public services",
            "citizen",
            "official portal"
        ],

        # -----------------------------------
        # PORTFOLIO
        # -----------------------------------

        "Portfolio Website": [
            "portfolio",
            "my projects",
            "my work",
            "case studies",
            "designer"
        ],

        # -----------------------------------
        # PHOTOGRAPHY
        # -----------------------------------

        "Photography Website": [
            "gallery",
            "photography",
            "photos",
            "albums",
            "wedding shoots"
        ],

        # -----------------------------------
        # WIKI
        # -----------------------------------

        "Wiki Website": [
            "encyclopedia",
            "wiki",
            "knowledge base",
            "history"
        ],

        # -----------------------------------
        # FILE SHARING
        # -----------------------------------

        "File Sharing Website": [
            "upload",
            "download",
            "share files",
            "cloud storage"
        ],

        # -----------------------------------
        # CLOUD PLATFORM
        # -----------------------------------

        "Cloud Platform": [
            "cloud",
            "virtual server",
            "hosting",
            "deploy",
            "infrastructure"
        ],

        # -----------------------------------
        # CYBERSECURITY
        # -----------------------------------

        "Cybersecurity Website": [
            "security",
            "vpn",
            "encryption",
            "cybersecurity",
            "firewall"
        ]
    }

    # =====================================
    # SCORING
    # =====================================

    scores = {}

    for category, keywords in website_categories.items():

        score = 0

        for keyword in keywords:

            if keyword in content:
                score += 1

        scores[category] = score

    # =====================================
    # DOMAIN BASED DETECTION
    # =====================================

    domain_rules = {

        "Search Engine": [
            "google", "bing",
            "yahoo", "duckduckgo"
        ],

        "Social Media Website": [
            "facebook", "instagram",
            "twitter", "linkedin",
            "snapchat", "pinterest"
        ],

        "Video Streaming Website": [
            "youtube", "netflix",
            "primevideo",
            "hotstar",
            "vimeo"
        ],

        "Music Platform": [
            "spotify", "soundcloud",
            "gaana", "wynk"
        ],

        "Education Website": [
            "coursera", "udemy",
            "khanacademy",
            "w3schools"
        ],

        "Coding & Developer Website": [
            "github", "gitlab",
            "stackoverflow",
            "replit",
            "codepen"
        ],

        "E-Commerce Website": [
            "amazon", "flipkart",
            "myntra", "ebay",
            "shopify"
        ],

        "AI Website": [
            "openai", "chatgpt",
            "claude",
            "gemini",
            "perplexity"
        ],

        "News Website": [
            "bbc", "cnn",
            "ndtv",
            "timesofindia"
        ],

        "Travel Website": [
            "booking", "makemytrip",
            "airbnb", "tripadvisor"
        ],

        "Food Delivery Website": [
            "zomato", "swiggy"
        ],

        "Job Portal": [
            "linkedin", "indeed",
            "naukri"
        ],

        "Gaming Website": [
            "steam", "epicgames"
        ],

        "Wiki Website": [
            "wikipedia"
        ],

        "Cloud Platform": [
            "aws", "azure",
            "digitalocean"
        ]
    }

    for category, domains in domain_rules.items():

        if any(x in domain for x in domains):
            scores[category] += 6

# =====================================
# BEST MATCH
# =====================================
    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "General Website"

    return best_category
# ============================================
# HOME PAGE
# ============================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================
# ANALYZE API
# ============================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        website_url = data.get("url")

        if not website_url.startswith("http"):
            website_url = "https://" + website_url

        html, status = get_website_data(website_url)

        if html is None:
            return jsonify({
                "error": status
            })

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        title = soup.title.string.strip() if soup.title else "No Title"

        meta_description = ""

        desc_tag = soup.find("meta", attrs={"name": "description"})

        if desc_tag and desc_tag.get("content"):
            meta_description = desc_tag["content"]

        text = soup.get_text()

        text = clean_text(text)

        short_text = text[:5000]

        website_type = detect_website_type(
            short_text,
            title,
            meta_description,
            website_url
        )

        sentiment = TextBlob(short_text).sentiment.polarity

        if sentiment > 0:
            tone = "Positive"
        elif sentiment < 0:
            tone = "Negative"
        else:
            tone = "Neutral"

        links = soup.find_all("a")
        images = soup.find_all("img")
        forms = soup.find_all("form")

        total_links = len(links)
        total_images = len(images)
        total_forms = len(forms)

        conclusion = (
            f"This website appears to be a {website_type}. "
            f"It contains {total_links} links and "
            f"{total_images} images. "
            f"The overall website tone is {tone.lower()}."
        )

        return jsonify({

            "url": website_url,
            "website_type": website_type,
            "title": title,
            "meta_description": meta_description,
            "tone": tone,
            "links": total_links,
            "images": total_images,
            "forms": total_forms,
            "preview": short_text[:1000],
            "conclusion": conclusion

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":
    app.run(debug=True)
