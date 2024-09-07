import PropTypes from 'prop-types';
import AudioPlayer from './AudioPlayer';
import { downloadStem } from '../api/api';

const StemsList = ({ stems = [] }) => {
  const handleDownload = async (fileName) => {
    try {
      const data = await downloadStem(fileName);
      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url); // Clean up the URL object
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  return (
    <div>
      {stems.length > 0 ? (
        stems.map((stem) => (
          <div key={stem.id} className="box">
            <h3 className="title is-4">{stem.name}</h3>
            <AudioPlayer src={stem.url} formats={[{ type: 'audio/mpeg', extension: 'mp3' }]} />
            <button className="button is-primary mt-2" onClick={() => handleDownload(stem.name)}>Download</button>
          </div>
        ))
      ) : (
        <p className="notification is-warning" style={{ padding: '10px', margin: '20px 0' }}>No stems available.</p>
      )}
    </div>
  );
};

StemsList.propTypes = {
  stems: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default StemsList;