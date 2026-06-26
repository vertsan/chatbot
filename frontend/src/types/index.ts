export interface User {
  id: string;
  email: string;
  display_name: string;
  avatar_url: string | null;
  email_verified: boolean;
  is_superuser: boolean;
  two_factor_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface Chat {
  id: string;
  title: string;
  model_id: string | null;
  system_prompt: string | null;
  temperature: number | null;
  top_p: number | null;
  max_tokens: number | null;
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: string;
  chat_id: string;
  user_id: string;
  title: string;
  status: "active" | "archived" | "deleted";
  model_id: string | null;
  system_prompt: string | null;
  temperature: number | null;
  top_p: number | null;
  max_tokens: number | null;
  token_count: number;
  message_count: number;
  summary: string | null;
  last_message_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  model_id: string | null;
  provider_id: string | null;
  tool_calls: unknown[] | null;
  tool_call_id: string | null;
  input_tokens: number | null;
  output_tokens: number | null;
  total_tokens: number | null;
  latency_ms: number | null;
  finish_reason: string | null;
  created_at: string;
  parent_id: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface AIProvider {
  id: string;
  name: string;
  provider_type: string;
  api_base_url: string | null;
  is_active: boolean;
  is_default: boolean;
  config: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface AIModel {
  id: string;
  provider_id: string;
  name: string;
  model_id: string;
  version: string | null;
  description: string | null;
  max_tokens: number | null;
  context_length: number | null;
  supports_streaming: boolean;
  supports_tools: boolean;
  supports_vision: boolean;
  supports_embeddings: boolean;
  supports_json_mode: boolean;
  is_active: boolean;
  is_default: boolean;
}

export interface KnowledgeBase {
  id: string;
  name: string;
  description: string | null;
  user_id: string;
  embedding_model: string;
  chunk_size: number;
  chunk_overlap: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Document_ {
  id: string;
  knowledge_base_id: string;
  file_name: string;
  file_size: number;
  mime_type: string;
  document_type: string;
  status: "pending" | "processing" | "ready" | "error";
  chunk_count: number;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface StreamChunk {
  content: string;
  done: boolean;
  finish_reason: string | null;
  input_tokens: number | null;
  output_tokens: number | null;
}
