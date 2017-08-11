import Vue from 'vue'

import showdown from 'showdown'
var converter = new showdown.Converter({
  simplifiedAutoLink: true,
  tables: true
})

Vue.filter('markdown', function (str) {
  return converter.makeHtml(str)
})

var transliterate = (
  function() {
    var
      rus = "щ    ш  ч  ц  й  ё  э  ю  я  х  ж  а б в г д е з и к л м н о п р с т у ф ъ  ы ь".split(/ +/g),
      eng = "shch sh ch cz ij yo ye yu ya kh zh a b v g d e z i k l m n o p r s t u f xx y x".split(/ +/g)
    ;
    return function(text, engToRus) {
      var x;
      for(x = 0; x < rus.length; x++) {
        text = text.split(engToRus ? eng[x] : rus[x]).join(engToRus ? rus[x] : eng[x]);
        text = text.split(engToRus ? eng[x].toUpperCase() : rus[x].toUpperCase()).join(engToRus ? rus[x].toUpperCase() : eng[x].toUpperCase());
      }
      return text;
    }
  }
)()
Vue.filter('latCyr', function (str) {
  var result= transliterate(str,true)
  return result
})
Vue.filter('remove_ru', function (str) {
  if (str.indexOf("ru--") > -1){
    var result=Vue.options.filters.latCyr(str.replace('ru--',''))
    return result
  }
  else {//просто вернем как есть
    return str
  }
})

import moment from 'moment'
// console.log('moment locale',moment.locale())
// moment.locale(Vue.cookie.get('locale') || "ru")
moment.locale("ru")
// console.log('locale cookie',)

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).fromNow()
  }
})

Vue.filter('toRub', function(value) {
  var price = 2.37
  var sum = value * price
  return sum.toFixed(2)
})
