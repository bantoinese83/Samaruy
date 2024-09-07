// HomePage.jsx
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook, faMusic, faSearch } from '@fortawesome/free-solid-svg-icons';
import Layout from '../components/Layout';
import samaruyLogo from '../assets/samaruy-logo.jpeg';
import Loader from '../components/Loader';

const HomePage = () => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate a loading delay
        const timer = setTimeout(() => {
            setLoading(false);
        }, 2000); // Adjust the delay as needed

        return () => clearTimeout(timer);
    }, []);

    if (loading) {
        return <Loader />;
    }

    return (
        <Layout isHomePage={true}>
            <img src={samaruyLogo} alt="Samaruy Logo" className="mb-6"
                 style={{width: '50%', height: 'auto', borderRadius: '10px'}}/>
            <h2 className="subtitle">Separate Audio or Search Stems In Our Extensive Sample Library</h2>
            <p> click on the buttons below to get started</p>
            <div className="buttons is-centered">
                <Link to="/upload" className="button is-primary is-large">
                    <FontAwesomeIcon icon={faMusic} className="mr-2"/>
                    Separate Audio
                </Link>
                <Link to="/search" className="button is-link is-large">
                    <FontAwesomeIcon icon={faSearch} className="mr-2"/>
                    Search Stems
                </Link>
                <Link to="/sample-library" className="button is-info is-large">
                    <FontAwesomeIcon icon={faBook} className="mr-2"/>
                    Sample Library
                </Link>
            </div>
        </Layout>
    );
};

export default HomePage;