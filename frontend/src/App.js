import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './Home';
import VirusPage from './Virus';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/virus" element={<VirusPage />} />
            </Routes>
        </Router>
    );
}

export default App;
