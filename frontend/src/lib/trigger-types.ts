export interface TriggerRead {
  id: number;
  name: string;
  trigger_type: string;
  description: string | null;
  condition_expression: string | null;
  delay_minutes: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TriggerCreatePayload {
  name: string;
  trigger_type: string;
  description?: string | null;
  condition_expression?: string | null;
  delay_minutes?: number;
  is_active?: boolean;
}