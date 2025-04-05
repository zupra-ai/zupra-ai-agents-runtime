interface LLMProvider {
  name: string;
  description: string;
  api_key: string;
}

export interface LLMProviderModel {
  id: string;
  name: string;
  description: string;
  api_key: string;
  created_at: Date;
  updated_at: Date;
}
const llmSettings: LLMProvider[] = [
  {
    name: "OpenAI",
    description: "OpenAI API",
    api_key: "$OPEN_API_KEY",
  },
];

export default llmSettings;
