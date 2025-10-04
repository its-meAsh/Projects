from PIL import Image
import soundfile
import os

class Sound:
    def __init__(self,path:str,window:int,duration:int) -> None:
        self.path:str = path
        self.window:int = window
        coords:list[tuple[int,int]] = self.imageExtraction()
        normalized:list[float] = self.normalize(coords)
        averaged:list[float] = self.movingAverage(normalized)
        loss:float = self.calculateLoss(normalized,averaged)
        self.saveWAV(averaged,duration)
        self.drawWave(averaged,Image.open(f'{self.path}/ogWave.png').size,coords)
        
        print('Sound:')
        print(' Folder path:',self.path)
        print(' OG Wave size:',os.path.getsize(f'{self.path}/ogWave.png'))
        print(' Loss:',loss)
        print(' Used Wave size:',os.path.getsize(f'{self.path}/usedWave.png'))
        print(' Audio size:',os.path.getsize(f'{self.path}/audio.wav'))
        return
    
    def imageExtraction(self) -> list[tuple[int,int]]:
        file = Image.open(f'{self.path}/ogWave.png')
        pixels:list = list(file.getdata())
        coordsMap:dict[float:float] = {}
        fileSize:tuple[int,int] = file.size
        for i in range(len(pixels)):
            if pixels[i] == (0,0,0):
                if i%fileSize[0] in coordsMap:
                    coordsMap[i%file.size[0]] = min(i//file.size[0],coordsMap[i%fileSize[0]])
                else:
                    coordsMap[i%file.size[0]] = i//file.size[0]
        keys:list[int] = list(coordsMap.keys())
        keys.sort()
        coords:list[tuple[int,int]] = [(i,coordsMap[i]) for i in keys]
        return coords
    
    def normalize(self,coords:list[tuple[int,int]]) -> list[float]:
        minY:int = coords[1][1]
        maxY:int = 0
        for coord in coords:
            if coord[1] > maxY:
                maxY = coord[1]
            if coord[1] < minY:
                minY = coord[1]
        normalized:list[float] = []
        mean:float = (maxY+minY)/2
        for coord in coords:
            y:int = coord[1]
            distance:float = abs(mean-y)
            if y < mean:
                normValue:float = distance/abs(mean-minY)
            if y >= mean:
                normValue:float = -distance/abs(mean-maxY)
            normalized.append(normValue)
        return normalized
    
    def movingAverage(self,values:list[float]) -> list[float]:
        split:int = int(self.window/2)
        averaged:list[float] = []
        for i in range(len(values)):
            toAverage:list[float] = []
            start:int = i-split
            end:int = i+split
            for j in range(start,end+1):
                if j>=0 and j<len(values):
                    toAverage.append(values[j])
            average:float = sum(toAverage)/len(toAverage)
            averaged.append(average)
        return averaged
    
    def calculateLoss(self,list1:list[float],list2:list[float]):
        return sum([(list1[i]-list2[i])**2 for i in range(len(list1))])/len(list1)

    def drawWave(self,values:list[float],size:tuple[int,int],coords:list[tuple[int,int]]) -> None:
        image:list[list[tuple[int,int,int]]] = [[(255,255,255) for j in range(size[0])] for i in range(size[1])]
        minY:int = coords[1][1]
        maxY:int = 0
        for coord in coords:
            if coord[1] > maxY:
                maxY = coord[1]
            if coord[1] < minY:
                minY = coord[1]
        mean:float = (maxY+minY)/2
        xToY:dict[int:int] = {coords[i][0]:int(mean)+(-abs(values[i])*abs(maxY-mean) if values[i] >= 0 else abs(values[i])*abs(minY-mean)) for i in range(len(coords))}
        for key in xToY:
            image[int(xToY[key])][key] = (0,0,0)
        flatten:list[tuple[int,int,int]] = [image[i][j] for i in range(size[1]) for j in range(size[0])]
        imageFile = Image.new("RGB",size)
        imageFile.putdata(flatten)
        imageFile.save(f'{self.path}/usedWave.png')
        return
    
    def saveWAV(self,values:list[float],duration:int) -> None:
        sampleRate:float = len(values)
        values*=duration
        soundfile.write(f'{self.path}/audio.wav',values,sampleRate)
        return

folderPath:str = input("Folder path: ")
window:int = int(input("Averaging window: "))
duration:int = int(input("Duration: "))
sound:Sound = Sound(folderPath,window,duration)