#Importation des bibliothèques et des fichiers 
# django.shortcuts est utilisé pour communiquer avec le framework Django.
# pandas est utilisé pour manipuler les données sous forme de tableaux.
#.utils fait référence à un fichier local contenant des fonctions d’aide.

from django.shortcuts import render
import pandas as pd
from .utils import get_lampes_by_noeud_name, get_nodes_with_lampes
from .models import Lampe, Noeud
from django.shortcuts import redirect


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
    # ne7sEB 9adech men  ON 

    sums= [0] * len(first_row_values)
    avgs= [0] * len(first_row_values)
    avg_arr =[]
    for i, row in df.iterrows():
        for index, val in enumerate(first_row_values):
            if(row[val]=="ON"):
                sums[index]+=1
        if (i +1) % 6 ==0:
            for x in range(len(sums)):
                if lampes is not None:
                    avgs[x]=round(sums[x]/6 * lampes[x].puissance, 2)  
                                    
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



def delete_node(request):
    if request.method == 'POST':
        node_name = request.POST.get('node_name')
        if node_name:
            Noeud.objects.filter(name=node_name).delete()
    return redirect('configurationgtb')



def visualisation(request):
    
    
    return render(request, 'app/visualisation.html')

def planification(request):
    return render(request, 'app/planification.html')