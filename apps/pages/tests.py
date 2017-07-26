from apps.auth_api.models import User
from pprint import pprint
from collections import Counter
from apps.common.storage import Storage


# print(set(''.join(User.objects.values_list('username', flat=True))))

#storage = Storage()
#storage.put_container('posts', headers={'X-Container-Read': '.r:*'})
#print(storage.get_container('posts'))
