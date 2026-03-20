import React from 'react';
import { useStore } from '../store/useStore';
import { TrendingUp, Target, Clock, ArrowRight, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard: React.FC = () => {
  const { analysis, roadmap } = useStore();
  
  if (!analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No analysis data available. Please upload documents first.</p>
        <Link to="/" className="btn-primary mt-4 inline-block">
          Go to Upload
        </Link>
      </div>
    );
  }
  
  const skillGapData = [
    { name: 'Strong', value: analysis.strong_skills?.length || 0, color: '#10b981' },
    { name: 'Weak', value: analysis.weak_skills?.length || 0, color: '#f59e0b' },
    { name: 'Missing', value: analysis.skill_gaps?.filter(g => g.gap_score >= 1.0).length || 0, color: '#ef4444' },
  ];
  
  const priorityData = analysis.skill_gaps?.slice(0, 5).map(gap => ({
    skill: gap.skill.length > 15 ? gap.skill.substring(0, 15) + '...' : gap.skill,
    priority: Math.round(gap.priority * 100),
  })) || [];
  
  const metrics = [
    {
      label: 'Skills Gap',
      value: analysis.skill_gaps?.length || 0,
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      label: 'Strong Skills',
      value: analysis.strong_skills?.length || 0,
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      label: 'Coverage',
      value: `${analysis.metrics?.coverage_percentage?.toFixed(1) || 0}%`,
      icon: Target,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      label: 'Est. Hours',
      value: roadmap?.estimated_total_hours?.toFixed(0) || 0,
      icon: Clock,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ];
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Analysis Dashboard</h1>
        <Link to="/roadmap" className="btn-primary flex items-center space-x-2">
          <span>View Roadmap</span>
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
      
      <div className="grid md:grid-cols-4 gap-6">
        {metrics.map((metric, idx) => {
          const Icon = metric.icon;
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: idx * 0.1 }}
              className="card"
            >
              <div className="flex items-center space-x-4">
                <div className={`p-3 rounded-lg ${metric.bgColor}`}>
                  <Icon className={`h-6 w-6 ${metric.color}`} />
                </div>
                <div>
                  <p className="text-sm text-gray-600">{metric.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
      
      <div className="grid md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <h2 className="section-title">Skill Distribution</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={skillGapData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {skillGapData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <h2 className="section-title">Top Priority Skills</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priorityData} layout="vertical">
                <XAxis type="number" domain={[0, 100]} />
                <YAxis type="category" dataKey="skill" width={100} />
                <Tooltip />
                <Bar dataKey="priority" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="card"
      >
        <h2 className="section-title">Your Strong Skills</h2>
        <div className="flex flex-wrap gap-2">
          {analysis.strong_skills?.map((skill, idx) => (
            <span
              key={idx}
              className="badge bg-green-100 text-green-800"
            >
              {skill}
            </span>
          ))}
        </div>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="card"
      >
        <h2 className="section-title">Skills Needing Improvement</h2>
        <div className="space-y-3">
          {analysis.skill_gaps?.slice(0, 5).map((gap, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium text-gray-900">{gap.skill}</p>
                <p className="text-sm text-gray-600">
                  Current: {gap.current_level.toFixed(1)} → Required: {gap.required_level.toFixed(1)}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full"
                    style={{ width: `${(gap.current_level / 5) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-primary-600">
                  {(gap.priority * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
