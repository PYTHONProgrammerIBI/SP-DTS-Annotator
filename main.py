import cv2
from pdf2image import convert_from_path
import cv2
import numpy as np
import csv

points = []

def mouseCallBackFunction(event, x, y, flags, param):
    global points
    print(event)
    if event == cv2.EVENT_LBUTTONDOWN : 
        points.append((x, y))

def main() -> None : 
    imageAddress = input("Enter the image name you want to annotate: ")
    fileds = "name,page,tr,tl,br,bl".split(",")

    images = convert_from_path(f'./documents/{imageAddress}.pdf')
    print("Reading PDF")
    cvImages = [ (np.array(image))[:, :, ::-1].copy() for image in images]
    cvImages.reverse()
    
    # Choosing the page
    pageNumber = 0
    print("Here are all the pages. See which page number has a sticker and click 'Q'")
    for image in cvImages: 
        cv2.imshow(f'page {len(cvImages) - pageNumber}', image)
        pageNumber += 1
    cv2.waitKey(-1)
    cv2.destroyAllWindows()
    
    pageNumber = int(input("What page is the sticker on, enter -1 if there is no sticker : "))

    if(pageNumber == -1):
        with open("database.csv", 'w') as csvfile : 
            writer = csv.DictWriter(csvfile, fieldnames=fileds)
            
            writer.writerow({
                "name": imageAddress, 
                "page": -1, 
                "tr": -1, 
                "tl": -1, 
                "br": -1, 
                "bl": -1
            })
    else :
        importantPage: cv2.Mat = cvImages[len(cvImages) - pageNumber]
        pointsList = []
        print("Please click on the points of the sticker in the following order : \n\t 1) top right\n\t 2) top left\n\t 3) bottom right \n\t 4) bottom left")
        
        cv2.namedWindow(f'page {pageNumber}')
        cv2.setMouseCallback(f'page {pageNumber}', mouseCallBackFunction)

        while True : 
            frame = importantPage.copy()

            for point in points : 
                cv2.circle(frame, point, 8, (0, 0, 255), -1)
            
            if len(points) == 4 : 
                break

            cv2.imshow(f'page {pageNumber}', frame)
            cv2.waitKey(1)
      
        with open("database.csv", 'a') as csvfile : 
            writer = csv.DictWriter(csvfile, fieldnames=fileds)
            
            writer.writerow({
                "name": imageAddress, 
                "page": len(cvImages) - pageNumber + 1, 
                "tr": points[0], 
                "tl": points[1], 
                "br": points[2], 
                "bl": points[3]
            })
    
    print("data logged, thankyou for participating")

main()