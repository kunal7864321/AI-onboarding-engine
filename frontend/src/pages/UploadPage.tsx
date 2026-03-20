import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload as UploadIcon, FileText, Briefcase, ArrowRight, Loader2, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { useStore } from '../store/useStore';
import { uploadDocuments, analyzeDocuments, generateRoadmap } from '../utils/api';

const UploadPage: React.FC = () => {
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<File | null>(null);
  const [email, setEmail] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  const navigate = useNavigate();
  const { setSessionId, setAnalysis, setRoadmap, setError } = useStore();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!resume || !jobDescription) {
      setError('Please upload both resume and job description');
      return;
    }
    
    setIsUploading(true);
    setIsAnalyzing(true);
    setError(null);
    
    try {
      console.log('Starting upload...');
      
      const uploadResponse = await uploadDocuments(resume, jobDescription, email || undefined);
      console.log('Upload complete:', uploadResponse);
      setSessionId(uploadResponse.session_id);
      
      await new Promise(resolve => setTimeout(resolve, 500));
      
      console.log('Starting analysis...');
      const analysisResponse = await analyzeDocuments(uploadResponse.session_id);
      console.log('Analysis complete:', analysisResponse);
      setAnalysis(analysisResponse);
      
      console.log('Generating roadmap...');
      const roadmapResponse = await generateRoadmap(uploadResponse.session_id);
      console.log('Roadmap complete:', roadmapResponse);
      setRoadmap(roadmapResponse);
      
      console.log('Navigating to dashboard...');
      navigate('/dashboard');
    } catch (err: any) {
      console.error('Full error object:', err);
      console.error('Error response:', err.response);
      console.error('Error message:', err.message);
      if (err.response) {
        console.error('Status:', err.response.status);
        console.error('Data:', err.response.data);
      }
      setError(err.response?.data?.detail || err.message || 'An error occurred during analysis');
    } finally {
      setIsUploading(false);
      setIsAnalyzing(false);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-6">
          <Sparkles className="h-8 w-8 text-primary-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI-Adaptive Onboarding Engine
        </h1>
        <p className="text-xl text-gray-600">
          Upload your resume and target job description to get a personalized learning roadmap
        </p>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card"
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FileText className="inline-block h-4 w-4 mr-2" />
                Resume (PDF, TXT)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-500 transition-colors">
                <div className="space-y-1 text-center">
                  {resume ? (
                    <div className="text-primary-600">
                      <FileText className="mx-auto h-12 w-12" />
                      <p className="mt-2 text-sm">{resume.name}</p>
                    </div>
                  ) : (
                    <>
                      <UploadIcon className="mx-auto h-12 w-12 text-gray-400" />
                      <div className="flex text-sm text-gray-600 justify-center mt-2">
                        <label className="relative cursor-pointer rounded-md font-medium text-primary-600 hover:text-primary-500">
                          <span>Upload a file</span>
                          <input
                            type="file"
                            className="sr-only"
                            accept=".pdf,.txt"
                            onChange={(e) => setResume(e.target.files?.[0] || null)}
                          />
                        </label>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Briefcase className="inline-block h-4 w-4 mr-2" />
                Job Description (PDF, TXT)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-500 transition-colors">
                <div className="space-y-1 text-center">
                  {jobDescription ? (
                    <div className="text-primary-600">
                      <FileText className="mx-auto h-12 w-12" />
                      <p className="mt-2 text-sm">{jobDescription.name}</p>
                    </div>
                  ) : (
                    <>
                      <UploadIcon className="mx-auto h-12 w-12 text-gray-400" />
                      <div className="flex text-sm text-gray-600 justify-center mt-2">
                        <label className="relative cursor-pointer rounded-md font-medium text-primary-600 hover:text-primary-500">
                          <span>Upload a file</span>
                          <input
                            type="file"
                            className="sr-only"
                            accept=".pdf,.txt"
                            onChange={(e) => setJobDescription(e.target.files?.[0] || null)}
                          />
                        </label>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email (Optional)
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
              placeholder="your.email@example.com"
            />
          </div>
          
          <button
            type="submit"
            disabled={isUploading || !resume || !jobDescription}
            className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <span>Analyze & Generate Roadmap</span>
                <ArrowRight className="h-5 w-5" />
              </>
            )}
          </button>
        </form>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="mt-8 grid md:grid-cols-3 gap-6"
      >
        {[
          { title: 'Smart Analysis', desc: 'AI-powered skill extraction' },
          { title: 'Gap Detection', desc: 'Identify learning needs' },
          { title: 'Adaptive Paths', desc: 'Personalized roadmaps' },
        ].map((feature, idx) => (
          <div key={idx} className="bg-white/50 backdrop-blur rounded-lg p-6 text-center">
            <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
            <p className="text-sm text-gray-600">{feature.desc}</p>
          </div>
        ))}
      </motion.div>
    </div>
  );
};

export default UploadPage;
