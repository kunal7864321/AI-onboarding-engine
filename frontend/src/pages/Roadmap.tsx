import React, { useState } from 'react';
import { useStore } from '../store/useStore';
import { Link } from 'react-router-dom';
import { Clock, ChevronDown, ChevronUp, Zap, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const Roadmap: React.FC = () => {
  const { roadmap, analysis } = useStore();
  const [expandedStep, setExpandedStep] = useState<number | null>(null);
  const [fastTrack, setFastTrack] = useState(false);
  
  if (!roadmap || !analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No roadmap available. Please complete analysis first.</p>
        <Link to="/" className="btn-primary mt-4 inline-block">
          Go to Upload
        </Link>
      </div>
    );
  }
  
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'advanced': return 'bg-red-100 text-red-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-green-100 text-green-800';
    }
  };
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Learning Roadmap</h1>
          <p className="text-gray-600 mt-1">Target Role: {roadmap.target_role}</p>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setFastTrack(!fastTrack)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              fastTrack ? 'bg-accent-100 text-accent-800' : 'bg-gray-100 text-gray-800'
            }`}
          >
            <Zap className="h-4 w-4" />
            <span>Fast Track</span>
          </button>
          <Link to="/skill-gap" className="btn-secondary">
            View Analysis
          </Link>
        </div>
      </div>
      
      <div className="grid md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card bg-gradient-to-br from-primary-500 to-primary-600 text-white"
        >
          <p className="text-sm opacity-80">Total Skills</p>
          <p className="text-4xl font-bold">{roadmap.learning_path?.length || 0}</p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card bg-gradient-to-br from-accent-500 to-accent-600 text-white"
        >
          <p className="text-sm opacity-80">Est. Hours</p>
          <p className="text-4xl font-bold">{roadmap.estimated_total_hours?.toFixed(0) || 0}h</p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card bg-gradient-to-br from-green-500 to-green-600 text-white"
        >
          <p className="text-sm opacity-80">Milestones</p>
          <p className="text-4xl font-bold">{roadmap.milestones?.length || 0}</p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white"
        >
          <p className="text-sm opacity-80">Courses</p>
          <p className="text-4xl font-bold">
            {roadmap.learning_path?.reduce((acc, step) => acc + (step.courses?.length || 0), 0) || 0}
          </p>
        </motion.div>
      </div>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <h2 className="section-title">Learning Path</h2>
          <div className="space-y-4">
            {roadmap.learning_path?.map((step, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className={`card cursor-pointer transition-all ${
                  expandedStep === idx ? 'ring-2 ring-primary-500' : ''
                }`}
                onClick={() => setExpandedStep(expandedStep === idx ? null : idx)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                      <span className="text-primary-700 font-bold">{step.order}</span>
                    </div>
                      <div>
                      <h3 className="font-semibold text-gray-900 text-lg">{step.skill}</h3>
                      <div className="flex items-center space-x-3 mt-1">
                        <span className={`badge ${getDifficultyColor(step.difficulty || 'intermediate')}`}>
                          {step.difficulty || 'intermediate'}
                        </span>
                        <span className="flex items-center text-sm text-gray-600">
                          <Clock className="h-4 w-4 mr-1" />
                          {step.estimated_hours}h
                        </span>
                        {step.prerequisites_met ? (
                          <span className="flex items-center text-sm text-green-600">
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Ready
                          </span>
                        ) : (
                          <span className="flex items-center text-sm text-yellow-600">
                            Dependencies pending
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  {expandedStep === idx ? (
                    <ChevronUp className="h-5 w-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="h-5 w-5 text-gray-400" />
                  )}
                </div>
                
                {expandedStep === idx && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mt-4 pt-4 border-t border-gray-200"
                  >
                    <p className="text-sm text-gray-700 mb-4">{step.reasoning}</p>
                    
                    {step.dependencies && step.dependencies.length > 0 && (
                      <div className="mb-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Dependencies:</p>
                        <div className="flex flex-wrap gap-2">
                          {step.dependencies.map((dep, depIdx) => (
                            <span key={depIdx} className="badge bg-gray-100 text-gray-800">
                              {dep}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-3">Recommended Courses:</p>
                      <div className="space-y-3">
                        {step.courses?.map((course, courseIdx) => (
                          <div key={courseIdx} className="bg-gray-50 rounded-lg p-4">
                            <div className="flex justify-between items-start">
                              <div>
                                <p className="font-medium text-gray-900">{course.title}</p>
                                <p className="text-sm text-gray-600">{course.provider}</p>
                              </div>
                              <div className="text-right">
                                <p className="text-sm font-medium text-primary-600">{course.duration_hours}h</p>
                                <p className="text-xs text-gray-500">{course.level}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
        
        <div>
          <h2 className="section-title">Milestones</h2>
          <div className="space-y-4">
            {roadmap.milestones?.map((milestone, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="card"
              >
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-8 h-8 bg-accent-100 rounded-full flex items-center justify-center">
                    <span className="text-accent-700 font-bold">{milestone.order + 1}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900">{milestone.title}</h3>
                </div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {milestone.skills?.map((skill, skillIdx) => (
                    <span key={skillIdx} className="badge bg-primary-50 text-primary-700">
                      {skill}
                    </span>
                  ))}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Clock className="h-4 w-4 mr-1" />
                  {milestone.estimated_hours.toFixed(0)} hours
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Roadmap;
