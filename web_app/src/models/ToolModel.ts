interface ToolModel {
  id: string;
  name: string;
  description: string;
  runtime: string;
  hash: string;
  organization_id: string;
  tag_name: string;
  body?: string;
  updated_at: string; // or Date if you prefer to parse it
}

export default ToolModel;
