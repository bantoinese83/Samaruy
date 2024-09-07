import { useState } from 'react';
import Layout from '../components/Layout';
import FileUpload from '../components/FileUpload';
import { separateAudio } from '../api/api.js';
import Loader from '../components/Loader';
import AudioPlayer from '../components/AudioPlayer';

const UploadPage = () => {
    const [uploadStatus, setUploadStatus] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [previewUrl, setPreviewUrl] = useState('');

    const handleUpload = async (file) => {
        setLoading(true);
        try {
            const response = await separateAudio(2, file);
            setUploadStatus('File uploaded successfully');
            setErrorMessage('');
            console.log('File uploaded successfully:', response);
        } catch (error) {
            setUploadStatus('');
            setErrorMessage('Error uploading file. Please try again.');
            console.error('Error uploading file:', error);
        } finally {
            setLoading(false);
        }
    };

    const handlePreview = (url) => {
        setPreviewUrl(url);
    };

    return (
        <Layout>
            <h1>Upload Audio File</h1>
            {loading ? (
                <Loader />
            ) : (
                <>
                    <FileUpload onUpload={handleUpload} onPreview={handlePreview} />
                    {previewUrl && (
                        <div>
                            <h2>Audio Preview</h2>
                            <AudioPlayer src={previewUrl} formats={[{ type: 'audio/mpeg', extension: 'mp3' }]} />
                        </div>
                    )}
                    {uploadStatus && <p>{uploadStatus}</p>}
                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                </>
            )}
        </Layout>
    );
};

export default UploadPage;