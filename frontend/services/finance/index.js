
//import { ls } from '../services'

/**
 * Responsible for all HTTP requests.
 */
// import http from '../services'

export default {

  getCurrency(context){
    // console.log('get SBD!!!!')
    //Ходит и получает данные для конвертации Валюты постов
    //this.http.
    context.$http.jsonp('http://data-asg.goldprice.org/GetData/RUB-XAU/1' , {
        client_id: 'xxxxxxxxxxxxxxxxxxxxxxxx'
    }, function(data){
      // console.log('DATA!!!!!',data)
      var result=data[0].replace('RUB-XAU,','')
      var x=parseFloat(Math.round(result / 31.1034768 / 1000).toFixed(2))
      context.currency_sbd=x
      //console.log('!SET',context.finances.currency_sbd)
    }, {
        'jsonp': 'callback'
    });
  },
  init () {
  }
}
