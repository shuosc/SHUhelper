import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

export const fetch = axios.create({
  // baseURL: process.env.baseUrl,
  headers: {
    'Access-Control-Allow-Origin': '*'
  }
});

const requestSuccess = (req: AxiosRequestConfig) => {
  return req;
};

const requestError = (err: AxiosError) => {
  return Promise.reject(err);
};

const responseSuccess = (res: AxiosResponse) => {
  return Promise.resolve(res);
};

const responseError = (err: AxiosError) => {
  if (err.request.status === 401 || err.request.status === 403) {
    console.log('UNAUTHORIZED');
  }

  return Promise.reject(err);
};

fetch.interceptors.request.use(requestSuccess, requestError);
fetch.interceptors.response.use(responseSuccess, responseError);
