from PIL import Image
import copy
import random
import cv2
import os
import numpy

class Sand:
    def __init__(self,path:str,saveFrames:bool,time:int,fps:int) -> None:
        self.path:str = path
        image,self.size = self.readImage()
        self.currentImage:list[tuple[int,int,int]] = list(image)
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
        self.saveVideo(frames,fps,'sandVideo')

        print('Sand:')
        print(' Folder path:',self.path)
        print(" FPS: ",fps)
        print(' Save frames:',saveFrames)
        if saveFrames:
            print(' Saved frames size:',os.path.getsize(f'{self.path}/frames'),'bytes')
        print(' Video size:',os.path.getsize(f'{self.path}/sandVideo.mp4'),'bytes')
        return
    
    def readImage(self) -> tuple[list[tuple[int,int,int]],tuple[int,int]]:
        file = Image.open(f'{self.path}/sand.png')
        return (file.getdata(),file.size)
    
    def indexToCoords(self,index:int) -> tuple[int,int]:
        return (index%self.size[0],index//self.size[0])
    
    def coordsToIndex(self,coords:tuple[int,int]) -> int:
        return coords[1]*self.size[0] + coords[0]

    def getBottomAdjacent(self,index:int) -> dict[int:int]:
        coordinates:tuple[int,int] = self.indexToCoords(index)
        adjacents:dict[int,int] = {}
        if coordinates[1] + 1 < self.size[1]:
            adjacents[1] = self.coordsToIndex((coordinates[0],coordinates[1]+1))
            if coordinates[0] - 1 >= 0:
                adjacents[0] = self.coordsToIndex((coordinates[0]-1,coordinates[1]+1))
            if coordinates[0] + 1 < self.size[0]:
                adjacents[2] = self.coordsToIndex((coordinates[0]+1,coordinates[1]+1))
        if coordinates[0] - 1 >= 0:
            adjacents[3] = self.coordsToIndex((coordinates[0]-1,coordinates[1]))
        if coordinates[0] + 1 < self.size[0]:
            adjacents[4] = self.coordsToIndex((coordinates[0]+1,coordinates[1]))
        return adjacents
    
    def proceedFrame(self) -> bool:
        delta:bool = False
        for i in range(1,len(self.currentImage)+1):
            index:int = len(self.currentImage)-i
            item:tuple[int,int,int] = self.currentImage[index]
            newKey:int = None
            if item == (239,228,176):
                adjacents:dict[int,int] = self.getBottomAdjacent(index)
                if 1 in adjacents and self.currentImage[adjacents[1]] not in [(0,0,0),(239,228,176)]:
                    newKey = 1
                else:
                    keyOptions:list[int] = []
                    if 0 in adjacents and self.currentImage[adjacents[0]] not in [(0,0,0),(239,228,176)]:
                        keyOptions.append(0)
                    if 2 in adjacents and self.currentImage[adjacents[2]] not in [(0,0,0),(239,228,176)]:
                        keyOptions.append(2)
                    if len(keyOptions) > 0:
                        newKey = random.choice(keyOptions)
                if newKey != None:
                    if not delta:
                        delta = True
                    newIndex = adjacents[newKey]
                    self.currentImage[index],self.currentImage[newIndex] = self.currentImage[newIndex],(239,228,176)
            if item == (0,162,232):
                adjacents:dict[int,int] = self.getBottomAdjacent(index)
                if 1 in adjacents and self.currentImage[adjacents[1]] not in [(0,0,0),(239,228,176),(0,162,232)]:
                    newKey = 1
                else:
                    keyOptions:list[int] = []
                    if 0 in adjacents and self.currentImage[adjacents[0]] not in [(0,0,0),(239,228,176),(0,162,232)]:
                        keyOptions.append(0)
                    if 2 in adjacents and self.currentImage[adjacents[2]] not in [(0,0,0),(239,228,176),(0,162,232)]:
                        keyOptions.append(2)
                    if len(keyOptions) > 0:
                        newKey = random.choice(keyOptions)
                    else:
                        keyOptions2:list[int] = []
                        if 3 in adjacents and self.currentImage[adjacents[3]] not in [(0,0,0),(239,228,176),(0,162,232)]:
                            keyOptions2.append(3)
                        if 4 in adjacents and self.currentImage[adjacents[4]] not in [(0,0,0),(239,228,176),(0,162,232)]:
                            keyOptions2.append(4)
                        if len(keyOptions2) > 0:
                            newKey = random.choice(keyOptions2)
                if newKey != None:
                    if not delta and newKey in [0,1,2]:
                        delta = True
                    newIndex = adjacents[newKey]
                    self.currentImage[index],self.currentImage[newIndex] = self.currentImage[newIndex],(0,162,232)
        return delta
    
    def getFrames(self,till:int) -> list[list[tuple[int,int,int]]]:
        frames:list[list[tuple[int,int,int]]] = [copy.deepcopy(self.currentImage)]
        if till == 0:
            delta:bool = True
            while delta:
                delta = self.proceedFrame()
                frames.append(self.currentImage)
        else:
            for _ in range(till):
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
sand:Sand = Sand(folderPath,saveFrames,time,fps)
