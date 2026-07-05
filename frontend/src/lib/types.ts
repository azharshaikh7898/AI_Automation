export type RoleName = "Admin" | "Manager" | "Sales Executive";

export interface AuthenticatedUser {
  id: number;
  role_id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string | null;
  is_active: boolean;
  is_superuser: boolean;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}

export interface AuthResponse {
  user: AuthenticatedUser;
  tokens: TokenPair;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload extends LoginPayload {
  first_name: string;
  last_name: string;
  phone_number?: string | null;
  role_name?: RoleName;
}

export interface CustomerRead {
  id: number;
  assigned_user_id: number | null;
  first_name: string;
  last_name: string;
  email: string | null;
  phone_number: string | null;
  company_name: string | null;
  status: string;
  source: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreatePayload {
  first_name: string;
  last_name: string;
  email?: string | null;
  phone_number?: string | null;
  company_name?: string | null;
  assigned_user_id?: number | null;
  status?: string;
  source?: string | null;
  notes?: string | null;
}

export interface ProductRead {
  id: number;
  name: string;
  sku: string;
  description: string | null;
  unit_price: string;
  stock_quantity: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCreatePayload {
  name: string;
  sku: string;
  description?: string | null;
  unit_price: string;
  stock_quantity?: number;
  is_active?: boolean;
}

export interface OrderItemRead {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  unit_price: string;
  line_total: string;
  created_at: string;
  updated_at: string;
}

export interface OrderItemCreatePayload {
  product_id: number;
  quantity: number;
  unit_price?: string | null;
}

export interface OrderRead {
  id: number;
  customer_id: number;
  created_by_id: number | null;
  order_number: string;
  status: string;
  currency: string;
  total_amount: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
  order_items: OrderItemRead[];
}

export interface OrderCreatePayload {
  customer_id: number;
  created_by_id?: number | null;
  order_number: string;
  status?: string;
  currency?: string;
  notes?: string | null;
  items: OrderItemCreatePayload[];
}

