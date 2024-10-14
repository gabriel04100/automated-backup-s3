import logging
import os
from dotenv import load_dotenv
from src.s3_upload import upload_directory, get_existing_buckets

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
path_dir = os.getenv("directory")
bucket_name = os.getenv("bucket_name")


def main():
    # Configuration du logging
    logging.basicConfig(filename="./logs/push_to_s3.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Vérifier les buckets S3 disponibles
    buckets = get_existing_buckets()
    print("Existing buckets:")
    for bucket in buckets['Buckets']:
        print(f'  {bucket["Name"]}')

    if path_dir and bucket_name:
        logging.info(f"Starting upload of {path_dir} to {bucket_name}")
        upload_directory(path_dir, bucket_name)
        logging.info("Upload completed.")
    else:
        logging.error("Directory path or bucket name not specified.")


if __name__ == "__main__":
    main()
