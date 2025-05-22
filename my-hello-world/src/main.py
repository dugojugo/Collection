"""
Module defines the main entry point for the Apify Actor.
To build Apify Actors, utilize the Apify SDK toolkit:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations
import asyncio
import csv
from apify import Actor
from apify_client import ApifyClient

API_TOKEN = ""
ACTOR_ID = "dbEyMBriog95Fv8CW"
CSV_FILENAME = "actor_results.csv"

async def main() -> None:
    """Define the main async entry point for the Apify Actor."""
    async with Actor:
        Actor.log.info('Starting Actor execution...')

        # Initialize the ApifyClient with your API token
        client = ApifyClient(API_TOKEN)

        # Prepare the Actor input
        run_input = {
            "query": "Chicago",
            "maxItemsPerQuery": 10,
            "includeTags": True,
            "includeNearbyResults": False,
            "includeAttractions": True,
            "includeRestaurants": True,
            "includeHotels": True,
            "includeVacationRentals": False,
            "includePriceOffers": False,
            "includeAiReviewsSummary": False,
            "language": "en",
            "currency": "USD",
            "locationFullName": "Chicago",
        }

        # Run the Actor and wait for it to finish
        Actor.log.info(f"Calling actor {ACTOR_ID} with input: {run_input}")
        run = client.actor(ACTOR_ID).call(run_input=run_input)

        # Fetch dataset items and collect them
        dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        # Log and write to CSV
        if dataset_items:
            keys = dataset_items[0].keys()
            with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(dataset_items)
            Actor.log.info(f"Results written to {CSV_FILENAME}")
        else:
            Actor.log.info("No data items found in the dataset.")
