import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const delayDebounceFn = setTimeout(() => {
            if (query) {
                setLoading(true);
                onSearch(query)
                    .then(() => setLoading(false))
                    .catch((err) => {
                        setLoading(false);
                        setError('Error occurred during search');
                        console.error(err);
                    });
            }
        }, 500);

        return () => clearTimeout(delayDebounceFn);
    }, [query, onSearch]);

    const handleClear = () => {
        setQuery('');
        setError('');
    };

    return (
        <div className="field">
            <div className="control has-icons-left">
                <input
                    className="input is-primary is-medium"
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search stems..."
                    style={{ borderRadius: '25px' }}
                />
                <span className="icon is-left">
                    <i className="fas fa-search"></i>
                </span>
            </div>
            <div className="control mt-2">
                <button className="button is-light is-medium" onClick={handleClear} style={{ borderRadius: '25px' }}>
                    Clear
                </button>
            </div>
            {loading && <p className="help is-info">Loading...</p>}
            {error && <p className="help is-danger">{error}</p>}
        </div>
    );
};

SearchBar.propTypes = {
    onSearch: PropTypes.func.isRequired,
};

export default SearchBar;