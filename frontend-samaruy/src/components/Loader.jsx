import { useLottie } from "lottie-react";
import animationData from '../assets/loading_animation.json';

const Loader = () => {
    const options = {
        animationData: animationData,
        loop: true,
        autoplay: true,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice'
        }
    };
    const { View } = useLottie(options);
    return <div className="loader-container">{View}</div>;
};

export default Loader;