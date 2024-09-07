import {useState} from 'react';
import {useDropzone} from 'react-dropzone';
import {separateAudio} from '../api/api';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleDrop = (acceptedFiles) => {
        setFile(acceptedFiles[0]);
        setUploadStatus('');
        setErrorMessage('');
    };

    const handleUpload = async () => {
        if (!file) {
            setErrorMessage('Please select a file to upload.');
            return;
        }

        setUploadStatus('Uploading...');
        setErrorMessage('');

        try {
            const response = await separateAudio(2, file); // Adjust stemCount and other parameters as needed
            setUploadStatus('File uploaded successfully.');
            console.log('File uploaded successfully:', response);
        } catch (error) {
            setUploadStatus('');
            setErrorMessage('Error uploading file. Please try again.');
            console.error('Error uploading file:', error);
        }
    };

    const {getRootProps, getInputProps} = useDropzone({onDrop: handleDrop});

    return (
        <div className="container">
            <div {...getRootProps({className: 'dropzone'})}>
                <input {...getInputProps()} />
                <p>Drag & drop a audio file here, or click to select one</p>
                <p>Supported formats: mp3, wav, ogg</p>
                <p>Maximum file size: 10 MB</p>
            </div>
            {file && <p className="file-name">{file.name}</p>}
            <button className="button is-primary mt-4" onClick={handleUpload}>Upload</button>
            {uploadStatus && <p className="notification is-success mt-4">{uploadStatus}</p>}
            {errorMessage && <p className="notification is-danger mt-4">{errorMessage}</p>}
        </div>
    );
};

export default FileUpload;