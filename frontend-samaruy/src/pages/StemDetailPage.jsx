import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import AudioPlayer from '../components/AudioPlayer';
import { getStemDetails } from '../api/api';
import Loader from '../components/Loader';

const StemDetailPage = () => {
    const { stemId } = useParams();
    const [stem, setStem] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchStem = async () => {
            try {
                const response = await getStemDetails(stemId);
                setStem(response);
            } catch (error) {
                setError('Error fetching stem details. Please try again.');
                console.error('Error fetching stem:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStem().then(r => console.log(r));
    }, [stemId]);

    if (loading) {
        return <Layout><Loader /></Layout>;
    }

    if (error) {
        return <Layout><div style={{ color: 'red' }}>{error}</div></Layout>;
    }

    return (
        <Layout>
            <h1>{stem.name}</h1>
            <AudioPlayer src={stem.url} formats={[{ type: 'audio/mpeg', extension: 'mp3' }]} />
        </Layout>
    );
};

export default StemDetailPage;