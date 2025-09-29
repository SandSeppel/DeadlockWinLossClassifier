import pyarrow.dataset as ds
import pandas as pd


def fetch_dump(batch_size, batch_index):
    dataset = ds.dataset("training_data/raw/match_info_30.parquet", format="parquet")

    table = dataset.to_table()
    batches = table.to_batches(max_chunksize = batch_size)
    return batches[batch_index].to_pandas()["match_id"]
