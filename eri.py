import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(3)  # Simulating network delay
    print("Data fetched!")
    return "Data"

async def main():
    task1 = asyncio.create_task(fetch_data())  # Starts fetch_data()
    task2 = asyncio.create_task(fetch_data())  # Starts another fetch_data()
    
    await task1  # Waits for task1 to complete
    await task2  # Waits for task2 to complete

asyncio.run(main())