export interface TaskRead {
  id: number;
  customer_id: number;
  assigned_user_id: number | null;
  trigger_id: number | null;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  due_date: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCreatePayload {
  customer_id: number;
  assigned_user_id?: number | null;
  trigger_id?: number | null;
  title: string;
  description?: string | null;
  status?: string;
  priority?: string;
  due_date?: string | null;
}