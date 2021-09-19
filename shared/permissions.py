def is_logged(request):
    """
    Verifica se o usuário está autenticado.
    """

    return bool(request.user and request.user.is_authenticated)
