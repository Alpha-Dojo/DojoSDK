from dojo import Dojo
import asyncio


def test_sync():
    client = Dojo(api_key="test")
    df = client.stocks.get_all_klines_with_df()
    print(f"Sync returned dataframe with shape: {df.shape}")


async def test_async():
    from dojo import AsyncDojo

    client = AsyncDojo(api_key="test")
    df = await client.stocks.get_all_klines_with_df()
    print(f"Async returned dataframe with shape: {df.shape}")


if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())
    print("Both tests passed!")
