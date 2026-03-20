import { Routes, Route } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import Dashboard from './pages/Dashboard';
import SkillGap from './pages/SkillGap';
import Roadmap from './pages/Roadmap';
import ReasoningPanel from './pages/ReasoningPanel';
import Layout from './components/Layout';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<UploadPage />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="skill-gap" element={<SkillGap />} />
        <Route path="roadmap" element={<Roadmap />} />
        <Route path="reasoning" element={<ReasoningPanel />} />
      </Route>
    </Routes>
  );
}

export default App;
