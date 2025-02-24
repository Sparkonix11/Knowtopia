import axios from 'axios';

const apiConnector = (method, url, bodyData = null, headers = null, params = null) => {
  return axios({
    method,
    url,
    data: bodyData,
    headers,
    params,
    withCredentials: true
  });
};

export default apiConnector;