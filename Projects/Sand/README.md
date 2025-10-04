![Banner](https://raw.githubusercontent.com/its-meAsh/python/main/Banner.png)
# Pixel Fall

Pixel Fall is a Python-based simulation that brings a classic falling sand game to life. It takes a static `.png` image as input and simulates the physics of falling "sand" and "water" pixels, generating a video of the final animation.

---

## Features

* **Dual-Pixel Simulation:** Simulates the physics of two distinct pixel types: sand and water.
* **Customizable Input:** Use a `sand.png` image to define the initial state of the simulation.
* **Flexible Output:** Choose to generate a video of the simulation or save individual frames as images.
* **Dynamic or Fixed Duration:** Run the simulation for a fixed number of frames or let it run until all pixels have settled.

---

## How It Works

The simulation uses three specific pixel colors in the input image to determine their behavior:

* **Sand:** The color `(239, 228, 176)` represents sand. Sand pixels fall straight down if the space below is empty. If the space is blocked, they will try to fall diagonally left or right.
* **Water:** The color `(0, 162, 232)` represents water. Water pixels behave similarly to sand, falling down and then diagonally. However, if all downward paths are blocked, they will move horizontally to the left or right to find an open space.
* **Block:** The color `(0, 0, 0)` represents a static block or wall. These pixels do not move and act as obstacles for the sand and water.

Any other colors in the image will also act as static blocks.

---

## Installation

Before you can run the simulation, you need to install the necessary Python libraries.

```bash
pip install Pillow opencv-python numpy
```
## Usage

1.  **Prepare your input image:** Place your starting image, which **must be named `sand.png`**, in the project folder. You can find a few examples in the repository.
    
2.  **Run the script:** Open your terminal or command prompt, navigate to the folder containing `sand.py` and `sand.png`, and run the script.
3.  **Enter the parameters:** The script will prompt you for four inputs:

    * **Folder path:** The relative path to the folder containing `sand.png`.
    * **Save frames:** Enter `True` to save each frame as a `.png` file in a `frames` subfolder. Leave it blank to skip saving frames.
    * **Time:** The number of frames to run the simulation. Enter `0` to run until all pixels have settled.
    * **FPS (Frames Per Second):** The frame rate for the output video.

### Example

```bash
python sand.py
Folder path: ./sand1
Save frames:
Time: 500
FPS: 30
```
---

## Connect with Me

* **GitHub:** [its-meAsh](https://github.com/its-meAsh)
* **Instagram:** [@itsmeash0405](https://www.instagram.com/itsmeash0405)
* **Gmail:** itsmeash0405@gmail.com
