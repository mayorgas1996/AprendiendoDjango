from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article
from django.db.models import Q
from miapp.forms import FormArticle
from django.contrib import messages

# Create your views here.

layout = """
    
"""


def index(request):

    html = """
    <ul>
    """
    year = 2020

    while year <= 2030:
        html += f"<li>{str(year)}</li>"
        year+=1
    
    html += "</ul>"

    year = 2021
    hasta = range(year,2051)
    nombre = "Javier Mayorgas"
    lenguajes = ['Python','PHP','C++']
    return render(request, 'index.html',{
        'nombre':nombre,
        'title':'Inicio',
        'mi_variable': 'Soy un dato que está en la vista',
        'lenguajes': lenguajes,
        'years':hasta
        }
    )

def hola_mundo(request):
    return render(request, 'hola_mundo.html' )

def pagina(request, redirigir = 0):

    if redirigir == 1:
        return redirect('contact', nombre = "Javi", apellido = "Mayorgas")


    return render(request, 'pagina.html',{
        'texto':'',
        'lista':['uno','dos','tres'],
    })

def contact(request, nombre="", apellido=""):
    html = ""

    if nombre and apellido:
        html += f"<h3>El nombre completo es: {nombre} {apellido}<h3>"

    return HttpResponse(layout + f"<h2>Contacto</h2>" + html)




def crear_articulo(request, title, content, public):

    articulo = Article(
        title = title,
        content = content,
        public = public
    )

    articulo.save()

    return HttpResponse(f"Articulo creado: <strong>{articulo.title}</strong> - {articulo.content}")

def save_article(request):

    if request.method == "POST":

        title = request.POST['title']
        if len(title) <= 5:
            return HttpResponse("<h2>El titulo es muy corto</h2>")

        content = request.POST['content']
        public = request.POST['public']

        articulo = Article(
            title = title,
            content = content,
            public = public
        )
        
        articulo.save()

        return HttpResponse(f"Articulo creado: <strong>{articulo.title}</strong> - {articulo.content}")

    else:
        return HttpResponse("<h2>No se ha podido crear el articulo</h2>")


def create_article(request):

    return render(request,'create_article.html')

def create_full_article(request):

    if request.method == "POST":
        formulario = FormArticle(request.POST)
        if formulario.is_valid():
            data_form = formulario.cleaned_data

            title = data_form.get('title')
            content = data_form['content']
            public = data_form['public']

            articulo = Article(
                title = title,
                content = content,
                public = public
            )
            
            articulo.save()

            #Crear mensaje flash (sesión que solo se muestra 1 vez)
            messages.success(request, f'Has creado correctamente el articulo {articulo.id}')

            return redirect('articulos')

    else:
        formulario = FormArticle()

    return render(request, 'create_full_article.html', {
        'form': formulario
    })

def articulo(request):
    try:
        articulo = Article.objects.get(title="Superman", public = True)
        response = f"Articulo: <br/> {articulo.id}. {articulo.title}"
    except:
        response = "<h1>Articulo no encontrado</h1>"
    return HttpResponse(response)


def editar_articulo(request, id):

    articulo = Article.objects.get(pk = id)
    articulo.title = "Batman"
    articulo.content = "Pelicula de 2017"
    articulo.public = True

    articulo.save()

    return HttpResponse(f"Articulo {articulo.id} editado: <strong>{articulo.title}</strong> - {articulo.content}")

def articulos(request):

    articulos = Article.objects.all()
    """
    articulos = Article.objects.filter(title__contains = "articulo")

    articulos = Article.objects.filter(
        public="True"
    ).exclude(public = False)

    articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title = 'Batman' ")

    articulos = Article.objects.filter(
        Q(title__contains = "art") | Q(public = True)
    )
    """
    return render(request, 'articulos.html', {
        'articulos': articulos
    })

def borrar_articulo(request,id):
    articulo = Article.objects.get(pk=id)

    articulo.delete()

    return redirect('articulos')

