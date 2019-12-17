import cv2
import numpy as np
import argparse
import time
import math


def slope(first, second, resy):
    if(second[0]-first[0] == 0):
        return 100    
    return ((resy - second[1]) - (resy - first[1]))/(  second[0] - first[0] )

def is_offside(shoulder, elbow, wrist, resy):
    if (not shoulder) or (not wrist) or (not elbow):
        return False

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
            if( abs(dist) <= 10):
                return True
        
    return False

def is_something(shoulder, elbow, wrist, resy):
    if (not shoulder) or (not wrist) or (not elbow):
        return False
    if (shoulder[0] + shoulder [1] ==0 ) or (wrist[0] + wrist [1] ==0 ):
        return False

    s = slope(shoulder, wrist, resy)
    d = abs(math.degrees(math.atan(s)))
    if ( d <= 45):
        p1 = np.array(shoulder)
        p2 = np.array(wrist)
        p3 = np.array(elbow )
        dist=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
        if( abs(dist) <= 10):
            return True
    return False


class PoseDetector:
    def __init__(self):
        self.proto = "libs\pose\coco\pose_deploy_linevec.prototxt"
        self.model = "libs\pose\coco\pose_iter_440000.caffemodel"
        self.dataset = "COCO"

        # self.proto = "libs\pose\mpi\pose_deploy_linevec.prototxt"
        # self.proto="libs\pose\mpi\pose_deploy_linevec_faster_4_stages.prototxt"
        # self.model = "libs\pose\mpi\pose_iter_160000.caffemodel"
        # self.dataset = "MPI"

        # self.proto="libs\pose\body_25\pose_deploy.prototxt"
        # self.model = "libs\pose\body_25\pose_iter_584000.caffemodel"
        # self.dataset = "libs\pose\BODY25"

    def getpose(self, box):
                
        dataset= self.dataset
        scale=0.003922
        width = 368
        height = 368
        thr = 0.1

        frame= box
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        if (frameHeight < 80) or (frameWidth < 50):
            return ""

        debug= False

        if dataset == 'COCO':
            BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                        "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

            POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]
        elif dataset == 'MPI':
            BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                        "Background": 15 }

            POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                        ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                        ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]
        
        elif dataset == 'BODY25':
            BODY_PARTS= { "Nose":0 , "Neck":1 , "RShoulder":2 , "RElbow":3 , "RWrist":4 , "LShoulder":5 ,
                        "LElbow":6 ,"LWrist":7 ,"MidHip":8 ,"RHip":9 ,"RKnee":10 ,
                        "RAnkle":11 , "LHip":12 ,"LKnee":13 ,"LAnkle":14 ,"REye":15 , "LEye":16 ,"REar":17 ,
                        "LEar":18 ,"LBigToe":19 ,"LSmallToe":20 ,"LHeel":21 ,
                        "RBigToe":22 ,"RSmallToe":23 ,"RHeel":24 ,"Background":25 }

            POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]
            
        else:
            assert(dataset == 'HAND')
            BODY_PARTS = { "Wrist": 0,
                        "ThumbMetacarpal": 1, "ThumbProximal": 2, "ThumbMiddle": 3, "ThumbDistal": 4,
                        "IndexFingerMetacarpal": 5, "IndexFingerProximal": 6, "IndexFingerMiddle": 7, "IndexFingerDistal": 8,
                        "MiddleFingerMetacarpal": 9, "MiddleFingerProximal": 10, "MiddleFingerMiddle": 11, "MiddleFingerDistal": 12,
                        "RingFingerMetacarpal": 13, "RingFingerProximal": 14, "RingFingerMiddle": 15, "RingFingerDistal": 16,
                        "LittleFingerMetacarpal": 17, "LittleFingerProximal": 18, "LittleFingerMiddle": 19, "LittleFingerDistal": 20,
                        }

            POSE_PAIRS = [ ["Wrist", "ThumbMetacarpal"], ["ThumbMetacarpal", "ThumbProximal"],
                        ["ThumbProximal", "ThumbMiddle"], ["ThumbMiddle", "ThumbDistal"],
                        ["Wrist", "IndexFingerMetacarpal"], ["IndexFingerMetacarpal", "IndexFingerProximal"],
                        ["IndexFingerProximal", "IndexFingerMiddle"], ["IndexFingerMiddle", "IndexFingerDistal"],
                        ["Wrist", "MiddleFingerMetacarpal"], ["MiddleFingerMetacarpal", "MiddleFingerProximal"],
                        ["MiddleFingerProximal", "MiddleFingerMiddle"], ["MiddleFingerMiddle", "MiddleFingerDistal"],
                        ["Wrist", "RingFingerMetacarpal"], ["RingFingerMetacarpal", "RingFingerProximal"],
                        ["RingFingerProximal", "RingFingerMiddle"], ["RingFingerMiddle", "RingFingerDistal"],
                        ["Wrist", "LittleFingerMetacarpal"], ["LittleFingerMetacarpal", "LittleFingerProximal"],
                        ["LittleFingerProximal", "LittleFingerMiddle"], ["LittleFingerMiddle", "LittleFingerDistal"] ]


        inWidth = width
        inHeight = height
        inScale = scale

        net = cv2.dnn.readNet(cv2.samples.findFile(self.proto), cv2.samples.findFile(self.model))

        if frameHeight < 368:
            inWidth = frameWidth
            inHeight = frameHeight

        #tt= time.time()

        inp = cv2.dnn.blobFromImage(frame, inScale, (inWidth, inHeight),
                                    (0, 0, 0), swapRB=False, crop=False)

        net.setInput(inp)
        out = net.forward()

        #print("time : {:.3f}".format(time.time() - tt))
        assert(len(BODY_PARTS) <= out.shape[1])

        points = []
        for i in range(len(BODY_PARTS)):
            heatMap = out[0, i, :, :]

            _, conf, _, point = cv2.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]

            #points.append((int(x), int(y)) if conf > thr else None)
            points.append((x, y) if conf > thr else points.append((0,0)))

        strL = is_something(points[BODY_PARTS['LShoulder']], points[BODY_PARTS['LElbow']],
                                    points[BODY_PARTS['LWrist']], frameHeight )
        offL = is_offside(points[BODY_PARTS['LShoulder']], points[BODY_PARTS['LElbow']],
                                points[BODY_PARTS['LWrist']], frameHeight )
        strR = is_something(points[BODY_PARTS['RShoulder']], points[BODY_PARTS['RElbow']],
                                    points[BODY_PARTS['RWrist']], frameHeight )
        offR = is_offside(points[BODY_PARTS['RShoulder']], points[BODY_PARTS['RElbow']],
                                points[BODY_PARTS['RWrist']], frameHeight )

        straightArm = strR or strL
        offSide = offR or offL

        result =""
        if offSide:
            result= "offside"
        elif straightArm:
            result= "straight_arm"
        

        if debug:
            for pair in POSE_PAIRS:
                partFrom = pair[0]
                partTo = pair[1]
                assert(partFrom in BODY_PARTS)
                assert(partTo in BODY_PARTS)

                idFrom = BODY_PARTS[partFrom]
                idTo = BODY_PARTS[partTo]


                if points[idFrom] and points[idTo]:
                    pfrom= (int(points[idFrom][0]) , int(points[idFrom][1]))
                    pto =  (int(points[idTo][0]) , int(points[idTo][1]))
                    cv2.line(frame, pfrom, pto, (0, 255, 0), 3)
                    cv2.ellipse(frame, pfrom, (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                    cv2.ellipse(frame, pto, (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

            cv2.putText(frame, result, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))


            cv2.imshow('OpenPose using Opencv2', frame)
            cv2.waitKey(20000)

        #print( is_something(points[BODY_PARTS['LShoulder']], points[BODY_PARTS['LElbow']],
        #                    points[BODY_PARTS['LWrist']], frameHeight ) )
        
        return result
