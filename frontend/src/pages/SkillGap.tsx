import React from 'react';
import { useStore } from '../store/useStore';
import { Link } from 'react-router-dom';
import { ArrowRight, AlertTriangle, CheckCircle, TrendingUp, GitBranch } from 'lucide-react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const SkillGap: React.FC = () => {
  const { analysis } = useStore();
  
  if (!analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No analysis data available.</p>
        <Link to="/" className="btn-primary mt-4 inline-block">
          Go to Upload
        </Link>
      </div>
    );
  }
  
  const gapChartData = analysis.skill_gaps?.map(gap => ({
    skill: gap.skill.length > 10 ? gap.skill.substring(0, 10) + '...' : gap.skill,
    current: gap.current_level,
    required: gap.required_level,
    gap: gap.gap_score * 5,
  })) || [];
  
  const radarData = [
    { skill: 'Technical', A: analysis.strong_skills?.length || 0, fullMark: 10 },
    { skill: 'Tools', A: 3, fullMark: 10 },
    { skill: 'Domain', A: 4, fullMark: 10 },
    { skill: 'Soft', A: 5, fullMark: 10 },
  ];
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Skill Gap Analysis</h1>
        <Link to="/reasoning" className="btn-secondary flex items-center space-x-2">
          <span>View AI Reasoning</span>
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
      
      <div className="grid md:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card bg-gradient-to-br from-red-50 to-red-100 border border-red-200"
        >
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-red-200 rounded-full">
              <AlertTriangle className="h-6 w-6 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-red-800">Missing Skills</p>
              <p className="text-3xl font-bold text-red-900">
                {analysis.skill_gaps?.filter(g => g.gap_score >= 1.0).length || 0}
              </p>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card bg-gradient-to-br from-yellow-50 to-yellow-100 border border-yellow-200"
        >
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-yellow-200 rounded-full">
              <TrendingUp className="h-6 w-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-sm text-yellow-800">Weak Skills</p>
              <p className="text-3xl font-bold text-yellow-900">
                {analysis.weak_skills?.length || 0}
              </p>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card bg-gradient-to-br from-green-50 to-green-100 border border-green-200"
        >
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-green-200 rounded-full">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-green-800">Strong Skills</p>
              <p className="text-3xl font-bold text-green-900">
                {analysis.strong_skills?.length || 0}
              </p>
            </div>
          </div>
        </motion.div>
      </div>
      
      <div className="grid md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h2 className="section-title">Skill Levels Comparison</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={gapChartData}>
                <XAxis dataKey="skill" />
                <YAxis domain={[0, 5]} />
                <Tooltip />
                <Bar dataKey="current" name="Current" fill="#10b981" />
                <Bar dataKey="required" name="Required" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <h2 className="section-title">Skill Radar</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="skill" />
                <PolarRadiusAxis domain={[0, 10]} />
                <Radar name="Your Skills" dataKey="A" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card"
      >
        <div className="flex items-center space-x-2 mb-4">
          <GitBranch className="h-5 w-5 text-primary-600" />
          <h2 className="section-title mb-0">Detailed Gap Analysis</h2>
        </div>
        <div className="space-y-4">
          {analysis.skill_gaps?.map((gap, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{gap.skill}</h3>
                  <p className="text-sm text-gray-600 mt-1">{gap.reasoning}</p>
                </div>
                <span className={`badge ${
                  gap.gap_score >= 0.8 ? 'bg-red-100 text-red-800' :
                  gap.gap_score >= 0.5 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  Priority: {(gap.priority * 100).toFixed(0)}%
                </span>
              </div>
              <div className="flex items-center space-x-4 mt-3">
                <div className="flex-1">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Current Level</span>
                    <span className="font-medium">{gap.current_level.toFixed(1)}/5</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${(gap.current_level / 5) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Required Level</span>
                    <span className="font-medium">{gap.required_level.toFixed(1)}/5</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${(gap.required_level / 5) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default SkillGap;
