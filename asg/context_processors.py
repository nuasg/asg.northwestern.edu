from models import Person

def my_senator(request):
    if 'my_senator' in request.session:
        return {'my_senator': 
                Person.objects.get(id=request.session['my_senator'])}
    return {}
