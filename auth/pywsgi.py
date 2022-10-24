from gevent import monkey

monkey.patch_all()

from manage import app  # noqa
