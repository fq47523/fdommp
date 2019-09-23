from django.shortcuts import redirect


def session_auth(func):
    def inner(request,*args,**kwargs):
        v = request.session.get('is_login',None)
        if not v:
            return redirect('/accounts/login/')
        return func(request, *args,**kwargs)
    return inner