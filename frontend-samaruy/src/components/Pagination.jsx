import PropTypes from 'prop-types';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
    const pages = [];
    const maxPagesToShow = 5;

    if (totalPages <= maxPagesToShow) {
        for (let i = 1; i <= totalPages; i++) {
            pages.push(i);
        }
    } else {
        if (currentPage <= 3) {
            pages.push(1, 2, 3, 4, '...', totalPages);
        } else if (currentPage >= totalPages - 2) {
            pages.push(1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
        } else {
            pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages);
        }
    }

    return (
        <nav className="pagination is-centered" role="navigation" aria-label="pagination">
            <button className="pagination-previous" onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 1} style={{ marginRight: '10px' }}>
                Previous
            </button>
            <button className="pagination-next" onClick={() => onPageChange(currentPage + 1)} disabled={currentPage === totalPages} style={{ marginLeft: '10px' }}>
                Next
            </button>
            <ul className="pagination-list">
                {pages.map((page, index) =>
                    page === '...' ? (
                        <li key={`ellipsis-${index}`}><span className="pagination-ellipsis">&hellip;</span></li>
                    ) : (
                        <li key={page}>
                            <button
                                className={`pagination-link ${page === currentPage ? 'is-current' : ''}`}
                                onClick={() => onPageChange(page)}
                                aria-label={`Goto page ${page}`}
                                style={{ margin: '0 5px' }}
                            >
                                {page}
                            </button>
                        </li>
                    )
                )}
            </ul>
        </nav>
    );
};

Pagination.propTypes = {
    currentPage: PropTypes.number.isRequired,
    totalPages: PropTypes.number.isRequired,
    onPageChange: PropTypes.func.isRequired,
};

export default Pagination;