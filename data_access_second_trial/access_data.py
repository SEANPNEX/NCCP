import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm.asyncio import tqdm_asyncio

# Load links from file
with open("all_links_full.txt", "r") as file:
    links = [line.strip() for line in file if line.strip()]

# Split links into 20 batches
def split_into_batches(data, num_batches):
    batch_size = len(data) // num_batches
    return [data[i * batch_size:(i + 1) * batch_size] for i in range(num_batches)]

batches = split_into_batches(links, 20)

# Set rate limit (delay in seconds)
RATE_LIMIT_DELAY = 0.1  # Adjust as needed

# Asynchronous function to fetch data and extract table information and coordinates
async def fetch_data(session, url):
    try:
        # Respect rate limit
        await asyncio.sleep(RATE_LIMIT_DELAY)
        
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = bs(html_content, "html.parser")
                
                # Locate the table and extract table data
                table = soup.find("table")
                data_dict = {}
                
                # Extract table rows and clean values
                for row in table.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        label = cells[0].get_text(strip=True).replace(":", "")
                        value = cells[1].get_text(strip=True)
                        # Clean up value by removing unwanted characters
                        clean_value = value.replace("\n", "").replace(" ", "").replace("\r", "")
                        data_dict[label] = clean_value
                
                # Extract coordinates from the Google Maps iframe
                iframe = soup.find("iframe", src=lambda x: x and "maps.google.com" in x)
                if iframe:
                    src_url = iframe.get("src")
                    # Parse latitude and longitude from the URL
                    lat_lng = src_url.split("q=")[-1].split("&")[0]  # Extract "37.033295,-76.435401"
                    lat, lng = lat_lng.split(",")
                    data_dict["Latitude"] = lat
                    data_dict["Longitude"] = lng
                
                return data_dict
            else:
                print(f"Failed to fetch {url} with status {response.status}")
                with open("failed_address.txt", 'a') as f:
                    f.write(url + "\n")
                return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        with open("failed_address.txt", 'a') as f:
            f.write(url + "\n")
        return None

# Function to process a single batch
async def process_batch(session, batch, batch_index):
    print(f"Starting batch {batch_index + 1}...")
    tasks = [fetch_data(session, link) for link in batch]
    results = await tqdm_asyncio.gather(*tasks, desc=f"Batch {batch_index + 1}")
    print(f"Completed batch {batch_index + 1}.")
    return [result for result in results if result is not None]

# Main asynchronous function to handle all batches
async def fetch_all_batches(batches):
    all_data = []
    async with aiohttp.ClientSession() as session:
        for i, batch in enumerate(batches):
            batch_results = await process_batch(session, batch, i)
            all_data.extend(batch_results)
            
            # Rest for 10 seconds between batches
            if i < len(batches) - 1:  # No need to rest after the last batch
                print("Resting for 10 seconds...")
                await asyncio.sleep(10)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    return df

# Execute the async code and produce the DataFrame
async def main():
    df = await fetch_all_batches(batches)
    # Save or display the DataFrame as needed
    df.to_csv("extracted_data_with_coordinates.csv", index=False)  # Save to CSV
    print("Data extraction and saving completed")

# Run the main function
asyncio.run(main())
