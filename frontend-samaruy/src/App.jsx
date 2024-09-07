import {Route, Routes} from 'react-router-dom';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import SearchResultsPage from './pages/SearchResultsPage';
import StemDetailPage from './pages/StemDetailPage';
import SampleLibraryPage from "./pages/SampleLibraryPage";
import './App.css';

const App = () => {
    return (
        <Routes>
            <Route path="/" element={<HomePage/>}/>
            <Route path="/upload" element={<UploadPage/>}/>
            <Route path="/search" element={<SearchResultsPage/>}/>
            <Route path="/stems/:stemId" element={<StemDetailPage/>}/>
            <Route path="/sample-library" element={<SampleLibraryPage/>}/>
        </Routes>
    );
};

export default App;