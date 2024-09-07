import {useEffect, useState} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faFacebookF, faInstagram, faTelegram, faTwitter, faYoutube} from '@fortawesome/free-brands-svg-icons';
import StemsGrid from './StemsGrid';

const Footer = () => {
    const [dateTime, setDateTime] = useState(new Date());
    const [location, setLocation] = useState(null);

    useEffect(() => {
        const timer = setInterval(() => {
            setDateTime(new Date());
        }, 1000);

        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const {latitude, longitude} = position.coords;
                    try {
                        const response = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`);
                        const data = await response.json();
                        setLocation(`${data.city}, ${data.principalSubdivision}`);
                    } catch (error) {
                        console.error("Error getting location: ", error);
                        setLocation("Location not available");
                    }
                },
                (error) => {
                    console.error("Error getting location: ", error);
                    setLocation("Location not available");
                }
            );
        } else {
            setLocation("Geolocation not supported");
        }
    }, []);

    return (
        <div className="page-wrapper">
            <div id="waterdrop"></div>
            <footer className="footer">
                <div className="footer-top">
                    <div className="pt-exebar"></div>
                    <div className="container">
                        <div className="columns">
                            <div className="column is-half">
                                <div className="widget">
                                    <h5 className="footer-title">Email Us</h5>
                                    <div className="textwidget">
                                        <div role="form" className="wpcf7" id="wpcf7-f4-o1" lang="en-US" dir="ltr">
                                            <form method="post" className="wpcf7-form" noValidate="novalidate">
                                                <div className="contact-form-footer">
                                                    <p>
                                                        <span className="wpcf7-form-control-wrap your-first-name">
                                                            <input type="text" name="your-first-name" size="40"
                                                                   className="input" aria-invalid="false"
                                                                   placeholder="Your name"/>
                                                        </span>
                                                    </p>
                                                    <p>
                                                        <span className="wpcf7-form-control-wrap your-email_1">
                                                            <input type="email" name="your-email_1" size="40"
                                                                   className="input" aria-invalid="false"
                                                                   placeholder="Your email"/>
                                                        </span>
                                                    </p>
                                                    <p>
                                                        <span className="wpcf7-form-control-wrap your-message">
                                                            <textarea name="your-message" cols="40" rows="10"
                                                                      className="textarea" aria-invalid="false"
                                                                      placeholder="Your message"></textarea>
                                                        </span>
                                                    </p>
                                                    <div>
                                                        <input type="submit" value="Send"
                                                               className="button is-primary"/>
                                                        <span className="ajax-loader"></span>
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="column is-one-quarter">
                                <div className="widget widget_gallery gallery-grid-4">
                                    <h5 className="footer-title">Sample Library</h5>
                                    <StemsGrid/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="footer-bottom">
                    <div className="container">
                            <div id="footer-socials">
                                <div className="socials inline-inside socials-colored">
                                    <a href="#" target="_blank" title="Facebook" className="socials-item">
                                        <FontAwesomeIcon icon={faFacebookF} className="facebook"/>
                                    </a>
                                    <a href="#" target="_blank" title="Twitter" className="socials-item">
                                        <FontAwesomeIcon icon={faTwitter} className="twitter"/>
                                    </a>
                                    <a href="#" target="_blank" title="Instagram" className="socials-item">
                                        <FontAwesomeIcon icon={faInstagram} className="instagram"/>
                                    </a>
                                    <a href="#" target="_blank" title="YouTube" className="socials-item">
                                        <FontAwesomeIcon icon={faYoutube} className="youtube"/>
                                    </a>
                                    <a href="#" target="_blank" title="Telegram" className="socials-item">
                                        <FontAwesomeIcon icon={faTelegram} className="telegram"/>
                                    </a>
                                </div>
                            </div>
                        <div className="footer-bottom-right">
                            <p>{dateTime.toLocaleString()}</p>
                            {location && <p>{location}</p>}
                            <p>&copy; 2024 Samaruy</p>

                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Footer;