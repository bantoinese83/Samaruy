import { useState, useEffect } from 'react';
import StemsGrid from '../components/StemsGrid';
import Layout from '../components/Layout';
import Loader from '../components/Loader';

const SampleLibraryPage = () => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate a data fetch
        const fetchData = async () => {
            // Simulate a delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            setLoading(false);
        };

        fetchData().then(r => r);
    }, []);

    return (
        <Layout>
            <h1 className="title">Sample Library</h1>
            {loading ? <Loader /> : <StemsGrid />}
        </Layout>
    );
};

export default SampleLibraryPage;