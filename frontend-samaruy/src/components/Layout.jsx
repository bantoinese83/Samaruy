import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome } from '@fortawesome/free-solid-svg-icons';
import Footer from './Footer';

const Layout = ({ children, isHomePage = false }) => {
    return (
        <div className="layout-container">
            <section className="hero">
                <div className="hero-body">
                    <div className="container has-text-centered">
                        {children}
                    </div>
                </div>
            </section>
            {!isHomePage && (
                <div className="home-icon">
                    <Link to="/">
                        <FontAwesomeIcon icon={faHome} className="mr-2" />
                    </Link>
                </div>
            )}
            {isHomePage && <Footer />}
        </div>
    );
};

Layout.propTypes = {
    children: PropTypes.node.isRequired,
    isHomePage: PropTypes.bool
};

export default Layout;