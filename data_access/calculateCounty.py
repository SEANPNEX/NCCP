import matplotlib.pyplot as plt
import geoplot
import geoplot.crs as gcrs
import geopandas as gpd
from shapely.geometry import Point, shape
from shapely.validation import explain_validity
import pandas as pd
import sqlite3
from tqdm import tqdm
import concurrent.futures

geo_NC = gpd.read_file(
    "NC_counties.geojson"
)
geo_nearby = gpd.read_file("merged_output.geojson")
bus_df = pd.read_csv("extracted_data_with_coordinates.csv")

def find_county(lon, lat):
    point = Point(lon, lat)
    for _, county in geo_NC.iterrows():
        if county['geometry'].contains(point):
            return county.get('NAME')
    for _, county in geo_nearby.iterrows():
        if county['geometry'].contains(point):
            return f"NOT_NC:{county.get('NAME')}"
    return "NOT_FOUND"

def process_row(row):
    company = row.to_dict()
    lat = company["Latitude"]
    lon = company["Longitude"]
    company.update({"County": find_county(lon, lat)})
    return company

# Main processing function
def process_dataframe_async(df, geo_NC, geo_nearby):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Wrap rows with tqdm for progress bar
        futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            results.append(future.result())
    return pd.DataFrame(results)

# Example usage
# Replace `bus_df`, `geo_NC`, and `geo_nearby` with your actual data
processed_df = process_dataframe_async(bus_df, geo_NC, geo_nearby)

# Display or save the result
processed_df.to_csv("processed_results.csv", index=False)
print(processed_df.head())