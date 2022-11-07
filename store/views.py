from rest_framework.decorators import api_view
from rest_framework.response import Response


# django way : 
# def product_list(request):
#     return HttpResponse('ok')

# rest way : 

@api_view()
def product_list(request):
    return Response('ok')

@api_view()
def product_detail(request, id):
    return Response(id)


