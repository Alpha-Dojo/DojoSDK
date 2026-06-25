from dojo import Dojo
import time


def test_caching():
    client = Dojo(api_key="test")

    # First fetch (should hit disk)
    start = time.time()
    df1 = client.stocks.get_all_klines_with_df()
    t1 = time.time() - start
    print(f"First fetch: {t1:.4f} seconds (Shape: {df1.shape})")

    # Second fetch (should hit cache)
    start = time.time()
    df2 = client.stocks.get_all_klines_with_df()
    t2 = time.time() - start
    print(f"Second fetch: {t2:.4f} seconds (Shape: {df2.shape})")

    assert t2 < t1, "Second fetch was not faster than first fetch!"
    assert df1 is df2, "The returned DataFrame is not the exact same cached object!"


if __name__ == "__main__":
    test_caching()
    print("Caching test passed!")
