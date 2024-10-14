import streamlit as st
from dotenv import load_dotenv
import os
from src.s3_upload import upload_file, upload_directory, get_existing_buckets

# Charger les variables d'environnement
load_dotenv()

# Obtenir le chemin du répertoire à partir du fichier .env
path_dir = os.getenv("directory")

# Interface utilisateur de Streamlit
st.title("S3 File Uploader")

# Obtenir les buckets existants
st.subheader("Existing Buckets:")
try:
    # Appeler la fonction pour obtenir la liste des buckets
    buckets = get_existing_buckets()
    if buckets:
        for bucket in buckets['Buckets']:
            st.write(f'  - {bucket["Name"]}')
    else:
        st.write("No buckets found.")
except Exception as e:
    st.error(f"Error fetching buckets: {e}")

# Interface pour upload via drag and drop
st.subheader("Upload files to S3")

# Sélection du bucket parmi les buckets existants
existing_buckets_names = [bucket["Name"] for bucket in buckets['Buckets']]
selected_bucket = st.selectbox("Select a bucket to upload to",
                               existing_buckets_names)

# Drag and Drop pour un seul fichier
uploaded_file = st.file_uploader("Choose a file to upload", type=None)

if uploaded_file is not None:
    # Chemin temporaire pour sauvegarder le fichier avant upload
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Lancer l'upload vers S3
    if st.button("Upload to S3"):
        try:
            upload_successful = upload_file(uploaded_file.name,
                                            selected_bucket)
            if upload_successful:
                st.success("File {} uploaded successfully to {}.".format(
                    uploaded_file.name, selected_bucket
                ))
            else:
                st.error(f"Failed to upload {uploaded_file.name}.")
        except Exception as e:
            st.error(f"Error during upload: {e}")

# Upload d'un répertoire entier
if st.checkbox("Upload an entire directory"):
    if path_dir:
        st.write(f"Directory to upload: {path_dir}")
        if st.button("Upload directory to S3"):
            try:
                upload_directory(path_dir, selected_bucket)
                st.success("Directory {} uploaded successfully to {}.".format(
                    path_dir, selected_bucket
                ))
            except Exception as e:
                st.error(f"Error uploading directory: {e}")
    else:
        st.warning("No directory path specified in .env file.")
