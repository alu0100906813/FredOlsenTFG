
import axios from 'axios';

//const axios = require('axios');

export const GET = (url, params, callback) => {
  return axios.get(url, params)
  .then(function (response) {
    if (callback) {
      callback(response);
    }
  })
  .catch(function (error) {
    console.log(error);
  });
}