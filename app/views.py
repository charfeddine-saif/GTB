from django.shortcuts import render
import pandas as pd

# Read the Excel file
df = pd.read_excel('data.xlsx', sheet_name='noeud 1')
puiss_1 = 15
puiss_2 = 12


# ne7sEB 9adech men  ON 
avg_1=[]
avg_2=[]
sum_1 = 0
sum_2 = 0
for index, row in df.iterrows():
    print("..",row["lampe1"])
    if(row["lampe1"]=="ON"):
        sum_1+=1
    if(row["lampe2"]=="ON"):
        sum_2+=1
    if (index +1) % 6 ==0:
        avg_1.append(sum_1 * puiss_1 /6)
        avg_2.append(sum_2 * puiss_1 /6)
        sum_1 = 0
        sum_2 = 0
        
print("avg 1 :",avg_1)
print("avg 2: ",avg_2)
# Group by hour

# Print average power consumption for each hour
# for hour, avg_power in average_power_per_hour.items():
#     print(f"Hour {hour}: Average Power Consumption = {avg_power}")


# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, 'app/home.html')


def login(request):
    return render(request, 'app/login.html')



def pilotage(request):
    return render(request, 'app/pilotage.html')


def dashboard(request):
    return render(request, 'app/dashboard.html')


def configurationgtb(request):
    return render(request, 'app/configurationgtb.html')

def visualisation(request):
    
    
    return render(request, 'app/visualisation.html')

def planification(request):
    return render(request, 'app/planification.html')