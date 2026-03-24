import axios from 'axios';

// @ts-ignore
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  withCredentials: true,
});

export interface UploadResponse {
  session_id: string;
  status: string;
  message: string;
}

export interface SkillLevel {
  skill: string;
  level: number;
  confidence: number;
  source: string;
}

export interface RequiredSkill {
  skill: string;
  required_level: number;
  importance: number;
  frequency: number;
}

export interface SkillGap {
  skill: string;
  current_level: number;
  required_level: number;
  gap_score: number;
  priority: number;
  reasoning: string;
}

export interface ReasoningStep {
  step_number: number;
  title: string;
  description: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  confidence: number;
}

export interface AnalysisResponse {
  session_id: string;
  status: string;
  user_skills: SkillLevel[];
  required_skills: RequiredSkill[];
  skill_gaps: SkillGap[];
  strong_skills: string[];
  weak_skills: string[];
  reasoning_trace: ReasoningStep[];
  metrics: Record<string, any>;
}

export interface Course {
  title: string;
  provider: string;
  duration_hours: number;
  level: string;
  url?: string;
  is_free?: boolean;
}

export interface LearningStep {
  order: number;
  skill: string;
  target_level: number;
  estimated_hours: number;
  courses: Course[];
  prerequisites_met: boolean;
  reasoning: string;
  dependencies: string[];
  difficulty?: string;
  category?: string;
}

export interface Milestone {
  title: string;
  skills: string[];
  estimated_hours: number;
  order: number;
}

export interface RoadmapResponse {
  session_id: string;
  target_role: string;
  learning_path: LearningStep[];
  milestones: Milestone[];
  estimated_total_hours: number;
  fast_track_available: boolean;
  reasoning_trace: ReasoningStep[];
}

export const uploadDocuments = async (
  resume: File,
  jobDescription: File,
  email?: string
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('resume', resume);
  formData.append('job_description', jobDescription);
  if (email) {
    formData.append('email', email);
  }
  
  const response = await api.post<UploadResponse>('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  
  return response.data;
};

export const analyzeDocuments = async (sessionId: string): Promise<AnalysisResponse> => {
  const response = await api.get<AnalysisResponse>(`/analyze/${sessionId}`);
  return response.data;
};

export const generateRoadmap = async (
  sessionId: string,
  fastTrack: boolean = false
): Promise<RoadmapResponse> => {
  const response = await api.get<RoadmapResponse>(`/roadmap/${sessionId}`, {
    params: { fast_track: fastTrack },
  });
  return response.data;
};

export const updateProgress = async (
  sessionId: string,
  skillName: string,
  completionPercentage: number,
  timeSpentHours?: number,
  assessmentScore?: number
): Promise<any> => {
  const response = await api.post(`/progress/${sessionId}`, {
    skill_name: skillName,
    completion_percentage: completionPercentage,
    time_spent_hours: timeSpentHours,
    assessment_score: assessmentScore,
  });
  return response.data;
};
