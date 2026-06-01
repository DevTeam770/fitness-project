export interface User {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
}

export interface Exercise {
  id: number;
  name: string;
  target_muscle: string;
  gif_url?: string;
}

export interface WorkoutLog {
  id: number;
  session_id: number;
  exercise_id: number;
  set_number: number;
  weight: number;
  reps: number;
  timestamp: string;
}

export interface WorkoutSession {
  id: number;
  user_id: number;
  template_id?: number;
  start_time: string;
  end_time?: string;
  is_completed: boolean;
  logs: WorkoutLog[];
}

export interface VolumeHistoryPoint {
  date: string;
  total_volume: number;
}

export interface ExerciseAnalytics {
  exercise_id: number;
  exercise_name: string;
  personal_record: number;
  volume_history: VolumeHistoryPoint[];
}