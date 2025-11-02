from django.http import HttpResponse, JsonResponse

def root(request):
    # If the user is not authenticated, return JSON response
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Everything okay", "info": "You are not logged-in user"}, 
            status=401
        )

    # User is authenticated, return HTML response
    me = request.user
    admin_link = "/admin/"
    drf_docs_link = "/api/v1/docs/"

    html_content = f"""
    <h2>Hello, {me.name}!</h2>
    <p>Email: {me.email}</p>
    <p>User type: {getattr(me, 'user_type', 'N/A')}</p>
    <br>
    <a href="{admin_link}">Go to Admin Panel</a><br>
    <a href="{drf_docs_link}">API docs: /api/v1/docs/</a>
    """

    return HttpResponse(html_content)
