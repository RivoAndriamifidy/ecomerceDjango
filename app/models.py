
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mysite.settings import AUTH_USER_MODEL

# Create your models here.
class Produit(models.Model):
    nom = models.CharField(max_length=100) 
    slug = models.SlugField(max_length=100)
    prix = models.FloatField(default=0.0)
    stock =models.IntegerField(default=0)
    description = models.TextField(blank = True)
    photo = models.ImageField(upload_to="image", blank=True, null = True)
    
    def __str__(self):
        return f"{self.nom} (nombre de stocks: {self.stock})"
    def get_absolute_url(self):
        return reverse("produit", kwargs={"slug": self.slug})
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Liste des produits'
        verbose_name_plural = 'Liste des produitss'

class Commander(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete = models.CASCADE)
    Qte = models.IntegerField(default=1)
    confirm = models.BooleanField(default=False)
    dateCommande = models.DateTimeField(blank = True, null=True)
    
    def __str__(self):
        return f"{self.produit.nom} ({self.Qte} (montant : {self.produit.prix * self.Qte}))"
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Commande confirmé'
        verbose_name_plural = 'Commande confirmés'
class Pannier(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    commande = models.ManyToManyField(Commander)
    
    
    def __str__(self):
        return self.user.username
    def delete(self, *arg, **kwargs):
        for commander in self.commande.all():
            commander.confirm = True
            commander.dateCommande = timezone.now()
            commander.save()
        
        self.commande.clear()       
        super().delete(*arg, **kwargs)
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Commande en attente'
        verbose_name_plural = 'Commande en attentes'
    
    
