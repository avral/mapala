export function vkShare(page) {
    let url  = 'https://vkontakte.ru/share.php?'
    let pageUrl = `${window.location.origin}/${page.author.username}/${page.permlink}`
    let body =  page.body.replace(/<\/?[^>]+(>|$)/g, '')

    url += 'url='          + encodeURIComponent(pageUrl)
    url += '&title='       + encodeURIComponent(page.title)
    // url += '&description=' + encodeURIComponent(body)
    url += '&image='       + encodeURIComponent(page.miniature)
    url += '&noparse=true'
    window.open(url,'','toolbar=0,status=0,width=626,height=436')
}

export function commentsNumeral(comments_number){
  let word = "комментариев"
  comments_number %= 100

  if(comments_number > 20)
    comments_number %= 10

  if(comments_number == 1){
    word = "комментарий"
  } else if (comments_number >= 2 && comments_number <= 4){
    word = "комментария"
  } else if (comments_number >= 5 && comments_number <= 20){
    word = "комментариев"
  }
  return word
}

/**
 * Show notification blocks with errors
 * @param  {array} errors erros array for display
 */
export function showErrors (errors, context) {
    if (typeof(errors) == 'string') {
      context.$notify(
        {
            title: 'Error :',
            message: errors,
            type: 'warning',
        })
    } else {
      var offset = 0
      for (var error in errors) {
          var err = errors[error]
          if (error == 'non_field_errors') {
            var message = err[0]
          } else {
            if (error == '0') {
              message = err
            } else {
              message = error + ': ' + errors[error]
            }
          }
          context.$notify(
            {
                title: 'Error :',
                message: message,
                type: 'warning',
                offset: offset,
            })
          offset += 100
      }
    }
}


/**
 * detect mobile device
 * @return boolean
 */
export function detectmob() {
   if(window.innerWidth <= 1000 && window.innerHeight <= 600) {
     return true;
   } else {
     return false;
   }
}

var d = /\s+/g,

    rus = "щ    ш  ч  ц  й  ё  э  ю  я  х  ж  а б в г д е з и к л м н о п р с т у ф ъ  ы ь".split(d),
    eng = "shch sh ch cz ij yo ye yu ya kh zh a b v g d e z i k l m n o p r s t u f xx y x".split(d);

export function detransliterate(str, reverse) {
    if (!reverse && str.substring(0, 4) !== 'ru--') return str
    if (!reverse) str = str.substring(4)

    // TODO rework this
    // (didnt placed this earlier because something is breaking and i am too lazy to figure it out ;( )
    if(!reverse) {
    //    str = str.replace(/j/g, 'ь')
    //    str = str.replace(/w/g, 'ъ')
        str = str.replace(/yie/g, 'ые')
    }
    else {
    //    str = str.replace(/ь/g, 'j')
    //    str = str.replace(/ъ/g, 'w')
        str = str.replace(/ые/g, 'yie')
    }

    var i,
        s = /[^[\]]+(?=])/g, orig = str.match(s),
        t = /<(.|\n)*?>/g, tags = str.match(t);

    if(reverse) {
        for(i = 0; i < rus.length; ++i) {
            str = str.split(rus[i]).join(eng[i]);
            str = str.split(rus[i].toUpperCase()).join(eng[i].toUpperCase());
        }
    }
    else {
        for(i = 0; i < rus.length; ++i) {
            str = str.split(eng[i]).join(rus[i]);
            str = str.split(eng[i].toUpperCase()).join(rus[i].toUpperCase());
        }
    }

    if(orig) {
        var restoreOrig = str.match(s);

        for (i = 0; i < restoreOrig.length; ++i)
            str = str.replace(restoreOrig[i], orig[i]);
    }

    if(tags) {
        var restoreTags = str.match(t);

        for (i = 0; i < restoreTags.length; ++i)
            str = str.replace(restoreTags[i], tags[i]);

        str = str.replace(/\[/g, '').replace(/\]/g, '');
    }

    return str;
}
