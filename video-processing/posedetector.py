import json
import math
import numpy as np
import os
from sys import platform
import sys
import cv2
import argparse
import time

def set_arms(data):
    keypoints = data[0]

    rshoulder = []
    if keypoints[2][2]==0:
        keypoints[2][0]=0
        keypoints[2][1]=0
    rshoulder.append(keypoints[2][0])
    rshoulder.append(keypoints[2][1])

    relbow = []
    relbow.append(keypoints[3][0])
    relbow.append(keypoints[3][1])

    rwrist = []
    if keypoints[4][2]==0:
        keypoints[4][0]=0
        keypoints[4][1]=0
    rwrist.append(keypoints[4][0])
    rwrist.append(keypoints[4][1])
    
    lshoulder = []
    if keypoints[5][2]==0:
        keypoints[5][0]=0
        keypoints[5][1]=0
    lshoulder.append(keypoints[5][0])
    lshoulder.append(keypoints[5][1])

    lelbow = []
    lelbow.append(keypoints[6][0])
    lelbow.append(keypoints[6][1])

    lwrist = []
    if keypoints[7][2]==0:
        keypoints[7][0]=0
        keypoints[7][1]=0
    lwrist.append(keypoints[7][0])
    lwrist.append(keypoints[7][1])
    
    return rshoulder, relbow, rwrist, lshoulder, lelbow, lwrist


def set_arms_josn(data):
    keypoints = data['people'][0]['pose_keypoints_2d']
    rshoulder = []
    rshoulder.append(keypoints[6])
    rshoulder.append(keypoints[7])

    relbow = []
    relbow.append(keypoints[9])
    relbow.append(keypoints[10])

    rwrist = []
    rwrist.append(keypoints[12])
    rwrist.append(keypoints[13])
    
    lshoulder = []
    lshoulder.append(keypoints[15])
    lshoulder.append(keypoints[16])

    lelbow = []
    lelbow.append(keypoints[18])
    lelbow.append(keypoints[19])

    lwrist = []
    lwrist.append(keypoints[21])
    lwrist.append(keypoints[22])
    
    return rshoulder, relbow, rwrist, lshoulder, lelbow, lwrist

def slope(first, second, resy):
    if(second[0]-first[0] == 0):
        return 0    
    return ((resy - second[1]) - (resy - first[1]))/(  second[0] - first[0] )

def is_offside(shoulder, elbow, wrist, resy):
    if (shoulder[0] + shoulder [1] ==0 ) or (wrist[0] + wrist [1] ==0 ):
        return False

    if(shoulder[0] == wrist[0]):
        if( wrist[1] < shoulder[1]):
            return True
        else:
            return False
    
    if(wrist[1] < shoulder[1]):
        s= slope(shoulder, wrist, resy)
        d = abs(math.degrees(math.atan(s)))
        if ( d >= 70 ):
            p1 = np.array(shoulder)
            p2 = np.array(wrist)
            p3 = np.array(elbow )
            dist=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
            if( abs(dist) <= 15):
                return True
        
    return False

def is_something(shoulder, elbow, wrist, resy):

    if (shoulder[0] + shoulder [1] ==0 ) or (wrist[0] + wrist [1] ==0 ):
        return False

    s = slope(shoulder, wrist, resy)
    d = abs(math.degrees(math.atan(s)))
    if ( d <= 45):
        p1 = np.array(shoulder)
        p2 = np.array(wrist)
        p3 = np.array(elbow )
        dist=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
        if( abs(dist) <= 15):
            return True
    return False

# "../../../examples/media/"

def get_pose_event(images_path, json_folder='' ):

    #######################################
    try:
        # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            # Windows Import
            if platform == "win32":
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append(dir_path + '/../../python/openpose/Release');
                os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
                import pyopenpose as op
            else:
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append('../../python');
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu),
                #  you can also access the OpenPose/python module from there.
                #  This will install OpenPose and the python library at your desired installation
                #  path. Ensure that this is in your python path in order to use it.
                # sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        # Flags
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_dir", default=images_path, help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
        parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
        
        #parser.add_argument("--write_keypoint", default=json_folder, help="Enable to disable the visual display.")


        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "../../../models/"

        params["display"] = 0
        params["number_people_max"] = 1
        #params["write_json"] = json_folder
        params["render_pose"] = 0
        params["model_pose"] = 'COCO'

        # Add others in path?
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1])-1: next_item = args[1][i+1]
            else: next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-','')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-','')
                if key not in params: params[key] = next_item

        # Construct it from system arguments
        # op.init_argv(args[1])
        # oppython = op.OpenposePython()

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Read frames on directory
        imagePaths = op.get_images_on_directory(args[0].image_dir);
        start = time.time()

        events = []

        q=0
        # Process and display images
        for imagePath in imagePaths:
            q+=1
            print(q)
            datum = op.Datum()
            imageToProcess = cv2.imread(imagePath)
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop([datum])

            #print("Body keypoints: \n" + str(datum.poseKeypoints))

            if datum.poseKeypoints.shape!=(1,25,3):
                continue

            he, wi = imageToProcess.shape[:2]
            resy = he

            rshoulder, relbow, rwrist, lshoulder, lelbow, lwrist = set_arms(datum.poseKeypoints)
            
            o= False
            if (is_offside(rshoulder, relbow, rwrist, resy) or is_offside(lshoulder, lelbow, lwrist, resy)  ):
                o = True

            ss=False
            if (is_something(rshoulder, relbow, rwrist, resy) or is_something(lshoulder, lelbow, lwrist, resy)):
                ss=True

            
            events.append((imagePath, o, ss))



            # if not args[0].no_display:
            #     cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
            #     key = cv2.waitKey(-1)
            #     if key == 27: break

        end = time.time()
        print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
    except Exception as e:
        print(e)
        sys.exit(-1)


    ###########################################
        #detect from json
    # for filename in os.listdir(json_folder):
    #     if filename.endswith(".json"):
    #         with open(json_folder+"/"+filename) as json_file:
    #             data = json.load(json_file)
                
    #             if len(data['people']) == 0: 
    #                 continue
                    
    #             rshoulder, relbow, rwrist, lshoulder, lelbow, lwrist = set_arms_josn(data)
                
    #             o= False
    #             if (is_offside(rshoulder, relbow, rwrist, resy) or is_offside(lshoulder, lelbow, lwrist, resy)  ):
    #                 o = True
                
    #             ss=False
    #             if (is_something(rshoulder, relbow, rwrist, resy) or is_something(lshoulder, lelbow, lwrist, resy)):
    #                 ss=True
                
    #             print (filename, o,ss)
                
            #with open(filename, 'w') as json_file:
             #   json.dump(data, json_file)

    return events