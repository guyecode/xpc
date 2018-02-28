# export PYTHONSTARTUP=<this file path>
from django.conf import settings
from django.core.paginator import Paginator
from web.models.post import Post
from web.models.composer import Composer
from web.models.comment import Comment
from web.models.copyright import Copyright
