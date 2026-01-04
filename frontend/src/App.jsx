import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import { TryOnPage } from './components/virtual';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/try-on" element={<TryOnPage />} />
      </Routes>
    </Router>
  );
}

export default App;