import {_get} from '../Utils/requests'

/**
 * Get ICO auction data
 * @param  {String}			block hash signature
 * @param  {Function} callback
 * @return {Json}
 */
export function auction(user, callback) {
  let parameters = {
    // user: 'dark.sun'
  	user: user
  }
  // var endpoint = 'auction'
  var endpoint = '/auction'
  return _get(endpoint, parameters, callback)
}

/**
 * Get investors data
 * @param  {Function} callback
 * @return {json}
 */
export function investors(callback) {
	let parameters = {}
	var endpoint = 'investors'
  	return _get(endpoint, parameters, callback)
}

/**
 * Get user wallet data
 * @param  {string} 	user
 * @param  {Function} 	callback
 * @return {json}
 */
export function wallet(user, callback) {
	let parameters = {
		user: user
	}
	var endpoint = 'personal_info'
  	return _get(endpoint, parameters, callback)
}