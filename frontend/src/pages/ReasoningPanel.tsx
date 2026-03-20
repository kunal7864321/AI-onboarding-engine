import React from 'react';
import { useStore } from '../store/useStore';
import { Link } from 'react-router-dom';
import { Brain, Lightbulb, ChevronRight, CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const ReasoningPanel: React.FC = () => {
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
  
  const steps = analysis.reasoning_trace || [];
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-primary-100 rounded-full">
            <Brain className="h-8 w-8 text-primary-600" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Reasoning Panel</h1>
            <p className="text-gray-600">Step-by-step AI decision explanation</p>
          </div>
        </div>
        <Link to="/roadmap" className="btn-primary flex items-center space-x-2">
          <span>View Roadmap</span>
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
      
      <div className="bg-gradient-to-r from-primary-50 to-accent-50 rounded-xl p-6 border border-primary-200">
        <div className="flex items-start space-x-4">
          <div className="p-2 bg-white rounded-lg shadow-sm">
            <Lightbulb className="h-6 w-6 text-accent-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">How the AI Reasoning Works</h3>
            <p className="text-gray-700 text-sm">
              Our AI system analyzes your resume and job description through multiple stages. 
              Each skill is evaluated based on your current proficiency, job requirements, 
              dependencies, and learning efficiency. The priority score combines these factors 
              to create your personalized learning path.
            </p>
          </div>
        </div>
      </div>
      
      <div className="space-y-4">
        {steps.map((step, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="card"
          >
            <div className="flex items-start space-x-4">
              <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                step.confidence >= 0.8 ? 'bg-green-100' :
                step.confidence >= 0.6 ? 'bg-yellow-100' : 'bg-red-100'
              }`}>
                <span className={`font-bold ${
                  step.confidence >= 0.8 ? 'text-green-700' :
                  step.confidence >= 0.6 ? 'text-yellow-700' : 'text-red-700'
                }`}>
                  {step.step_number}
                </span>
              </div>
              
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 text-lg">{step.title}</h3>
                  <span className={`badge ${
                    step.confidence >= 0.8 ? 'bg-green-100 text-green-800' :
                    step.confidence >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {step.confidence >= 0.8 ? 'High Confidence' :
                     step.confidence >= 0.6 ? 'Medium Confidence' : 'Low Confidence'}
                  </span>
                </div>
                
                <p className="text-gray-700 mb-4">{step.description}</p>
                
                {step.input_data && (
                  <div className="bg-gray-50 rounded-lg p-4 mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-2">
                      <ChevronRight className="inline h-4 w-4 mr-1" />
                      Input Data
                    </p>
                    <div className="grid grid-cols-2 gap-2">
                      {Object.entries(step.input_data).map(([key, value]) => (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-gray-600">{key}:</span>
                          <span className="font-medium text-gray-900">
                            {typeof value === 'number' ? value.toFixed(2) : String(value)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {step.output_data && (
                  <div className="bg-primary-50 rounded-lg p-4">
                    <p className="text-sm font-medium text-primary-700 mb-2">
                      <CheckCircle className="inline h-4 w-4 mr-1" />
                      Output Data
                    </p>
                    <div className="grid grid-cols-2 gap-2">
                      {Object.entries(step.output_data).map(([key, value]) => (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-primary-600">{key}:</span>
                          <span className="font-medium text-primary-900">
                            {typeof value === 'number' ? value.toFixed(2) : String(value)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      
      <div className="card bg-gradient-to-br from-gray-50 to-gray-100">
        <h2 className="section-title">Priority Calculation Formula</h2>
        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <div className="font-mono text-sm space-y-2">
            <p className="text-gray-700">
              <span className="font-bold text-primary-600">final_priority</span> = (
            </p>
            <p className="pl-4 text-gray-600">
              (gap_score <span className="text-gray-400">×</span> 0.40) + 
            </p>
            <p className="pl-4 text-gray-600">
              (importance <span className="text-gray-400">×</span> 0.35) + 
            </p>
            <p className="pl-4 text-gray-600">
              (dependency_satisfaction <span className="text-gray-400">×</span> 0.25)
            </p>
            <p className="text-gray-700">) <span className="text-gray-400">×</span> learning_efficiency</p>
          </div>
        </div>
        <div className="mt-4 flex items-start space-x-3">
          <AlertTriangle className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-gray-700">
            <span className="font-medium">Why this matters:</span> Skills are ranked not just by 
            how much you need to learn, but also by how important they are for the job and 
            whether you have the prerequisites to learn them efficiently.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ReasoningPanel;
