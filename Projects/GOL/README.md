![Banner](https://raw.githubusercontent.com/its-meAsh/python/main/Banner.png)
# Conway's Game of Life Simulator

This Python script is a robust implementation of **Conway's Game of Life (GOL)**. It takes a static image as the initial board state and simulates the evolution of the cellular automata, producing a video of the entire process.

---

## Features

* **Custom Initial State:** Define the starting board configuration using a simple black and white `.png` image.
* **Classic GOL Rules:** Accurately simulates the four fundamental rules of GOL.
* **Video Output:** Automatically generates a video (`.mp4`) of the simulation's evolution using **OpenCV**.
* **Frame Saving:** Option to save every frame of the simulation as a separate `.png` image for detailed analysis or external use.
* **Controlled Duration:** Run the simulation for a fixed number of steps or let it run indefinitely until the board stabilizes or the user manually stops it.

---

## How It Works

The simulation operates on a grid defined by the input image's dimensions.

### Cell States and Rules

* **Live Cell:** Represented by **White** pixels (`(255, 255, 255)`) in the input image.
* **Dead Cell:** Represented by **Black** pixels (`(0, 0, 0)`) in the input image.

The simulation proceeds by applying the standard GOL rules to every cell simultaneously in each generation (frame):

1.  **Underpopulation:** Any live cell with fewer than two live neighbors dies.
2.  **Survival:** Any live cell with two or three live neighbors lives on.
3.  **Overpopulation:** Any live cell with more than three live neighbors dies.
4.  **Reproduction:** Any dead cell with exactly three live neighbors becomes a live cell.

---

## Installation

The script requires the following Python libraries:

```bash
pip install Pillow opencv-python numpy
```

## Usage

1.  **Prepare your input image:** Create a black and white image of your starting pattern. The image **must be named `golInit.png`** and placed in the folder where you will run the script. **White pixels** are considered **live cells**, and **black pixels** are **dead cells**.
2.  **Run the script:** Open your terminal or command prompt, navigate to the folder containing `gol.py` and `golInit.png`, and run the script.
3.  **Enter the parameters:** The script will prompt you for four inputs:

    * **Folder path:** The relative path to the folder containing `golInit.png`.
    * **Save frames:** Enter `True` to save each frame as a `.png` file in a `frames` subfolder. Leave it blank or enter `False` to skip saving frames.
    * **Time:** The number of frames (generations) to run the simulation. **Enter `0` to run indefinitely** (the simulation must be manually stopped by the user in this case).
    * **FPS (Frames Per Second):** The frame rate for the output video.

### Example

```bash
python gol.py
Folder path: ./gol1
Save frames:
Time: 500
FPS: 15
```
## Connect with Me

* **GitHub:** [its-meAsh](https://github.com/its-meAsh)
* **Instagram:** [@itsmeash0405](https://www.instagram.com/itsmeash0405)
* **Gmail:** itsmeash0405@gmail.com
