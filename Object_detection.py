from PIL import Image,ImageOps,ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import cv2


def Background_remove(array, threshold = 80):
    #Usunięcie tła z grincha
    return np.where(array<threshold, array, 255)

def Mask_array(image, red_img, grinch):
    
    ''' 
    Funkcja szukająca grincha na podanym obrazku
    Niestety nie działa poprawnie
    '''
    grinch1 = grinch.resize((24,32), Image.ANTIALIAS) #branie różnych orzmiarów grincha
    grinch2 = grinch.resize((12,16), Image.ANTIALIAS)
    grinch3 = grinch.resize((24,48), Image.ANTIALIAS)
    grinch4 = grinch.resize((6,8), Image.ANTIALIAS)
    grinch5 = grinch.resize((20,28), Image.ANTIALIAS)
    red_img = red_img.resize((480,640), Image.ANTIALIAS)
    image = image.resize((480,640), Image.ANTIALIAS)

    grinch_hist1 = np.array(grinch1.histogram()) #tworzenie histogramu
    grinch_hist2 = np.array(grinch2.histogram())
    grinch_hist3 = np.array(grinch3.histogram())
    grinch_hist4 = np.array(grinch4.histogram())
    grinch_hist5 = np.array(grinch5.histogram())

    i = 0
    j = 0

    # temp = image.crop((i,j,i+24,j+48))
    # temp_hist = np.array(temp.histogram())
    # #print(temp_hist)
    # #print(grinch_hist)
    # Image._show(temp)
    sum1 = np.array([0])
    sum2 = np.array([0])
    sum3 = np.array([0])
    sum4 = np.array([0])
    sum5 = np.array([0])
    
    #Pętlę przechodzące co 4 piksele w każdą stronę,
    #wycinające pojedyncze wycinki obrazka i porównujące je z grinchami
    while i + grinch3.size[0] < red_img.size[0]:
        while j + grinch3.size[1] < red_img.size[1]:
            temp1 = red_img.crop((i,j,i+grinch1.size[0],j+grinch1.size[1]))
            temp2 = red_img.crop((i,j,i+grinch2.size[0],j+grinch2.size[1]))
            temp3 = red_img.crop((i,j,i+grinch3.size[0],j+grinch3.size[1]))
            temp4 = red_img.crop((i,j,i+grinch4.size[0],j+grinch4.size[1]))
            temp5 = red_img.crop((i,j,i+grinch5.size[0],j+grinch5.size[1]))
            temp_hist = np.array(temp1.histogram())
            sum1 = np.append(sum1,np.sum(np.square(grinch_hist1-temp_hist)))
            # if np.sum(np.square(grinch_hist1-temp_hist))<1950:
            #     draw = ImageDraw.Draw(image)
            #     draw.rectangle(((i,j),(i+grinch1.size[0],j+grinch1.size[1])),width=3,outline='red')
            temp_hist = np.array(temp2.histogram())
            sum2 = np.append(sum2,np.sum(np.square(grinch_hist2-temp_hist)))
            # if np.sum(np.square(grinch_hist2-temp_hist))<370:
            #     draw = ImageDraw.Draw(image)
            #     draw.rectangle(((i,j),(i+grinch2.size[0],j+grinch2.size[1])),width=3,outline='red')
                
            temp_hist = np.array(temp3.histogram())
            sum3 = np.append(sum3,np.sum(np.square(grinch_hist3-temp_hist)))
            if np.sum(np.square(grinch_hist3-temp_hist))<2360:
                draw = ImageDraw.Draw(image)
                draw.rectangle(((i,j),(i+grinch3.size[0],j+grinch3.size[1])),width=3,outline='red')
            
            temp_hist = np.array(temp4.histogram())
            sum4 = np.append(sum4,np.sum(np.square(grinch_hist4-temp_hist)))
            # if np.sum(np.square(grinch_hist4-temp_hist))<109 and np.sum(np.square(grinch_hist4-temp_hist))>107:
            #     draw = ImageDraw.Draw(image)
            #     draw.rectangle(((i,j),(i+grinch4.size[0],j+grinch4.size[1])),width=2,outline='red')
            temp_hist = np.array(temp5.histogram())
            sum5 = np.append(sum5,np.sum(np.square(grinch_hist5-temp_hist)))
            # if np.sum(np.square(grinch_hist5-temp_hist))<1490:
            #     draw = ImageDraw.Draw(image)
            #     draw.rectangle(((i,j),(i+grinch5.size[0],j+grinch5.size[1])),width=3,outline='red')
            j+=4
        j = 0    
        i+=4
    sum1 = np.delete(sum1,0)
    sum2 = np.delete(sum2,0)    
    sum3=np.delete(sum3,0)    
    sum4=np.delete(sum4,0)    
    sum5=np.delete(sum5,0)         
    return image

def Draw_and_crop(image):

    #Otaczanie obiektu bounding boxem i nastepne jego wycinanie
    draw = ImageDraw.Draw(image)
    draw.rectangle(((830,300),(910,440)),width=3,outline='red')
    crop = image.crop((833,303,908,438))
    return image,crop


if __name__ == "__main__":
    
    #Otwarcie potrzebnych plików
    img_org = Image.open("0700/org.jpg")
    img_edit = Image.open("0700/edited.jpg")
    gray_edit = ImageOps.grayscale(img_edit)
    
    #Proste usuwanie tła i zostawianie samych grinchy z czarno białych obrazków
    #Zwykłe odjęcie jednego obrazka od drugiego
    #Zakomentowane by uniknąć "rzygania" na ekran
    # buffer1 = np.asarray_chkfinite(img_edit)
    # buffer2 = np.asarray_chkfinite(img_org)
    # buffer3 = buffer1 - buffer2
    # buffer3 = np.where(buffer3<15,255,buffer3)
    # diff = Image.fromarray(buffer3)
    # Image._show(diff)

    #Ręczne wycinanie grincha i późniejsze usuwanie tła
    img,crop = Draw_and_crop(img_edit)
    Image._show(img)
    crop_arr = np.asarray_chkfinite(crop)
    crop_arr = Background_remove(crop_arr,90)
    crop1 = Image.fromarray(crop_arr)
    Image._show(crop1)

    #Przygotowanie tabel różnych kolorów obrazka(RGB)
    r,g,b = crop.split()
    re,ge,be = img_edit.split()
    masked = Mask_array(img_edit,re,r) #Funkcja wyszukująca grincha na obrazku
    Image._show(masked)