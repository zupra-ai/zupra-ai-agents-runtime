import axios from "axios";

const BASE_API = "http://127.0.0.1:9000/api";
class RestApiClient {
  static get(url: string) {
    return axios.get(`${BASE_API}${url}`);
  }
}

export default RestApiClient;
