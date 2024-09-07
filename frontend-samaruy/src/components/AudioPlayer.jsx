import PropTypes from 'prop-types';

const AudioPlayer = ({ src, formats }) => {
  return (
    <div className="box">
      <audio controls className="is-fullwidth">
        {formats.map((format) => (
          <source key={format.type} src={`${src}.${format.extension}`} type={format.type} />
        ))}
        Your browser does not support the audio element.
      </audio>
    </div>
  );
};

AudioPlayer.propTypes = {
  src: PropTypes.string.isRequired,
  formats: PropTypes.arrayOf(
    PropTypes.shape({
      type: PropTypes.string.isRequired,
      extension: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default AudioPlayer;