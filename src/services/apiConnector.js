import axios from 'axios';

export const apiConnector = (method, url, bodyData = null, headers = null, params = null) => {
  return axios.create({ withCredentials: true })({
    method,
    url,
    data: bodyData,
    headers,
    params,
  });
};
