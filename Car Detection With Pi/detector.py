#!/usr/bin/env python
# https://medium.com/@ageitgey/snagging-parking-spaces-with-mask-r-cnn-and-python-955f2231c400

from picamera import PiCamera
from time import sleep

from imageai.Detection import ObjectDetection
import cv2

def compare_tup(tup1, tup2):
    box1 = []
    for i in range(tup1[0][0], tup1[1][0]):
        for j in range(tup1[0][1], tup1[1][1]):
            box1.append((i, j))

    box2 = []
    for i in range(tup2[0][0], tup2[1][0]):
        for j in range(tup2[0][1], tup2[1][1]):
            box2.append((i, j))

    box_len = 0
    if len(box1) > len(box2):
        box_len = len(box2)*0.8
    else:
        box_len = len(box1)*0.8


    count = 0
    for point1 in box1:
        for point2 in box2:
            if point1[0] == point2[0] and point1[1] == point2[1]:
                count +=1
                if count > box_len:
                    return True
                break
    
    return False

def take_photo(file_name):
    camera = PiCamera()
    camera.start_preview()
    sleep(10)
    camera.capture(file_name)
    camera.stop_preview()

# loading model
model_path = "./models/yolo-tiny.h5"
detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()

# "training" phase
take_photo("./input/before_1.png") 
input_path = "./input/before_1.png"
output_path = "./output/before_1.png"

detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

tentative_parking_spots = []

print("Training 1")
for eachItem in detection:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"], " : ", eachItem["box_points"] )
    if eachItem["name"] == "car":
        tentative_parking_spots.append(eachItem)


take_photo("./input/before_2.png")
input_path_2 = "./input/before_2.png"
output_path_2 = "./output/before_2.png"
detection_2 = detector.detectObjectsFromImage(input_image=input_path_2, output_image_path=output_path_2)

print("Training 2")
for eachItem in detection_2:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"], " : ", eachItem["box_points"] )
    # if eachItem["name"] == "car":
    #     tentative_parking_spots.append(eachItem)

parked_cars = []
print("Parked Cars")
for eachItem in detection_2:
    if eachItem["name"] == "car":
        for tentCar in tentative_parking_spots:
            if (abs(eachItem["box_points"][0] - tentCar["box_points"][0]) < 20 and abs(eachItem["box_points"][1] - tentCar["box_points"][1]) < 20):
            # if eachItem["box_points"] == tentCar["box_points"]:
                print(eachItem["box_points"])
                parked_cars.append(eachItem)


parked_cars_image = cv2.imread("./output/before_2.png")
for car in parked_cars:
    start_point = (car["box_points"][0], car["box_points"][1])
    end_point = (car["box_points"][2], car["box_points"][3]) 
    color = (255, 0, 255)
    thickness = 2
    parked_cars_image = cv2.rectangle(parked_cars_image, start_point, end_point, color, thickness)  
    cv2.putText(parked_cars_image, 'Parked Car', (start_point[0], start_point[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

cv2.imwrite("./output/before_2_parking_outlined.png", parked_cars_image)


take_photo("./input/after_1.png")
input_path_3 = "./input/after_1.png"
output_path_3 = "./output/after_1.png"
detection_3 = detector.detectObjectsFromImage(input_image=input_path_3, output_image_path=output_path_3)

open_spots = []
still_parked = []
for car in parked_cars:
    found = False
    for maybe_car in detection_3:
        if maybe_car["name"] == "car" and (abs(maybe_car["box_points"][0] - car["box_points"][0]) < 20 and abs(maybe_car["box_points"][1] - car["box_points"][1]) < 20):
            found = True
            still_parked.append(maybe_car) 

    if (not found):  
        open_spots.append(car)



parked_cars_image = cv2.imread("./output/after_1.png")
for car in still_parked:
    start_point = (car["box_points"][0], car["box_points"][1])
    end_point = (car["box_points"][2], car["box_points"][3]) 
    color = (255, 0, 255)
    thickness = 2
    parked_cars_image = cv2.rectangle(parked_cars_image, start_point, end_point, color, thickness)  
    cv2.putText(parked_cars_image, 'Parked Car', (start_point[0], start_point[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


for car in open_spots:
    start_point = (car["box_points"][0], car["box_points"][1])
    end_point = (car["box_points"][2], car["box_points"][3]) 
    color = (0, 255, 255)
    thickness = 2
    parked_cars_image = cv2.rectangle(parked_cars_image, start_point, end_point, color, thickness)  
    cv2.putText(parked_cars_image, 'Open Spot', (start_point[0], start_point[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

cv2.imwrite("./output/after_1_parking_outlined.png", parked_cars_image)





