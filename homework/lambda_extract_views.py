## Part 3: Create Lambda Function

import datetime
import json
import boto3
import requests

S3_WIKI_BUCKET = "catheloni-wikidata"

def WikiViewLambdacatheloni(event, context):

    current_time = datetime.datetime.now(datetime.timezone.utc)

    # Get date from event or default to 21 days ago
    date_str = event.get("date")
    if date_str:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = current_time - datetime.timedelta(days=21)

    date_api = date.strftime("%Y/%m/%d")
    date_store = date.strftime("%Y-%m-%d")

    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{date_api}"
    print(f"Requesting REST API URL: {url}")

    response = requests.get(url, headers={"User-Agent": "curl/7.68.0"})
    if response.status_code != 200:
        raise Exception(f"Wiki API error: {response.status_code}")

    data = response.json()

    json_lines = ""

    for art in data["items"][0]["articles"][:10]:
        record = {
            "title": art["article"],
            "views": art["views"],
            "rank": art["rank"],
            "date": date_store,
            "retrieved_at": current_time.replace(tzinfo=None).isoformat(),
        }
        json_lines += json.dumps(record) + "\n"

    s3 = boto3.client("s3")
    s3_key = f"raw-views/raw-views-{date_store}.json"
    s3.put_object(Bucket=S3_WIKI_BUCKET, Key=s3_key, Body=json_lines)

