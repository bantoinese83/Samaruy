import streamlit as st
import os
import time
from urllib.parse import urlencode
from urllib.request import urlopen, Request

URL_API = "https://www.lalal.ai/api/"

_orion_stems = ('vocals', 'voice', 'drum', 'piano', 'bass', 'electric_guitar', 'acoustic_guitar')
_phoenix_stems = ('vocals', 'voice', 'drum', 'piano', 'bass', 'electric_guitar', 'acoustic_guitar', 'synthesizer', 'strings', 'wind')

# --- Utility Functions ---

def update_progress(progress):
    """Updates the progress bar with the given percentage."""
    st.progress(progress)
    st.write(f"Progress: {progress}%")

def make_content_disposition(filename, disposition='attachment'):
    """Creates a Content-Disposition header for file downloads."""
    try:
        filename.encode('ascii')
        file_expr = f'filename="{filename}"'
    except UnicodeEncodeError:
        from urllib.parse import quote
        quoted = quote(filename)
        file_expr = f"filename*=utf-8''{quoted}"
    return f'{disposition}; {file_expr}'

def upload_file(file_path, license):
    """Uploads the given file to the Lalal.AI API."""
    url_for_upload = URL_API + "upload/"
    _, filename = os.path.split(file_path)
    headers = {
        "Content-Disposition": make_content_disposition(filename),
        "Authorization": f"license {license}",
    }
    with open(file_path, 'rb') as f:
        request = Request(url_for_upload, f, headers)
        with urlopen(request) as response:
            upload_result = response.json()
            if upload_result["status"] == "success":
                return upload_result["id"]
            else:
                st.error(upload_result["error"])
                return None

def split_file(file_id, license, stem, splitter, enhanced_processing, noise_cancelling):
    """Initiates the splitting process for the uploaded file."""
    url_for_split = URL_API + "split/"
    headers = {
        "Authorization": f"license {license}",
    }
    query_args = {
        'id': file_id,
        'stem': stem,
        'splitter': splitter
    }

    if enhanced_processing is not None:
        query_args['enhanced_processing_enabled'] = enhanced_processing
    if noise_cancelling is not None:
        query_args['noise_cancelling_level'] = noise_cancelling

    encoded_args = urlencode(query_args).encode('utf-8')
    request = Request(url_for_split, encoded_args, headers=headers)
    with urlopen(request) as response:
        split_result = response.json()
        if split_result["status"] == "error":
            st.error(split_result["error"])
            return None
        return True

def check_file(file_id):
    """Continuously checks the status of the splitting process."""
    url_for_check = URL_API + "check/?"
    query_args = {'id': file_id}
    encoded_args = urlencode(query_args)

    is_queueup = False

    while True:
        with urlopen(url_for_check + encoded_args) as response:
            check_result = response.json()

        if check_result["status"] == "error":
            st.error(check_result["error"])
            return None

        task_state = check_result["task"]["state"]

        if task_state == "success":
            update_progress(100)
            return check_result["split"]

        elif task_state == "error":
            st.error(check_result["task"]["error"])
            return None

        elif task_state == "progress":
            progress = int(check_result["task"]["progress"])
            if progress == 0 and not is_queueup:
                st.info("Queue up...")
                is_queueup = True
            elif progress > 0:
                update_progress(progress)

        else:
            st.warning(f'Unknown track state: {task_state}')
            return None

        time.sleep(5)

def download_file(url_for_download):
    """Downloads the split track from the provided URL."""
    with urlopen(url_for_download) as response:
        filename = response.headers["Content-Disposition"].split("filename=")[1].strip('"')
        file_content = response.read()
        return filename, file_content

# --- Streamlit App ---

st.title("Samaruy Stem Separator")
license_key = st.text_input("Enter your Lalal.AI License Key:", type="password")

if license_key:
    uploaded_file = st.file_uploader("Upload an audio file", type=['mp3', 'wav', 'ogg', 'flac'])

    if uploaded_file:
        splitter = st.selectbox("Select Splitter", ["orion", "phoenix"])

        stem_options = _orion_stems if splitter == 'orion' else _phoenix_stems
        stem = st.selectbox("Select Stem to Extract", stem_options)

        enhanced_processing = st.checkbox("Enhanced Processing", value=False, disabled=(stem == 'voice'))
        noise_cancelling = st.slider("Noise Cancelling Level (for 'voice' only)", 0, 2, 1, disabled=(stem != 'voice'))

        if st.button("Start Separation"):
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                file_id = upload_file(uploaded_file, license_key)

            if file_id:
                with st.spinner("Splitting file..."):
                    split_successful = split_file(file_id, license_key, stem, splitter, enhanced_processing, noise_cancelling)

                if split_successful:
                    with st.spinner("Checking progress..."):
                        split_result = check_file(file_id)

                    if split_result:
                        with st.spinner("Downloading tracks..."):
                            stem_filename, stem_content = download_file(split_result['stem_track'])
                            back_filename, back_content = download_file(split_result['back_track'])

                        st.success("Separation complete!")
                        st.download_button(
                            label=f"Download {stem_filename}",
                            data=stem_content,
                            file_name=stem_filename)
                        st.download_button(
                            label=f"Download {back_filename}",
                            data=back_content,
                            file_name=back_filename)
else:
    st.info("Please enter your Lalal.AI license key to begin.")