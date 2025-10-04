import os
import copy
from PIL import Image
import math
import numpy
import cv2

class N_Body:
    def __init__(self,path:str,time:int,saveFrames:bool,fps:int,mass:float,trailFactor:int,timeRatio:float) -> None:
        self.path:str = path
        self.mass:float = mass
        self.trailFactor:int = trailFactor
        self.timeRatio:float = timeRatio
        
        image,self.size = self.openImage()
        self.currentImage:list[tuple[int,int,int,int]] = image
        self.channelValue = len(self.currentImage[0])
        self.bodies:dict[int:list] = {}
        self.identifyBodies(self.currentImage)
        frames:list[list[tuple[int,int,int]]] = self.getFrames(time)
        if saveFrames:
            try:
                os.mkdir(f'{self.path}/frames')
            except:
                None
            count:int = 1
            for frame in frames:
                self.saveImage(frame,f'frames/frame{count}')
                count+=1
        self.saveVideo(frames,fps,'spaceVideo')
        
        print('Space:')
        print(' Folder path:',self.path)
        print(" Mass: ",self.mass,'x 10**9 Kg')
        print(" Trail factor: ",self.trailFactor)
        print(" FPS: ",fps)
        print(" Time ratio: ",self.timeRatio)
        print(' Save frames:',saveFrames)
        if saveFrames:
            print(' Saved frames size:',os.path.getsize(f'{self.path}/frames'),'bytes')
        print(' Video size:',os.path.getsize(f'{self.path}/spaceVideo.mp4'),'bytes')
        return
    
    def openImage(self) -> tuple[list[tuple[int,int,int]],int]:
        imageObj = Image.open(f'{self.path}/space.png')
        return (list(imageObj.convert('RGBA').getdata()),imageObj.size)
    
    def indexToCoords(self,index:int) -> tuple[int,int]:
        return (index%self.size[0],index//self.size[0])
    
    def coordsToIndex(self,coords:tuple[int,int]) -> int:
        return coords[1]*self.size[0] + coords[0]
    
    def identifyBodies(self,image:list[tuple[int,int,int]]) -> None:
        count:int = 0
        for i in range(len(image)):
            if image[i] not in [(0,0,0),(0,0,0,255)]:
                self.bodies[count] = [i,image[i],self.indexToCoords(i),(0,0),[]]
                count+=1
        return
    
    def getFNet(self,body:int) -> list[tuple[float,float],float]:
        def distance(c1:tuple[int,int],c2:tuple[int,int]) -> float:
            return math.sqrt(((c2[1]-c1[1])**2)+((c2[0]-c1[0])**2))
        
        def directionVector(c1:tuple[int,int],c2:tuple[int,int]) -> tuple[float,float]:
            return ((c2[0]-c1[0]),(c2[1]-c1[1]))
        fNetMag:float = 0
        fNetDir:list[float,float] = [0,0]
        for body2 in self.bodies:
            if body2 != body:
                try:
                    c1:tuple[int,int] = self.indexToCoords(self.bodies[body][0])
                    c2:tuple[int,int] = self.indexToCoords(self.bodies[body2][0])
                    fNetMag += ((6.674*(10**(-11)))*(math.pow(self.mass,2)))/distance(c1,c2)
                    fDir:tuple[float,float] = directionVector(c1,c2)
                    fNetDir[0] += fDir[0]
                    fNetDir[1] += fDir[1]
                except:
                    None
        dirMag:float = distance(fNetDir,(0,0))
        if dirMag == 0:
            dirMag = 1
        return [(fNetDir[0]/dirMag,fNetDir[1]/dirMag),fNetMag*dirMag]
            
    def proceedFrame(self) -> bool:
        delta:bool = False
        temp:list[tuple[int,int,int]] = [(0,0,0) if self.channelValue == 3 else (0,0,0,255) for _ in range(len(self.currentImage))]
        
        for body in self.bodies:
            fNet:list[tuple[float,float],float] = self.getFNet(body)
            acc:float = fNet[1]/self.mass
            accDir:tuple[float,float] = fNet[0]
            xOld:tuple[float,float] = self.bodies[body][2]
            vOld:tuple[float,float] = self.bodies[body][3]
            xNew:tuple[float,float] = (xOld[0] + vOld[0]*self.timeRatio + 0.5*acc*accDir[0]*(self.timeRatio**2),xOld[1] + vOld[1]*self.timeRatio + 0.5*acc*accDir[1]*(self.timeRatio**2))
            self.bodies[body][3] = (vOld[0] + acc*accDir[0]*self.timeRatio,vOld[1] + acc*accDir[1]*self.timeRatio)
            self.bodies[body][2] = xNew
            newIndex:int = self.coordsToIndex((math.floor(xNew[0]),math.floor(xNew[1])))
            self.bodies[body][4].append(newIndex)
            try:
                if newIndex >= 0:
                    temp[newIndex] = self.bodies[body][1]
            except:
                None
            if self.bodies[body][0] != newIndex:
                if not delta:
                    delta = True
            self.bodies[body][0] = newIndex
            color:tuple[int,int,int] = self.bodies[body][1]
            trailData:list[int] = self.bodies[body][4]
            if self.trailFactor > 0:
                trailData = trailData[len(trailData)-self.trailFactor:]
            for i in range(len(trailData)):
                index:int = trailData[len(trailData)-i-1]
                if newIndex >= 0:
                    if self.trailFactor == 0:
                        temp[index] = color
                    elif self.trailFactor == -1:
                        None
                    else:
                        factor:float = i/self.trailFactor
                        colorR:int = int(color[0]*(1-factor))
                        colorG:int = int(color[1]*(1-factor))
                        colorB:int = int(color[2]*(1-factor))
                        try:
                            temp[index] = (colorR if colorR >= 0 else 0,colorG if colorG >= 0 else 0,colorB if colorB >= 0 else 0)
                            if self.channelValue == 4:
                                temp[index] = tuple(list(temp[index])+[255])
                        except:
                            None
        
        self.currentImage = temp
        return delta
    
    def getFrames(self,time:int) -> list[list[tuple[int,int,int]]]:
        frames:list[list[tuple[int,int,int]]] = [copy.deepcopy(self.currentImage)]
        if time == 0:
            delta = True
            while delta:
                delta = self.proceedFrame()
                frames.append(self.currentImage)
        else:
            for _ in range(time):
                print('Now on: Frame',len(frames)+1)
                self.proceedFrame()
                frames.append(self.currentImage)
        return frames
    
    def saveImage(self,image:list[tuple[int,int,int]],subpath:str) -> None:
        imageObj = Image.new("RGB",self.size)
        imageObj.putdata(image)
        imageObj.save(f'{self.path}/{subpath}.png')
        return

    def shrink2D(self,image:list[tuple[int,int,int]]) -> list[list[list[int]]]:
        count:int = 0
        imageShrinked:list[list[list[int]]] = []
        for j in range(self.size[1]):
            imageShrinked.append([])
            for i in range(self.size[0]):
                imageShrinked[-1].append(list(image[count]))
                count+=1
        return imageShrinked
    def saveVideo(self,frames:list[list[tuple[int,int,int]]],fps:int,filename:str) -> None:
        videoWriter = cv2.VideoWriter(f'{self.path}/{filename}.mp4',cv2.VideoWriter_fourcc(*'mp4v'),fps,self.size)
        for image in frames:
            image = self.shrink2D(image)
            videoWriter.write(cv2.cvtColor(numpy.array(image,dtype=numpy.uint8),cv2.COLOR_RGB2BGR))
        videoWriter.release()
        
folderPath:str = input("Folder path: ")
saveFrames:bool = bool(input("Save frames: "))
time:int = int(input("Time: "))
fps:int = int(input("FPS: "))
mass:float = float(input("Mass (10**9): "))*(10**9)
trailFactor:int = int(input("Trail factor: "))
timeRatio:float = float(input("Time Ratio: "))
nBody:N_Body = N_Body(folderPath,time,saveFrames,fps,mass,trailFactor,timeRatio)
