from django.shortcuts import render,HttpResponse
from django.conf import settings
import numpy as np
import cv2
from .models import Inferences,Query,Answer
from . import suggestions
from .forms import QueryForm
# Create your views here.

def reformat(name):
    l = name.split('_')
    for i,v in enumerate(l):
        if v in l[i+1:]:
            l.remove(v)
    return ' '.join(l).strip()

def home(request):
    model = settings.MODEL
    labels = settings.LABELS
    labels = np.array(list(map(reformat,labels)))
   
    if request.method=='POST':
        filestr = request.FILES['image'].read()
        #convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img,(128,128))
        img = img/255
        img = img.reshape(1,128,128,3)
        arr = model.predict(img.reshape(1,128,128,3))
        arr = arr.reshape(15)
        if arr.max()>=0.99:
            print(arr.max())
            disease = ''
            for i in labels[np.where(arr==arr.max())[0]][0].split('_'):
                disease = disease+' '+i
            disease = disease.strip()
            plant = disease.split(' ')[0]
            
            cure = suggestions.mapping[disease]
            disease = ' '.join(disease.split(' ')[1:])
            inference = Inferences.objects.create(image = request.FILES['image'],prediction = disease)
            inference.save()
            return render(request,'output.html',{'pred':inference,'cure':cure,'plant':plant})
        else:
            return render(request,'output.html',{'pred':{'prediction':'Unknown Leaf'},'cure':"Please Upload New Image"})
    else:
        return render(request, 'home.html')


def index(request):
    return render(request,'index.html')


def forum(request):
    queries = Query.objects.all()
    return render(request,'forum.html',{"queries":queries})

def postquery(request):
    context = dict()
    form = QueryForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
    context['form']=form

    return render(request,'postquery.html',context)