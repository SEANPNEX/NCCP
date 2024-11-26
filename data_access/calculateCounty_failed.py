import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import asyncio
from tqdm.asyncio import tqdm as async_tqdm

# Load GeoJSON and CSV files
geo_NC = gpd.read_file("NC_counties.geojson")
geo_nearby = gpd.read_file("merged_output.geojson")
bus_df = pd.read_csv("failed_data.csv")

# Function to find the county
async def find_county(lon, lat):
    point = Point(lon, lat)
    for _, county in geo_NC.iterrows():
        if county['geometry'].contains(point):
            return county.get('NAME')
    for _, county in geo_nearby.iterrows():
        if county['geometry'].contains(point):
            return f"NOT_NC:{county.get('NAME')}"
    return "NOT_FOUND"

# Process a single row
async def process_row(row):
    company = row.to_dict()
    lat = company["Latitude"]
    lon = company["Longitude"]
    company.update({"County": await find_county(lon, lat)})
    return company

# Process DataFrame asynchronously
async def process_dataframe_async(df):
    results = []
    # Wrap rows with async tqdm for progress bar
    tasks = [process_row(row) for _, row in df.iterrows()]
    for task in async_tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        results.append(await task)
    return pd.DataFrame(results)

# Main coroutine
async def main():
    # Process the DataFrame
    processed_df = await process_dataframe_async(bus_df)

    # Save the result
    processed_df.to_csv("processed_results_failed.csv", index=False)
    print(processed_df.head())

# Run the main coroutine
asyncio.run(main())
