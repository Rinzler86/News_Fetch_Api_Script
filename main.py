from datetime import timedelta, datetime
from ignore_file import RAPID_API_KEY
import requests
import json

def fetch_news(query, from_date, to_date, language="en", location="us", page=1):
    url = "https://newsnow.p.rapidapi.com/newsv2"
    payload = {
        "query": query,
        "time_bounded": True,
        "from_date": from_date,
        "to_date": to_date,
        "location": location,
        "language": language,
        "page": page
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": f"{RAPID_API_KEY}",
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)

    print(f"HTTP Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    print(f"HTTP Status Code: {response.status_code}")
    try:
        response_json = response.json()
        print(f"Fetching news for: {query}")
        print(json.dumps(response_json, indent=4))
        return response_json
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        return None

def print_news_articles(news_data, filename="news_articles.json"):
    # Prepare articles list for JSON
    articles_list = []

    if news_data and 'news' in news_data and news_data['news']:
        articles = news_data['news']
        for article in articles:
            # Print to console
            print(f"Title: {article.get('title', 'No Title')}")
            print(f"Link: {article.get('url', 'No Link')}")
            print(f"Published Date: {article.get('date', 'No Publication Date')}")
            print(f"Content: {article.get('text', 'No Content Available')}")
            print("-" * 60)

            # Add to articles list for JSON
            articles_list.append({
                "title": article.get('title', 'No Title'),
                "link": article.get('url', 'No Link'),
                "published_date": article.get('date', 'No Publication Date'),
                "content": article.get('text', 'No Content Available')
            })

        # Save articles to JSON file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(articles_list, file, ensure_ascii=False, indent=4)
            print(f"Articles have been saved to {filename}")
    else:
        print("No articles found or there was an error fetching the articles.")

def main():
    topics = ["United States"]
    to_date = datetime.now()  # Today's date
    from_date = to_date - timedelta(days=30)  # Date 30 days ago

    for topic in topics:
        news_data = fetch_news(topic, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
        if news_data:
            print_news_articles(news_data)
        else:
            print(f"Failed to fetch news articles for {topic}. Check the printed details above for more information.")

if __name__ == "__main__":
    main()
