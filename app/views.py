from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#from django.http import HttpResponse


from app.models import Produit, Commander, Pannier
# Create your views here.
def index(request):
    produits = Produit.objects.all()
    return render(request, 'app/index.html', context = {"produits": produits})

def detail(request, slug): 
    produit=get_object_or_404(Produit, slug=slug)
    return render(request, 'app/detail.html', context={"produit":produit})

def ajoutPannier(request, slug):
    user = request.user
    produit=get_object_or_404(Produit, slug=slug)
    pannier, _= Pannier.objects.get_or_create(user = user)
    commander, creer = Commander.objects.get_or_create(user = user, confirm=False, produit = produit)
    

    if creer:
        pannier.commande.add(commander)
        pannier.save()
    else:
        commander.Qte += 1
        commander.save()        
        produit.stock -=1
        produit.save()
    return redirect(reverse("produit", kwargs={"slug": slug}))
          
def pannier(request):
    pannier = get_object_or_404(Pannier, user = request.user)
    return render(request,'app/pannier.html',context = {"commandes": pannier.commande.all})  
    

def recherche(request):
    query = request.GET.get('query')
    
    if not query:
       produits = Produit.objects.all()
    else:
        produits = Produit.objects.filter(nom__contains = query)
        
        if not produits.exists():
            produits = Produit.objects.filter(produits__nom__contains = query)
            
    nom = "Résultats pour la requete %s"%query
    context = {
        'produits':produits,
        'nom': nom,
    }
    return render(request,'app/search.html', context)

def pageNext(request):
    produits_list = Produit.objects.all()
    paginator = Paginator(produits_list, 3)
    page = request.GET.get('page')
    try:
        produits = paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)
    context = {'produits':produits,
               'paginate':True}
    return render(request,'app/pageNext.html', context)

def deletePannier(request):
    pannier = request.user.pannier
    if pannier:
        pannier.commande.all().delete()
        pannier.delete()
        
    return redirect('index')