import { useEffect, useState } from 'react';
import { getAllStems } from '../api/api';
import AudioPlayer from './AudioPlayer';

const StemsGrid = () => {
    const [stems, setStems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchStems = async () => {
            try {
                const response = await getAllStems();
                setStems(response);
            } catch (error) {
                setError('Error fetching stems. Please try again.');
                console.error('Error fetching stems:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStems().then(r => r);
    }, []);

    if (loading) {
        return <div className="notification is-info">Loading...</div>;
    }

    if (error) {
        return <div className="notification is-danger">{error}</div>;
    }

    return (
        <div className="columns is-multiline">
            {stems.map((stem, index) => (
                <div key={index} className="column is-one-quarter">
                    <div className="box thumbnail">
                        <h3 className="title is-5">{stem}</h3>
                        <AudioPlayer src={`/api/download/${stem}`} formats={[{ type: 'audio/mpeg', extension: 'mp3' }]} />
                    </div>
                </div>
            ))}
        </div>
    );
};

export default StemsGrid;