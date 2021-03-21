from Movement_detection import *
import cv2
import numpy as np

'''

J'ai juste fait quelques tests, rien de concluant pour l'instant


'''


def blur_thresh(img,passe = 1,kernel_size = 3,thresh = 200):
    blur = img.copy()
    for i in range(passe):
        blur = cv2.GaussianBlur(blur,(kernel_size,kernel_size),0)
        _,blur = cv2.threshold(blur,thresh,255,cv2.THRESH_BINARY)
    return blur



def resize_and_draw_contours(img,ratio = 2):
    '''
    Prend les petites images que j'ai créé dans le dossier images
    les aggrandit et dessine les contours dessus

    '''
    width = int(img.shape[1] * ratio)
    height = int(img.shape[0] * ratio)
    img_big = cv2.resize(img,(width,height),cv2.INTER_LINEAR)
    img_gray = cv2.cvtColor(img_big, cv2.COLOR_RGB2GRAY)
    img_cont = get_contours(img_gray) #cleared function to find output
    img_output = cv2.drawContours(img_big,img_cont,-1,(0,255,0))
    img_contours = np.zeros((width,height),dtype=np.uint8)
    cv2.drawContours(img_contours,img_cont,-1,(255,255,255))
    return img_output, img_contours,img_cont

def draw_contours_points(contours,shape=(480,480)):
    '''Je dessine chaque trait séparément pour mieux comprendre le bazar'''

    new_cont = np.zeros(shape,dtype=np.uint8)
    new_shape = new_cont.copy()
    for shape in contours:
        for e,contour in enumerate(shape):
            pos1 = tuple(contour[0])
            pos2 = (200,200)

            if e < (len(shape)-1):
                pos2 = tuple(shape[e+1][0])
            else:
                pos2 = tuple(shape[0][0])

            center = (int((pos1[0]+pos2[0])/2),int((pos1[1]+pos2[1])/2))
            cv2.line(new_cont,pos1,pos2,(255,255,255),thickness=1)
            cv2.circle(new_shape,center,radius = 0,color=(255,255,255),thickness = -1) #-1 to fill
    return new_cont,new_shape


#----------------------------------------------------------------------------
'''Main code '''
if __name__ == '__main__':
    rect = cv2.imread("images\\rectangle.jpg")
    circ = cv2.imread("images\\circle.jpg")
    plant = cv2.imread("images\\plant.jpg")

    _,plant = cv2.threshold(plant,150,255,cv2.THRESH_BINARY_INV)
    plant,_,_ = resize_and_draw_contours(plant,1)

    rect_big, rect_cont, rect_contours = resize_and_draw_contours(rect,10)
    circ_big, circ_cont, _ = resize_and_draw_contours(circ,10)

    new_cont,new_shape = draw_contours_points(rect_contours)

    blur = blur_thresh(plant,1,15,150)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('n'):
            blur = blur_thresh(blur,1,15,150)

        cv2.imshow('shape_rect',plant)
        cv2.imshow('blurred',blur)

        #cv2.imshow('cont_rect',rect_cont)
        # cv2.imshow('cont_circ',circ_cont)
        # cv2.imshow('shape_circ',circ_big)
        # cv2.imshow('new',new_cont)
        # cv2.imshow('points',new_shape)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture and destroy the windows
    # cap.release() #Pour la caméra
    cv2.destroyAllWindows()
