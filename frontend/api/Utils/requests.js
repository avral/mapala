import axios from 'axios'
// import jsonp from 'jsonp'

// const version = require('../../package.json').version
// if (process.env.NODE_ENV === 'production') {
  // const API_URL = 'http://alfa.mapala.net/api/v1/site/auction?user=dark.sun'
// } else {
  // const API_URL = '/api/v1/site/auction?user=dark.sun '
// }
// const USER_AGENT = `${require('../../package.json').name} ${version}`

const API_URL = '/api/v1/site'

/**
 * Make Api
 * @param  {Array}    options   request options
 * @param  {Function} callback
 * @return {Json}               return Json response from Api server
 */
function _request(method, endpoint, parameters, callback) {
  var opt = {
    method: method,
    baseURL: API_URL,
    url: endpoint,
    crossDomain: true,
    headers: {
      // 'User-Agent': USER_AGENT,
    },
    timeout: 10000,
    params: parameters,
    responseType: 'json',
  }

  axios(opt)
  .then(response => {
    callback(response.data)
  })
  .catch(error => {
    var err = error.response
    callback(err)
  })
  // jsonp('http://alfa.mapala.net/api/v1/site/auction?user=dark.sun', null, callback)
  //   .then (response => {
  //     callback(response.data)
  //   })
  //   .catch(error => {
  //     var err = error.response
  //     callback(err)
  //   })
}

/**
 * Make GET Api request
 * @param  {String}   endpoint     Api endpoint (endpoint)
 * @param  {Array}    parameters  GET request query parameters
 * @param  {Function} callback
 * @return {Json}                 return Json response from public api request
 */
export function _get(endpoint, parameters, callback) {
  return _request('GET', endpoint, parameters, callback)
}

/**
 * Make POST Api request
 * @param  {String}   endpoint     Api endpoint (endpoint)
 * @param  {Array}    parameters  GET request query parameters
 * @param  {Function} callback
 * @return {Json}                 return Json response from public api request
 */
export function _post(endpoint, parameters, callback) {
  return _request('POST', endpoint, parameters, callback)
}