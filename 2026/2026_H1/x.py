import requests
import pandas as pd
import time

# --- Configuration ---
# The specific market Condition ID for "Presidential Election Winner 2024"
CONDITION_ID = "0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"


def get_trump_token_id():
    """
    Fetches the specific Token ID for 'Donald Trump' from the Gamma API.
    """
    url = "https://gamma-api.polymarket.com/markets"
    params = {"condition_id": CONDITION_ID}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Handle list response
        if isinstance(data, list):
            data = data[0]

        # Parse Outcomes and IDs
        # Note: Polymarket stores these as JSON strings inside the JSON response
        import json

        outcomes = json.loads(data["outcomes"]) if isinstance(data["outcomes"], str) else data["outcomes"]
        clob_ids = json.loads(data["clobTokenIds"]) if isinstance(data["clobTokenIds"], str) else data["clobTokenIds"]

        print(f"Market Found: {data['question']}")

        # Find Trump
        for i, outcome in enumerate(outcomes):
            if "Trump" in outcome:
                print(f"Selected Outcome: {outcome}")
                print(f"Token ID: {clob_ids[i]}")
                return clob_ids[i]

        return None
    except Exception as e:
        print(f"Error fetching ID: {e}")
        return None


def fetch_all_trades(token_id):
    """
    Fetches raw trade data (ticks) from the Data API.
    This is more reliable for closed markets than the History endpoint.
    """
    url = "https://data-api.polymarket.com/trades"
    all_trades = []
    limit = 1000
    offset = 0

    print("\nStarting data download (this may take a moment)...")

    # Loop to fetch older data (Pagination)
    # We fetch a few pages as an example. Increase 'max_pages' for full history.
    max_pages = 10

    for page in range(max_pages):
        params = {
            "asset": token_id,  # Use Asset ID (Token ID) not Market ID
            "limit": limit,
            "offset": offset,
        }

        try:
            r = requests.get(url, params=params)

            # Rate limit handling
            if r.status_code == 429:
                print("Rate limit hit. Sleeping for 2 seconds...")
                time.sleep(2)
                continue

            data = r.json()

            if not data:
                break

            all_trades.extend(data)
            offset += limit
            print(f"Fetched {len(all_trades)} trades so far...")

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    return pd.DataFrame(all_trades)


# --- Main Execution ---
if __name__ == "__main__":
    # 1. Get Correct ID
    token_id = get_trump_token_id()

    if token_id:
        # 2. Fetch Raw Trades
        df = fetch_all_trades(token_id)

        if not df.empty:
            # 3. Process Data
            df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
            df["price"] = pd.to_numeric(df["price"])
            df["size"] = pd.to_numeric(df["size"])

            # Sort by time
            df = df.sort_values("datetime")

            # 4. Filter for Election Night (Example: Nov 4 - Nov 6)
            mask = (df["datetime"] >= "2024-11-04") & (df["datetime"] <= "2024-11-07")
            election_df = df.loc[mask].copy()

            # 5. Resample to 1-Minute Candles (The "Graph" View)
            # This turns raw ticks into Open-High-Low-Close data
            ohlc_1min = election_df.set_index("datetime").resample("1min")["price"].agg(["first", "max", "min", "last"])
            ohlc_1min.columns = ["Open", "High", "Low", "Close"]

            print("\n--- 1-Minute Resampled Data (Election Night) ---")
            print(ohlc_1min.dropna().head(10))

            # election_df.to_csv("trump_raw_trades.csv", index=False)
            # ohlc_1min.to_csv("trump_1min_candles.csv")

        else:
            print("No trades found. The Data API might be archiving very old data.")
    else:
        print("Could not find Token ID.")
