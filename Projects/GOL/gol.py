import os
from PIL import Image
import copy
import cv2
import numpy

class GOL:
    def __init__(self,path:str,saveFrames:bool,time:int,fps:int) -> None:
        self.path:str = path
        image,self.size = self.openImage()
        self.currentImage = image
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
        self.saveVideo(frames,fps,'golVideo')
        
        print('Sand:')
        print(' Folder path:',self.path)
        print(" FPS: ",fps)
        print(' Save frames:',saveFrames)
        if saveFrames:
            print(' Saved frames size:',os.path.getsize(f'{self.path}/frames'),'bytes')
        print(' Video size:',os.path.getsize(f'{self.path}/golVideo.mp4'),'bytes')
        return

    def openImage(self) -> tuple[list[tuple[int,int,int]],int]:
        imageObj = Image.open(f'{self.path}/golInit.png')
        return (list(imageObj.getdata()),imageObj.size)

    def indexToCoords(self,index:int) -> tuple[int,int]:
        return (index%self.size[0],index//self.size[1])
    
    def coordsToIndex(self,coords:tuple[int,int]) -> int:
        return coords[1]*self.size[0] + coords[0]

    def getAdjacents(self,index:int) -> dict[int:int]:
        coords:tuple[int,int] = self.indexToCoords(index)
        adjacents:dict[int,int] = {}
        if coords[1]-1 >= 0:
            adjacents[1] = self.coordsToIndex((coords[0],coords[1]-1))
            if coords[0]-1>=0:
                adjacents[0] = self.coordsToIndex((coords[0]-1,coords[1]-1))
            if coords[0]+1<self.size[0]:
                adjacents[2] = self.coordsToIndex((coords[0]+1,coords[1]-1))
        if coords[1]+1 < self.size[1]:
            adjacents[6] = self.coordsToIndex((coords[0],coords[1]+1))
            if coords[0]-1>=0:
                adjacents[5] = self.coordsToIndex((coords[0]-1,coords[1]+1))
            if coords[0]+1<self.size[0]:
                adjacents[7] = self.coordsToIndex((coords[0]+1,coords[1]+1))
        if coords[0]-1>=0:
            adjacents[3] = self.coordsToIndex((coords[0]-1,coords[1]))
        if coords[0]+1<self.size[0]:
            adjacents[4] = self.coordsToIndex((coords[0]+1,coords[1]))
        return adjacents

    def proceedFrame(self) -> bool:
        delta:bool = False
        temp:list[tuple[int,int,int]] = []
        for i in range(len(self.currentImage)):
            if self.currentImage[i] == (0,0,0):
                adjacents:dict[int,int] = self.getAdjacents(i)
                neighbours:int = 0
                for dirn in adjacents:
                    neighbours+= 1 if self.currentImage[adjacents[dirn]] == (255,255,255) else 0
                if neighbours == 3:
                    temp.append((255,255,255))
                    if not delta:
                        delta = True
                else:
                    temp.append((0,0,0))
                continue
            toPut:tuple[int,int,int] = None
            adjacents:dict[int,int] = self.getAdjacents(i)
            neighbours:int = 0
            for dirn in adjacents:
                neighbours+= 1 if self.currentImage[adjacents[dirn]] == (255,255,255) else 0
            if neighbours < 2:
                toPut = (0,0,0)
                if not delta:
                    delta = True
            elif neighbours in [2,3]:
                toPut = (255,255,255)
            elif neighbours > 3:
                toPut = (0,0,0)
                if not delta:
                    delta = True
            temp.append(toPut)
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
sand:GOL = GOL(folderPath,saveFrames,time,fps)
