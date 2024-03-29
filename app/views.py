#Importation des bibliothèques et des fichiers 
# django.shortcuts est utilisé pour communiquer avec le framework Django.
# pandas est utilisé pour manipuler les données sous forme de tableaux.
#.utils fait référence à un fichier local contenant des fonctions d’aide.
from datetime import datetime
from django.shortcuts import render
import pandas as pd
from .utils import get_lampes_by_noeud_name, get_nodes_with_lampes,get_lampes_by_noeud_id
from .models import Lampe, Noeud, Planification
from django.shortcuts import redirect,get_object_or_404


file = pd.ExcelFile('data.xlsx')

# Get the names of the sheets
data=[]
sheet_names = file.sheet_names
puiss_1 = 15
puiss_2 = 12
sheet_names_arr = []
for name in sheet_names:
    df = pd.read_excel('data.xlsx', sheet_name=name)
    lampes = get_lampes_by_noeud_name(name)
    first_row_values = df.columns.tolist()[1:]
    print("lampes-----",lampes)
    # ne7sEB 9adech men  ON 

    sums= [0] * len(first_row_values)
    avgs= [0] * len(first_row_values)
    avg_arr =[]
    for i, row in df.iterrows():
        for index, val in enumerate(first_row_values):
            if(row[val]=="ON"):
                sums[index]+=1
        if (i +1) % 6 ==0:
            for x in range(len(sums)-1):
                if lampes is not None:
                    pass
                    # avgs[x]=round(sums[x]/6 * lampes[x].puissance, 2)
                    print("ooo",len(lampes),x)
                                    
            sums= [0] * len(first_row_values)
            avg_arr.append(avgs)
    data.append(avg_arr)
            


    # data.append((avg_1,avg_2))    
    

print("data: ",data)
print("data 1: ",data[0])
print("data 2: ",data[1])
print("data 3: ",data[2])


# # Group by hour

# Print average power consumption for each hour
# for hour, avg_power in average_power_per_hour.items():
#     print(f"Hour {hour}: Average Power Consumption = {avg_power}")



def home(request):
    return render(request, 'app/home.html')


def login(request):
    return render(request, 'app/login.html')



def pilotage(request):
    return render(request, 'app/pilotage.html')


def dashboard(request):
    return render(request, 'app/dashboard.html')


def configurationgtb(request):
    if request.method == 'POST':
        # Assuming the form is submitted via POST
        nom_noeud = request.POST.get('nom_noeud')
        lampes_names = request.POST.getlist('lampe')
        puissances = request.POST.getlist('puissance')
        
        if len(puissances)>0:
            noeud = Noeud.objects.create(name=nom_noeud)
            for i in range(len(lampes_names)):
                Lampe.objects.create(name=lampes_names[i], puissance=puissances[i], noeud=noeud)

        print("great", nom_noeud,lampes_names, puissances)

    
    nodes = get_nodes_with_lampes()
    return render(request, 'app/configurationgtb.html', { "nodes": nodes})

def edit_node(request):
    if request.method == 'POST':
        node_id = request.POST.get('id_noeud')
        new_lampes_names = request.POST.getlist('lampe')
        new_puissances = request.POST.getlist('puissance')
        # lampes = get_lampes_by_noeud_name(node_name)
        lampes = get_lampes_by_noeud_id(node_id)
        print("----", node_id)
        
        
        noeud = Noeud.objects.get(id=node_id)

        for i in range(len(new_lampes_names)):
            lampe = Lampe.objects.get(name=lampes[i].name, noeud=noeud)
            lampe.name = new_lampes_names[i]
            lampe.puissance = new_puissances[i]
            lampe.save()
            

        
       
        
    return redirect('configurationgtb')


def delete_node(request):
    if request.method == 'POST':
        node_id = request.POST.get('id_noeud_2')
        print("delete ", node_id)
        if node_id:
            Noeud.objects.filter(id=node_id).delete()
    return redirect('configurationgtb')



def visualisation(request):
    
    
    return render(request, 'app/visualisation.html')

def planification(request):
    
    lampes = Lampe.objects.all()
    planifications = Planification.objects.all()
    return render(request, 'app/planification.html', {'lampes': lampes, 'planifications':planifications})






def add_planification(request):
    if request.method == 'POST':
        lampe_id = request.POST.get('sel')
        lampe = Lampe.objects.get(id=lampe_id)
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')
        start_date = datetime.strptime(date1, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(date2, '%Y-%m-%dT%H:%M')
        
        planification_instance = Planification(lampe=lampe, start_date=start_date, end_date=end_date)
        planification_instance.save()
    return redirect('planification')



def edit_planification(request):
    if request.method == 'POST':
        plan_id = request.POST.get('id_plan_hidden')
        planification = get_object_or_404(Planification, id=plan_id)
        
        # Update the planification object with new data
        lampe_id = request.POST.get('sel')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        
        # Assuming lampe_id is obtained from the form
        planification.lampe_id = lampe_id
        
        # Assuming start_date and end_date are obtained from the form
        planification.start_date = start_date
        planification.end_date = end_date
        
        # Save the updated planification object
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

