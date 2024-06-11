#Importation des bibliothèques et des fichiers 
# django.shortcuts est utilisé pour communiquer avec le framework Django.
# pandas est utilisé pour manipuler les données sous forme de tableaux.
#.utils fait référence à un fichier local contenant des fonctions d’aide.
from datetime import datetime,timedelta #nous importons les classes datetime et timedelta du module datetime. La classe datetime est utilisée pour manipuler les dates et les heures, tandis que timedelta est utilisée pour représenter la différence entre deux dates ou heures.
from django.shortcuts import render #importe la fonction render du module shortcuts de la bibliothèque Django.
import pandas as pd# importe la bibliothèque Pandas en utilisant l'alias pd
from .utils import get_lampes_by_noeud_name, get_nodes_with_lampes,get_lampes_by_noeud_id,get_data_for_node_for_specific_date# importe les fonctions d'aide du fichier utils.


from .models import Lampe, Noeud, Planification# importe les modèles Lampe, Noeud et Planification.


from django.shortcuts import redirect,get_object_or_404# importe la fonction get_object_or_404 du module shortcuts de la bibliothèque Django.

from django.http import JsonResponse# importe la classe JsonResponse du module http de la bibliothèque Django.


from django.core.exceptions import ObjectDoesNotExist# importe la classe ObjectDoesNotExist du module exceptions de la bibliothèque Django.


import json

#authantification
from django.contrib.auth import authenticate, login as django_login, logout as django_logout# importe les fonctions authenticate, login et logout du module auth de la bibliothèque Django.


from django.contrib.auth.forms import UserCreationForm# importe la classe UserCreationForm du module forms de la bibliothèque Django.



from django.contrib import messages# importe la classe messages du module contrib de la bibliothèque Django.
import minimalmodbus, time,serial
from django.views.decorators.csrf import csrf_exempt



# def get_data():
        
#     file = pd.ExcelFile('data4.xlsx')#ouvrir le fichier Excel à l'aide de la bibliothèque Pandas
#     data=[]
#     sheet_names = file.sheet_names #stocke les noms des feuilles dans le fichier Excel
#     puiss_1 = 15
    
#     sheet_names_arr = []
#     for name in sheet_names:#parcourt chaque nom de feuille dans sheet_names
#         df = pd.read_excel('data4.xlsx', sheet_name=name)#lire la feuille

#         lampes = get_lampes_by_noeud_name(name)#est appelée pour obtenir des informations sur les lampes associées à ce nœud
#         print("////",name)
        
#         first_row_values = df.columns.tolist()[1:]#stocke les valeurs de la première ligne de la feuille

#         print("first_row_values",first_row_values)
#         # ne7sEB 9adech men  ON 

#         sums= [0] * len(first_row_values)#créer une liste vide avec la longueur de la liste first_row_values

#         avgs= [0] * len(first_row_values)


#         avg_arr =[]
#         for i, row in df.iterrows():#parcourt chaque ligne dans la feuille

#             for index, val in enumerate(first_row_values):#parcourt chaque valeur dans la liste first_row_values

#                 if(row[val]=="ON"):#si la valeur est ON

#                     sums[index]+=1#incrémente la valeur de la liste sums à l'index correspondant à la valeur val


#             if (i +1) % 6 ==0:#si la ligne est divisible par 6


#                 for x in range(len(sums)):#parcourt chaque valeur dans la liste sums


#                     avgs[x]=round(sums[x]/6 * 15, 2)#incrémente la valeur de la liste avgs à l'index correspondant à la valeur val


#                 sums= [0] * len(first_row_values)#bech nerje3ha lel 0 

#                 avg_arr.append(avgs)#ajoute la liste avgs à la liste avg_arr

#                 avgs= [0] * len(first_row_values)#réinitialise la liste avgs à 0


                
#         data.append(avg_arr)#ajoute une liste (avg_arr) à une autre liste (data)
#     return data

def get_data():
    """Reads data from Excel file and calculates average power consumption."""
    plans = []
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)# est l'heure de début de la journée (00:00:00)
    end_of_day = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999)
    for p in Planification.objects.all():#parcourt tous les objets de planification.
        if p.start_date.strftime('%Y-%m-%dT%H:%M') <= end_of_day.strftime('%Y-%m-%dT%H:%M') and p.end_date.strftime('%Y-%m-%dT%H:%M') > start_date.strftime('%Y-%m-%dT%H:%M'):#nechouf lampe tekhdem lyum wela le 
            plans.append(p)
    offset = 48
    Data = {
        'noeud 1':[0] * offset,
        'noeud 2':[0] * offset,
        'noeud 3':[0] * offset,
    }
    current_date = start_date
    for i in range(offset):
        for p in plans:
            print(p.end_date.strftime('%Y-%m-%dT%H:%M'), p.start_date.strftime('%Y-%m-%dT%H:%M'))
            if p.end_date.strftime('%Y-%m-%dT%H:%M') > current_date.strftime('%Y-%m-%dT%H:%M') and p.start_date.strftime('%Y-%m-%dT%H:%M') <= current_date.strftime('%Y-%m-%dT%H:%M'):#nechouf ken tekhdem fel 30 min mte3 tawa
                Data[p.lampe.noeud.name][i] += p.lampe.puissance#nezid fy somme mte3 pui mte3 30 min taw
        current_date += timedelta(minutes=30)

    return [Data['noeud 1'], Data['noeud 2'], Data['noeud 3'], [Data['noeud 1'][x] + Data['noeud 2'][x] + Data['noeud 3'][x] for x in range(offset)]]
                


    



def home(request):
    return render(request, 'app/home.html')


def login(request):
    if request.user.is_authenticated:
    
        return redirect("pilotage")
    if request.method == 'POST':#si la méthode est POST

        username = request.POST.get('username')#bech nekhou le nom d'utilisateur dans le formulaire

        password = request.POST.get('password')#bech nekhou  le mot de passe dans le formulaire


        user = authenticate(request, username=username, password=password)#authentifie l'utilisateur avec le nom d'utilisateur et le mot de passe


        if user is not None:
            django_login(request, user)
            return redirect('pilotage')#si l'utilisateur est authentifié, on redirige vers la page pilotage

        else:
            messages.success(request, 'Invalid username or password')#sinon, on affiche un message d'erreur

            return redirect('login')
    return render(request, 'app/login.html')#si la méthode n'est pas POST, on affiche la page de connexion




def logout(request):
    django_logout(request)
    return redirect("login")#on redirige vers la page de connexion





def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            try:
                # Attempt to save the user
                form.save()
                messages.success(request, 'USER CREATED form.validate_unique()')
                return redirect('pilotage')
            except Exception as e:
                # Handle potential username already exists error
                if 'username' in str(e):
                    messages.error(request, 'Username already exists.')
                    return render(request, 'app/login.html', {'form': form})
                else:
                    # Handle other errors
                    messages.error(request, 'An error occurred while creating the user.')
                    return render(request, 'app/login.html', {'form': form})
        else:
            # Handle form validation errors
            messages.error(request, f'Please correct the errors below. {form.validate_unique()}')
            return render(request, 'app/login.html', {'form': form})

    return render(request, 'app/login.html', {'form': UserCreationForm()})







def pilotage(request):
    if not request.user.is_authenticated:

        return redirect("login")
    
    data = get_data()
    print(data)
    return render(request, 'app/pilotage.html', context={'data': data})# fel context  n3adi el data ili 7achti beha


def dashboard(request):
    return render(request, 'app/dashboard.html')#tehel el page  dashboard.html


def configurationgtb(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':# 3dit req post wela le 
        
        nom_noeud = request.POST.get('nom_noeud')# nekhou input mel nom noeud 
        lampes_names = request.POST.getlist('lampe')#nekhou input mel lampes names

        puissances = request.POST.getlist('puissance')
        
        if len(puissances)>0:

            noeud = Noeud.objects.create(name=nom_noeud)#on crée un noeud avec le nom entré dans le formulaire

            for i in range(len(lampes_names)):
                Lampe.objects.create(name=lampes_names[i], puissance=puissances[i], noeud=noeud)

        print("great", nom_noeud,lampes_names, puissances)

    
    nodes = get_nodes_with_lampes()
    return render(request, 'app/configurationgtb.html', { "nodes": nodes})

def edit_node(request):# modifier noeud 
    if request.method == 'POST':# 3adit req post wela le
        node_id = request.POST.get('id_noeud')#nechou id el noeud
        new_lampes_names = request.POST.getlist('lampe')
        new_puissances = request.POST.getlist('puissance')#nechou puissances el lampes

        
        if not node_id and not new_lampes_names and new_puissances:

            return redirect('configurationgtb')


        
        lampes = get_lampes_by_noeud_id(node_id)
        print("----", node_id)
        
        noeud = Noeud.objects.get(id=node_id)# on retrouver  le noeud avec l'id entré dans le formulaire

        print("!!!!!!!!!",new_lampes_names)
        print("!!!!!new_puissances!!!!",new_puissances)
        for new_lampe_name, new_puissance in zip(new_lampes_names, new_puissances):#zip pour lier les lampes names et puissances

            lamp_exists = Lampe.objects.filter(name=new_lampe_name, noeud=noeud).exists()#verifier si la lampe existe dans le noeud

            
            if lamp_exists:
                lampe = Lampe.objects.get(name=new_lampe_name, noeud=noeud)#si la lampe existe on la récupère

                lampe.name = new_lampe_name
                lampe.puissance = new_puissance
                lampe.save()
            else:
                lampe = Lampe.objects.create(name=new_lampe_name, puissance=new_puissance, noeud=noeud)

        
       
        
    return redirect('configurationgtb')


def delete_node(request):# delete node 
    if request.method == 'POST':
        node_id = request.POST.get('id_noeud_2')#nechou id el noeud

        print("delete ", node_id)
        if node_id:
            Noeud.objects.filter(id=node_id).delete()#supprimer le noeud avec l'id entré dans le formulaire


    return redirect('configurationgtb')




def visualisation(request):
    if not request.user.is_authenticated:
        return redirect("login")
    #bech njibo data fil forme hedhi
    # var data = [                [("noeud1",            [("annee",[12,15]), ("mois",[]),            ()]      )]    ,            [(),[]],          []           ]
    date1 = None
    date2 = None
    if request.method == 'POST':
        date1 = request.POST.get('date1')# date début
        date2 = request.POST.get('date2')# date fin


        
        
        
    all_data = []# data for all nodes

    planifications_completed = Planification.objects.filter(status='completed')# get all planifications completed

    noeuds = Noeud.objects.all().order_by('name')[:3]# get all nodes


    periods = ["year", "month", "week", "day"]
    labels = []
    for node in noeuds:
        hist_for_node = []
        for period in periods:
            hist, label = get_data_for_node_for_specific_date(node.name, period, date1, date2)#récupère des données spécifiques pour un nœud donné et une période de temps spécifiée entre deux dates.

            labels.append(label)
            hist_for_node.append([period, hist])#: la période de temps et l'historique associé à cette période. Cela permet de regrouper des données associées dans une seule liste, facilitant ainsi leur manipulation ultérieure.

        all_data.append([node.name, hist_for_node])# ajoute une nouvelle liste à une liste existante appelée all_data
    print("finallllll ",all_data)
    print("labels ",labels)
        
    

    print("Planifications  complétées:", noeuds)
    

    

    labels_json = json.dumps(labels)#utilise le module json en Python pour convertir une liste Python en une chaîne JSON
    data_json = json.dumps(all_data)

    return render(request, 'app/visualisation.html', {'data': all_data, 'labels': labels_json, 'data2': data_json})


#def planification(request):
    #lampes = Lampe.objects.all()
    #planifications = Planification.objects.all()
    #planifications_not_completed = Planification.objects.filter(status='not-completed')
    #print("planifications", planifications_not_completed) 
    #return render(request, 'app/planification.html', {'lampes': lampes, 'planifications':planifications})
def planification(request):
    lampes = Lampe.objects.all()
    planifications_not_completed = Planification.objects.filter(status='not-completed')# get all planifications not completed


    return render(request, 'app/planification.html', {'lampes': lampes, 'planifications': planifications_not_completed})# renvoie une page HTML avec les données de la base de données



def add_planification(request):
    if request.method == 'POST':
        lampe_id = request.POST.get('sel')
        lampe = Lampe.objects.get(id=lampe_id)
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')

        try:
            start_date = datetime.strptime(date1, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(date2, '%Y-%m-%dT%H:%M')

            if start_date < end_date:
                planification_instance = Planification(lampe=lampe, start_date=start_date, end_date=end_date)
                planification_instance.save()
                return redirect('planification') 
            else:
                return JsonResponse({'error': 'Start date must be before end date.'}, status=400)
        except ValueError:
            # Handle invalid date format
            return JsonResponse({'error': 'Invalid date format. Please use YYYY-MM-DDTHH:MM.'}, status=400)

    return render(request, 'planification_form.html')



# def add_planification(request):#ajoute une planification à la base de données

#     if request.method == 'POST':
#         lampe_id = request.POST.get('sel')
#         lampe = Lampe.objects.get(id=lampe_id)
#         date1 = request.POST.get('date1')#njib el valeur eli fel input eli 3edineha fel forme  
#         date2 = request.POST.get('date2')
#         start_date = datetime.strptime(date1, '%Y-%m-%dT%H:%M')#convertit la date en format datetime

#         end_date = datetime.strptime(date2, '%Y-%m-%dT%H:%M')
        
#         planification_instance = Planification(lampe=lampe, start_date=start_date, end_date=end_date)#crée une instance de la classe Planification avec les valeurs entrées dans le formulaire

#         planification_instance.save()
#     return redirect('planification')



def edit_planification(request):#modifie une planification dans la base de données

    if request.method == 'POST':
        plan_id = request.POST.get('id_plan_hidden')

        planification = get_object_or_404(Planification, id=plan_id)
        
        
        lampe_id = request.POST.get('sel')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        
       
        planification.lampe_id = lampe_id
        
    
        planification.start_date = start_date
        planification.end_date = end_date
        
        planification.save()
        
    return redirect('planification')



def delete_planification(request):


    if request.method == 'POST':
        plan_id = request.POST.get('id_plan_hidden')
        if plan_id:
            Planification.objects.filter(id=plan_id).delete()
        else:
             print("ljlskjdsk", plan_id)
    return redirect('planification')



def delete_lampe(request):
    if request.method == 'POST':
        id_lampe = request.POST.get('id_lampe')
        id_noeud = request.POST.get('id_node_tracking')
        lampes = get_lampes_by_noeud_id(id_noeud)
        print("lampes", lampes)
        print("uuiuiui",id_noeud, "---------", id_lampe)
        for i,lampe in enumerate(lampes):

            if i==int(id_lampe):
               Lampe.objects.filter(id=lampe.id).delete()


    return redirect('configurationgtb')












def status_planification(request):#pour voir le status de la planification


    if request.method == 'POST':
        current_date = timezone.now()#date du jour

        completed_planifications = Planification.objects.filter(status='completed')#planifications terminées

                 
        context = {
        'completed_planifications': completed_planifications#envoie les planifications terminées

        }
    return redirect('planification',context)





def update_visualisation(request):#pour mettre a jour la visualisation

    if request.method == 'POST':
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')
        new_all_data = []
        planifications_completed = Planification.objects.filter(status='completed')
        noeuds = Noeud.objects.all().order_by('name')[:3]#on prend les 3 premiers noeuds

        periods = ["year", "month", "week", "day"]
        labels = []
        for node in noeuds:
            hist_for_node = []
            for period in periods:
                hist, label = get_data_for_node_for_specific_date(node.name, period, date1, date2)
                labels.append(label)
                hist_for_node.append([period, hist])
            new_all_data.append([node.name, hist_for_node])
        print("!!!!!!!!!!!!! ",new_all_data)
        print("labels!!!!!!!!!!!! ",labels)
            
            
        # for x in y:
        #     x -> ism,date1,date2,puissance

        print("Planifications  complétées:", noeuds)

        new_labels_json = json.dumps(labels)
        
        print("date 1",  date1)
        print("date 2",  date2)
        
        
    return render(request, 'app/visualisation.html', {'data': new_all_data, 'labels': new_labels_json})









#print(get_lamp_power())

#def planification(request):
   # planifications_not_completed = Planification.objects.filter(status='not-completed')
    #print(planifications_not_completed, "planifications_not_completed")
    
    #return render(request, 'app/planification.html', {'planifications': planifications_not_completed})





#def visualisation(request):
   #completed_planifications = Planification.objects.filter(status='completed')
    
    
    #completed_data = []
    #for planification in completed_planifications:
       # completed_data.append({
            #'id': planification.id,
            #'lampe_name': planification.lampe.name,
            #'start_date': planification.start_date,
            #'end_date': planification.end_date,
            #'status': planification.status
       # })
    
   # return render(request, 'app/visualisation.html', {'data': completed_data})
   
def initialisation_instrument(numPort, numSalve):
    # Initialisation de l'objet Modbus instrument
    instrument = minimalmodbus.Instrument(numPort, slaveaddress=numSalve)
    # Configuration de la connexion RS-485
    instrument.serial.baudrate = 96000
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 3
    instrument.mode = minimalmodbus.MODE_RTU
    return instrument
def lecture_etat(instrument, numLampe=0):
    try:
        # Lire état du circuit
        coil_state = instrument.read_bit(numLampe)
        print(f"etat du circuit 1: {coil_state}") #si 0 circuit ouvert (lampe éteinte), si 1 circuit fermé (lampe allumée)
        return coil_state
    except Exception as e:
        print(f"Erreur: {e}")
        return -1
    finally:
        # Fermeture de la connexion série
        instrument.serial.close()
def commande(instrument, numLampe, etat=True):
    try:
        # Activation/ Désactivation du relais
        instrument.write_bit(numLampe, etat)  # si True relai ON (pas de courant)

    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        instrument.serial.close()       
def lireEtat(request):
    ###Test pour esclave 1
    instrument1 = initialisation_instrument('COM2', 1)
    #Lecture de l'état lampe 1
    etat=lecture_etat(instrument1, 0)
    time.sleep(3)
    return JsonResponse({'lampe':'lampe1','etat': etat})
@csrf_exempt  
def lireTousEtats(request):
    nbEsclaves=3
    etats={}
    for i in range(nbEsclaves):
        instrument = initialisation_instrument('COM2', i+1)
        etat1=lecture_etat(instrument, 0)
        time.sleep(3)
        etats['lampe'+str(i+1)+str(1)]=etat1
        etat2=lecture_etat(instrument, 1)
        time.sleep(3)
        etats['lampe'+str(i+1)+str(2)]=etat2
    return JsonResponse(etats)
@csrf_exempt
def allumer(request):
    print("commande", request.POST.get('commande'))
    x=request.POST.get('numLampe')
    instrument = initialisation_instrument('COM2', int(request.POST.get('numEsclave')) )
    commande(instrument, int(x), int(request.POST.get('commande')))
    time.sleep(3)
    etat=lecture_etat(instrument, int(x))
    time.sleep(3)
    return JsonResponse({'etat': etat})