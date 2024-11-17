# This Python file uses the following encoding: utf-8 
import numpy as np

def process_Meng_video_A(folder,threshold):
    #this function calculates area of thrombus and area of thrombus core at video A from paper by Meng et al.
    #folder- path to folder with frames of video A from paper by Meng et al.
    #threshold- threshold value used in analyses of thrombus on video, 50 is recommended
    area_thrombus=[]
    area_p_selectin=[]
    times=[]
    #range below corresponds to the frames of video containing thrombus image
    for i in range(32,371):
        #get frame name
        if i<100:
            name=folder+'//output_00'+str(i)+'.jpg'
        else:
            name=folder+'//output_0'+str(i)+'.jpg'
        #calculate thrombus area
        area_thr,_,_=square2(name,threshold)
        #write it into array
        area_thrombus.append(area_thr)
        #calculate p_selectin positive area
        area_psel,_,_=square_psel(name,threshold)
        #write it into array
        area_p_selectin.append(area_psel)
        #write time moment into array
        times.append((i-31)*0.702)
    return times,area_thrombus,area_p_selectin

def process_Meng_video_D(folder,threshold):
    #this function calculates area of thrombus and area of thrombus core at video D from paper by Meng et al.
    #folder- path to folder with frames of video D from paper by Meng et al.
    #threshold- threshold value used in analyses of thrombus on video, 50 is recommended
    area_thrombus=[]
    area_p_selectin=[]
    times=[]
    #range below corresponds to the frames of video containing thrombus image
    for i in range(32,380):
        #get frame name
        if i<100:
            name=folder+'//output_00'+str(i)+'.jpg'
        else:
            name=folder+'//output_0'+str(i)+'.jpg'
        #calculate thrombus area
        area_thr,_,_=square2(name,threshold)
        #write it into array
        area_thrombus.append(area_thr)
        #calculate p_selectin positive area
        area_psel,_,_=square_psel(name,threshold)
        #write it into array
        area_p_selectin.append(area_psel)
        #write time moment into array
        times.append((i-31)*0.52)
    return times,area_thrombus,area_p_selectin

def process_Stalker_video_2(folder,threshold1,threshold2):
    #this function calculates areas of thrombus and area of fibrin in thrombus at video 2 from paper by Stalker et al.
    #folder- path to folder with frames of video 2 from paper by Stalker et al.
    #threshold1- threshold value used in analyses of thrombus on video, 80 is recommended
    #threshold2- threshold value used in analyses of fibrin on video, 30 is recommended
    area_thrombus=[]
    area_fibrin=[]
    times=[]
    #range below corresponds to the frames of video containing thrombus image
    for i in range(62,314):
        #get frame name
        if i<100:
            name=folder+'//output_00'+str(i)+'.jpg'
        else:
            name=folder+'//output_0'+str(i)+'.jpg'
        #calculate thrombus area
        area_thr,_,_=square3(name,threshold1,threshold2)
        #write it into array
        area_thrombus.append(area_thr)
        #calculate fibrin positive area
        area_fib,_,_=square_fibrin(name,threshold1,threshold2)
        #write it into array
        area_fibrin.append(area_fib)
        #write time moment into array
        times.append((i-62)*0.702)
    return times,area_thrombus,area_fibrin

def sort_thrombus(arr_x,arr_y):
    #this function sorts thrombus from everything else based on fast and simple distance-based algoithm
    #set of points (which potentially belong to one thrombus)
    arr_x=np.asarray(arr_x)
    arr_y=np.asarray(arr_y)
    #center mass for this set of points
    arrx1=np.sum(arr_x)/len(arr_x)
    arry1=np.sum(arr_y)/len(arr_y)
    #position related to center of mass
    arr_x2=arr_x-arrx1
    arr_y2=arr_y-arry1
    #squared distance to center mass
    v_dist=arr_x2*arr_x2+arr_y2*arr_y2
    #distance to center mass
    v_dist2=np.sqrt(v_dist)
    #sorted distance from center mass
    d1=np.sort(v_dist2)
    thresh2=10
    #N-number of points ('area') in connected zone (i.e. in thrombus)
    N=len(v_dist2)
    #check is there is significant drop of the distance from points to the mass center. if it exists, then distant points can not belong to the thrombus
    for i in range(len(v_dist2)-1):
        if (d1[i+1]-d1[i]>thresh2):
            N=i+1
            break  
    d2=np.argsort(v_dist2)
    d3=d2[0:N]
    arr_x_new=arr_x[d3]
    arr_y_new=arr_y[d3]      
    return N,arr_x_new,arr_y_new


def square2(name,threshold):
    #function calculates area of thrombus on videos A and D from Meng et al.
    #tested by visualization
    #get pixels of the image
    from PIL import Image
    im = Image.open(name)
    a = np.asarray(im)
    a=np.asarray(a,dtype=np.float64)
    b=-np.ones((len(a),len(a[0])))
    #gather pixels which potentially correspond to thrombus shell or thrombus core
    arr_x=[]
    arr_y=[] 
    ind=-1   
    for i in range(len(a)):
        for j in range(len(a[0])):
            c1=abs(a[i][j][0]-a[i][j][1])+abs(a[i][j][0]-a[i][j][2])+abs(a[i][j][1]-a[i][j][2])
            c3=a[i][j][0]-a[i][j][2]
            if (c1>threshold) and (c3>0):
                arr_x.append(i)
                arr_y.append(j)
                ind=ind+1
                b[i][j]=ind
    #get number of pixels ('area') in thrombus and their coordinates
    N,arr_x_new,arr_y_new=sort_thrombus(arr_x,arr_y)
    return N,arr_x_new,arr_y_new

def square3(name,threshold1,threshold2):
    #function calculates area of thrombus contating fibrin (on Video 2 from Stalker et al.)
    #get pixels of the image
    from PIL import Image
    im = Image.open(name)
    a = np.asarray(im)
    a=np.asarray(a,dtype=np.float64)
    #gather pixels which potentially correspond to thrombus without fibrin of thrombus with fibrin
    arr_x=[]
    arr_y=[]    
    for i in range(len(a)):
        for j in range(len(a[0])):
            c1=abs(a[i][j][0]-a[i][j][1])+abs(a[i][j][0]-a[i][j][2])+abs(a[i][j][1]-a[i][j][2])
            c3=a[i][j][0]-a[i][j][2]
            c4=(a[i][j][0]+a[i][j][2])/2-a[i][j][1]
            if (c1>threshold1) and (c3>-abs(threshold2)) and (c4>0):
                arr_x.append(i)
                arr_y.append(j)
    #get number of pixels ('area') in thrombus and their coordinates
    N,arr_x_new,arr_y_new=sort_thrombus(arr_x,arr_y)
    return N,arr_x_new,arr_y_new


def square_psel(name,threshold):
    #function calculates P-selectin-positive area in thrombus
    #get pixels of the image
    from PIL import Image
    im = Image.open(name)
    a = np.asarray(im)
    a=np.asarray(a,dtype=np.float64)
    arr_x=[]
    arr_y=[]
    #get N- number of pixels ('area') in thrombus core (P_selectin positive)
    N=0
    for i in range(len(a)):
        for j in range(len(a[0])):
            c1=abs(a[i][j][0]-a[i][j][1])+abs(a[i][j][0]-a[i][j][2])+abs(a[i][j][1]-a[i][j][2])
            c2=abs(a[i][j][1]-a[i][j][2])/(abs(a[i][j][0]-a[i][j][1])+1)
            c3=a[i][j][1]-a[i][j][2]
            if c1>abs(threshold) and c2>2 and c3>0:
                N=N+1
                arr_x.append(i)
                arr_y.append(j)
    return N,arr_x,arr_y

def square_fibrin(name,threshold1,threshold2):
    #function calculates fbrin-positive area in thrombus
    #get pixels of the image
    from PIL import Image    
    im = Image.open(name)
    a = np.asarray(im)
    a=np.asarray(a,dtype=np.float64)
    #get N- number of pixels ('area') in zone of fibrin in thrombus
    N=0
    arr_x=[]
    arr_y=[]
    for i in range(len(a)):
        for j in range(len(a[0])):
            c1=abs(a[i][j][0]-a[i][j][1])+abs(a[i][j][0]-a[i][j][2])+abs(a[i][j][1]-a[i][j][2])
            c3=a[i][j][0]-a[i][j][2]
            c4=(a[i][j][0]+a[i][j][2])/2-a[i][j][1]
            if (c1>threshold1) and (abs(c3)<threshold2) and (c4>0):
                N=N+1
                arr_x.append(i)
                arr_y.append(j)
    return N,arr_x,arr_y

def test_visualization(folder,i0,arr_x,arr_y):
    #this function allows to visualize results of binarization
    #folder-folder with image
    #i0 -image number
    #arr_x,arr_y- positions of pixels of thrombus (calculated by sort_thrombus or other function)
    from PIL import Image, ImageDraw
    #get frame name
    if i0<100:
        name=folder+'//output_00'+str(i0)+'.jpg'
    else:
        name=folder+'//output_0'+str(i0)+'.jpg'
    image2=Image.open(name)
    draw = ImageDraw.Draw(image2)
    a = np.asarray(image2)
    a=np.asarray(a,dtype=np.float64)
    name_new=folder+'//test_image'+'.jpg'
    for i in range(len(arr_x)):
        a1=arr_x[i]
        a2=arr_y[i]
        e=round(a[a1][a2][0])
        f=round(a[a1][a2][1])
        g=round(a[a1][a2][2])
        draw.point((a2,a1),(250,250,250))
    image2.save(name_new,'jpeg')