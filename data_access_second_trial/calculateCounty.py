import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import asyncio
from tqdm.asyncio import tqdm as async_tqdm
from tqdm import tqdm

# Load GeoJSON and CSV files
geo_NC = gpd.read_file("NC_counties.geojson")
geo_nearby = gpd.read_file("merged_output.geojson")
bus_df = pd.read_csv("extracted_data_with_coordinates.csv")

# Function to split DataFrame into batches
def split_dataframe_into_batches(df, num_batches):
    batch_size = len(df) // num_batches
    return [df.iloc[i * batch_size:(i + 1) * batch_size] for i in range(num_batches)]

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

# Process a single batch
async def process_batch(df):
    results = []
    # Wrap rows with async tqdm for progress bar
    tasks = [process_row(row) for _, row in df.iterrows()]
    async for result in async_tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Processing batch"):
        results.append(await result)
    return pd.DataFrame(results)

# Main function to process DataFrame in batches
async def process_dataframe_in_batches(df, num_batches):
    all_results = []
    batches = split_dataframe_into_batches(df, num_batches)
    overall_progress = tqdm(total=len(df), desc="Overall Progress", unit="row")

    for i, batch in enumerate(batches):
        print(f"Processing batch {i + 1}/{num_batches}...")
        batch_results = await process_batch(batch)
        all_results.append(batch_results)

        # Update overall progress
        overall_progress.update(len(batch))

    overall_progress.close()
    # Concatenate all batch results into a single DataFrame
    return pd.concat(all_results, ignore_index=True)

# Main coroutine
async def main():
    # Process the DataFrame in 20 batches
    processed_df = await process_dataframe_in_batches(bus_df, num_batches=20)

    # Save the result
    processed_df.to_csv("processed_results.csv", index=False)
    print("Processed DataFrame:")
    print(processed_df.head())

# Run the main coroutine
asyncio.run(main())
