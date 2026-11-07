import requests
from bs4 import BeautifulSoup
import csv

print("Starting web scraper...", flush=True)

url = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    print("Connecting to website...", flush=True)

    response = requests.get(
        url, headers=headers, timeout=30
    )

    response.raise_for_status()

    print("Website connected!", flush=True)

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find(
            "p", class_="instock availability"
        ).text.strip()
        rating = book.p["class"][1]

        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating
        })

    print("Books extracted:", len(books), flush=True)

    with open("books_data.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["Title", "Price", "Availability", "Rating"]
        )

        writer.writeheader()
        writer.writerows(books)

    print("CSV file saved successfully!", flush=True)
except requests.exceptions.RequestException as e:
    print("Connection error:", e)

except Exception as e:
    print("Error:", e)
print("Program finished!", flush=True)