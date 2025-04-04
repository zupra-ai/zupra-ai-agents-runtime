interface AgentModel {
  id: string;
  mrn: string;
  name: string;
  trait_text: string;
  type: string;
  tools_ids: string[];
}

export default AgentModel;
