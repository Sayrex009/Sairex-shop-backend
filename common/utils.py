from rest_framework.response import Response


def api_response(data=None, message='', code=200):
    return Response({'success': code < 400, 'message': message, 'data': data}, status=code)
