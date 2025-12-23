from pytrends.request import TrendReq
import logging

pytrends = TrendReq(hl="en-US", tz=360)

def fetch_trends(keyword, country):
    try:
        pytrends.build_payload(
            [keyword],
            timeframe="today 3-m",
            geo=country
        )

        data = pytrends.interest_over_time()

        if data.empty:
            return None

        value = int(data[keyword].mean())

        return {
            "workflow": keyword,
            "platform": "Google",
            "country": country,
            "popularity_metrics": {
                "average_interest": value
            },
            "evidence_source": "Google Trends"
        }

    except Exception as e:
        logging.warning(f"Trends API error for '{keyword}': {e}")
        return None
