import streamlit as st
import boto3
from dotenv import load_dotenv
import os


load_dotenv()
path_dir = os.getenv("directory")
st.title("S3 dump")

s3_client = boto3.client('s3')
response = s3_client.list_buckets()

st.write("Existing buckets:")
for bucket in response['Buckets']:
    st.write(f'  {bucket["Name"]}')
