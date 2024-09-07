import { useState } from 'react';
import SearchBar from '../components/SearchBar';
import StemsList from '../components/StemsList';
import Pagination from '../components/Pagination';
import Layout from '../components/Layout';
import { searchStems } from '../api/api';
import Loader from '../components/Loader';

const SearchResultsPage = () => {
    const [stems, setStems] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSearch = async (query) => {
        setLoading(true);
        setError('');
        try {
            const response = await searchStems(query, null, currentPage);
            setStems(response.stems || []);
            setTotalPages(response.totalPages || 1);
        } catch (error) {
            setError('Error searching stems. Please try again.');
            console.error('Error searching stems:', error);
        } finally {
            setLoading(false);
        }
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
        handleSearch().then(r => console.log(r));
    };

    return (
        <Layout>
            <h1>Search Stems</h1>
            <p>Search for stems by name and type</p>
            <SearchBar onSearch={handleSearch} />
            {loading ? (
                <Loader />
            ) : (
                <>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <StemsList stems={stems} />
                    <Pagination
                        currentPage={currentPage}
                        totalPages={totalPages}
                        onPageChange={handlePageChange}
                    />
                </>
            )}
        </Layout>
    );
};

export default SearchResultsPage;