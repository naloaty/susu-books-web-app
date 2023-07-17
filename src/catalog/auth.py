from catalog.models import User
from django.http import HttpResponseRedirect


class Authorization:

    def __init__(self):
        self.user = None
        self.role = None
        self.perms = []

    def check(self, perm):
        return perm in self.perms


class AuthManager:

    def __init__(self):
        self._default = None
        self._roles = {
            None: []
        }

    def register_role(self, name, permission_set, default=False):
        self._roles[name] = permission_set

        if default:
            if self._default:
                raise RuntimeError(f"Cannot set default role '{name}': "
                                   f"default role already defined - '{self._default}'")
            else:
                self._default = name

    def authorize(self, session):
        auth = Authorization()

        if 'user_id' in session:
            user = User.objects.get(pk=session['user_id'])
            auth.user = user
            auth.role = user.role
            auth.perms.extend(self._roles[user.role])
        else:
            auth.role = self._default
            auth.perms.extend(self._roles[self._default])

        return auth


ROLE_GUEST = {
    'name': 'GST',
    'permission_set': [
        'BOOKS_READ'
    ]
}

ROLE_USER = {
    'name': 'USR',
    'permission_set': [
        'PROFILE',
        'BOOKS_READ',
        'BOOKS_CREATE',
        'AUTHORS_READ',
        'AUTHORS_CREATE'
    ]
}

ROLE_CUSTOMER = {
    'name': 'CST',
    'permission_set': [
        'PROFILE',
        'BOOKS_READ',
        'BOOKS_SHOP'
    ]
}

ROLE_ADMIN = {
    'name': 'ADM',
    'permission_set': [
        'PROFILE',
        'BOOKS_READ',
        'BOOKS_CREATE',
        'BOOKS_UPDATE',
        'BOOKS_DELETE',
        'AUTHORS_READ',
        'AUTHORS_CREATE',
        'AUTHORS_UPDATE',
        'AUTHORS_DELETE'
    ]
}

auth_mgr = AuthManager()
auth_mgr.register_role(**ROLE_GUEST, default=True)
auth_mgr.register_role(**ROLE_USER)
auth_mgr.register_role(**ROLE_ADMIN)
auth_mgr.register_role(**ROLE_CUSTOMER)


class AuthMixin:
    required_perms = []
    forbidden_url = ''

    def __init__(self):
        self.auth = None

    def authorize(self):
        if not self.auth:
            self.auth = auth_mgr.authorize(self.request.session)

    def get_context_data(self, *args, **kwargs):
        self.authorize()
        get_context_data = getattr(super(), "get_context_data", None)

        if callable(get_context_data):
            context = get_context_data(*args, **kwargs)
        else:
            context = {}

        context['auth'] = self.auth
        return context

    def dispatch(self, request, *args, **kwargs):
        self.authorize()
        default_response = super().dispatch(request, *args, **kwargs)

        for perm in self.required_perms:
            if not self.auth.check(perm):
                return HttpResponseRedirect(self.forbidden_url)

        return default_response
