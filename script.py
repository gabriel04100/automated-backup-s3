import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
path_dir = os.getenv("directory")
bucket_name = os.getenv("bucket_name")


def upload_file(file_name: str, bucket: str, object_name: str = None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
        logging.info(f"File {file_name} uploaded successfully {object_name}")
    except ClientError as e:
        logging.error(f"Error uploading file {file_name}: {e}")
        return False
    return True


def upload_directory(path_dir: str, bucket: str):
    """Recursively upload a directory to an S3 bucket

    :param path_dir: Directory to upload
    :param bucket: S3 bucket name
    """

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            # Full local path of the file
            file_path = os.path.join(root, file)

            s3_object_name = os.path.relpath(file_path, path_dir)
            # Upload the file
            upload_file(file_path, bucket, s3_object_name)


def main():
    # Configuration du logging
    logging.basicConfig(filename="./logs/push_to_s3.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Vérifier les buckets S3 disponibles
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()

    print("Existing buckets:")
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

    if path_dir and bucket_name:
        logging.info(f"Starting upload of {path_dir} to {bucket_name}")
        upload_directory(path_dir, bucket_name)
        logging.info("Upload completed.")
    else:
        logging.error("Directory path or bucket name not specified.")


if __name__ == "__main__":
    main()
