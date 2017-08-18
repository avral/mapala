# storage.put_container('posts', headers={'X-Container-Read': '.r:*'})
# Page.objects.filter(position__isnull=False, position_text__isnull=False).update(has_point=True)
#from itertools import chain
#from apps.pages.models import Page

# Получить все теги
#for tag in set(t for t in chain.from_iterable([i.meta['tags'] for i in Page.objects.filter(meta__tags__isnull=False)])):
#    print(tag)

from piston.steem import Steem


s = Steem('wss://steemd.steemit.com')

p = s.get_content({'author': 'acro999', 'permlink': '1'})
print(p.export())


exit()
