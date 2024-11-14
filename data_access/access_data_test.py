import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup as bs

# Load links from file
with open("all_links_full.txt", "r") as file:
    all_links_full = [line.strip() for line in file if line.strip()]
# Asynchronous function to fetch data and extract table information
test_links = all_links_full[:100]
async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = bs(html_content, "html.parser")
                
                # Locate the table
                table = soup.find("table")
                data_dict = {}

                # Extract table rows
                for row in table.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        label = cells[0].get_text(strip=True).replace(":", "")
                        value = cells[1].get_text(strip=True).replace(" ","").replace("\n","").replace("\r","")
                        data_dict[label] = value
                
                print(f"Data extracted from {url}")
                return data_dict
            else:
                print(f"Failed to fetch {url} with status {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
# Main asynchronous function to handle all requests and compile results
async def fetch_all_data(links):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, link) for link in links]
        results = await asyncio.gather(*tasks)
        
        # Filter out None results and convert to DataFrame
        data = [result for result in results if result is not None]
        df = pd.DataFrame(data)
        return df

# Execute the async code and produce the DataFrame
async def main():
    df = await fetch_all_data(test_links)
    # Save or display the DataFrame as needed
    df.to_csv("extracted_data_test.csv", index=False)  # Example: save to CSV
    print("Data extraction and saving completed")

# Run the asynchronous main function
asyncio.run(main())