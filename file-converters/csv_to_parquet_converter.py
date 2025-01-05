import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

def csv_to_parquet(csv_file, parquet_file=None, chunk_size=10_000):
    """
    Converts a csv file to a parquet file
    Args:
        csv_file: Path to the input csv file.
        parquet_file: Path to the output parquet file. 
        chunk_size: The number of rows to read from the csv at a time (default: 10,000).
                   Useful for large csv files to manage memory efficiently
    """
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"The csv file '{csv_file} was not found.")
    
    if parquet_file is None:
        parquet_file = os.path.splitext(csv_file)[0] + ".parquet"
        
    parquet_writer = None # Initialize parquet_writer outside the loop
    
    try:
        for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
            # Convert the pandas DataFrame chunk to a PyArrow Table
            table = pa.Table.from_pandas(chunk)
            
            # Create a ParquetWriter if it doesn't exist yet
            if parquet_writer is None:
                parquet_writer = pq.ParquetWriter(parquet_file, table.schema)
            
            parquet_writer.write_table(table)
                    
        print(f"Successfully converted '{csv_file}' to '{parquet_file}'")
        
    except Exception as e:
        # Close the ParquetWriter if it was created
        print(f"An error occurred: {e}")
    
    finally:
        # Close the ParquetWriter if it was created
        if parquet_writer:
            parquet_writer.close()

# Example usage
if __name__ == "__main__":
    csv_file_path = "./data/Combined_Flights_2022.csv"
    parquet_file_path = "./data/flights.parquet"
    
    csv_to_parquet(csv_file_path, parquet_file_path)
