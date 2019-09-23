def user_var(request):
    return {
      'username': request.session.get('username',None),
      'role':  22,
      'menu': 1,
    }