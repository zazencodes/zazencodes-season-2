from datetime import datetime, timedelta

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator

# Define default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email": ["your-email@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def download_from_s3(
    s3_client, bucket_name: str, s3_file_key: str, local_file_path: str
) -> None:
    """
    Downloads a file from S3 to a local path.

    Args:
        s3_client: Initialized boto3 S3 client
        bucket_name (str): Name of the S3 bucket containing the input file
        s3_file_key (str): Path to the file within the S3 bucket
        local_file_path (str): Local path to save the downloaded file

    Raises:
        ClientError: If there's an error accessing S3
    """
    print(f"Downloading file from s3://{bucket_name}/{s3_file_key}")
    s3_client.download_file(bucket_name, s3_file_key, local_file_path)


def read_and_process_data(local_file_path: str) -> pd.DataFrame:
    """
    Reads and processes the CSV data using pandas.

    Args:
        local_file_path (str): Path to the local CSV file

    Returns:
        pd.DataFrame: Processed DataFrame

    Raises:
        Exception: If there's an error processing the data
    """
    print("Reading file with pandas")
    df = pd.read_csv(local_file_path)
    log_dataframe_summary(df)
    # Process the dataframe as needed
    # df = df.some_transformation()
    return df


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Saves the processed DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): Processed DataFrame to save
        output_path (str): Path where to save the processed file
    """
    print(f"Saving processed file to {output_path}")
    df.to_csv(output_path, index=False)


def process_s3_data(
    bucket_name: str,
    s3_file_key: str,
    local_file_path: str = "/tmp/downloaded_file.csv",
    output_path: str = "/tmp/processed_file.csv",
    **context,
) -> str:
    """
    Downloads a CSV file from S3, processes it using pandas, and saves the result locally.

    Args:
        bucket_name (str): Name of the S3 bucket containing the input file
        s3_file_key (str): Path to the file within the S3 bucket
        local_file_path (str, optional): Local path to save the downloaded file. Defaults to "/tmp/downloaded_file.csv"
        output_path (str, optional): Local path to save the processed file. Defaults to "/tmp/processed_file.csv"
        **context: Additional context parameters passed by Airflow

    Returns:
        str: Success message indicating where the processed file was saved

    Raises:
        ClientError: If there's an error accessing S3
        Exception: If there's an error processing the data
    """
    import boto3
    from botocore.exceptions import ClientError

    s3_client = boto3.client("s3")
    download_from_s3(s3_client, bucket_name, s3_file_key, local_file_path)
    df = read_and_process_data(local_file_path)
    save_processed_data(df, output_path)
    return f"Data processing completed. File saved to {output_path}"


def log_dataframe_summary(df: pd.DataFrame) -> None:
    """Logs summary statistics for a pandas DataFrame.

    This function calculates and logs basic summary statistics for a pandas DataFrame,
    including the shape, data types, null value counts, and basic descriptive statistics
    for numeric columns.

    Args:
        df (pd.DataFrame): The input pandas DataFrame to analyze

    Returns:
        None: This function only logs output and does not return anything
    """
    print("\n=== DataFrame Summary ===")
    print(f"\nShape: {df.shape}")

    print("\nData Types:")
    print(df.dtypes)

    print("\nNull Value Counts:")
    print(df.isnull().sum())

    print("\nNumeric Column Statistics:")
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns
    if len(numeric_columns) > 0:
        print(df[numeric_columns].describe())
    else:
        print("No numeric columns found")

    print("\n=== End Summary ===")


# Define the DAG
dag = DAG(
    "example_python_operator",
    default_args=default_args,
    description="A simple example DAG with PythonOperator",
    schedule_interval="0 2 * * 0",  # Run weekly on Sunday at 2am
    catchup=False,
    tags=["example"],
)

# Define the task
process_task = PythonOperator(
    task_id="process_data_task",
    python_callable=process_s3_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies (if you have multiple tasks)
# task1 >> process_task >> task3
