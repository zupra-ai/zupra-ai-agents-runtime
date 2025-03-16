import RestApiClient from "./RestApiClient";

class AgentsClient {
  static list() {
    return RestApiClient.get("/agents");
  }
}

export default AgentsClient;
