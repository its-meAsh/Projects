![Banner](https://raw.githubusercontent.com/its-meAsh/python/main/Banner.png)
# Maze Generator

This Python script is a powerful tool for generating and solving mazes using a randomized Depth-First Search algorithm. It offers a wide range of customization options and can export the maze in various formats, including images, videos, binary data, and a 3D model.

---

## Features

* **Procedural Generation:** Creates unique, perfect mazes of any specified size using a randomized Depth-First Search algorithm.
* **Customizable Parameters:** Control the height, width, and visual style of the maze, including colors and pixel density.
* **Seeded Generation:** Use a specific seed to reproduce the exact same maze every time.
* **Multiple Outputs:** Generate the maze in a variety of formats:
    * Question and solution images (`.png`).
    * Question and solution videos (`.mp4`).
    * Binary data file (`.bin`).
    * Individual frames for animation (`.png`).
    * A basic 3D model file (`.obj`).
* **Visualized Solution:** The script can solve the maze and highlight the path from start to finish.

---

## How It Works

The script generates a maze by treating each tile as a cell in a grid. It uses a **randomized Depth-First Search (DFS)** algorithm to carve paths. The algorithm starts at a random cell and explores as far as possible along each branch before backtracking. This ensures that every cell is visited and that the final maze has only one solution path.

### Byte Definitions

To store information efficiently, the script uses single bytes to represent the state of each cell.
* `usedByte`: Indicates that a cell has been visited during maze generation.
* `solByte`: Marks a cell as part of the solution path.
* `blockedByte`: Marks a cell that has been visited during the solve function but is not on the solution path.

---

## Installation

Before you can run the script, you need to install the necessary Python libraries.

```bash
pip install Pillow opencv-python numpy
```

## Usage

1.  **Run the script:** Open your terminal or command prompt, navigate to the folder containing `maze.py`, and run the script.
2.  **Enter the parameters:** The script will prompt you for several inputs. Pay close attention to the instructions for each prompt.
    * **Height, Width, Seed:** These are required numerical inputs. A seed of `0` will use a random seed, allowing you to generate the same maze again by entering the same seed.
    * **Maze name, Directory name:** Optional inputs. Leaving them blank will use a default name based on the seed.
    * **Functionality flags:** For saving images, videos, frames, etc., you must type anything to confirm (`y`, `yes`, `true`, etc.) or leave it blank and press enter to skip.
    * **Image and Video Parameters:** If you choose to save images or videos, you will be prompted for additional details like `Pixels per tile`, `Border width`, `Colors`, and for videos, the `Codec` and `Extension`.

### Example

```bash
python maze.py
Height: 20
Width: 20
Seed (0 for random): 12345
For below questions, leave empty for default values
Maze name:
Directory name:
For below questions, press enter key for NO, and type anything and enter for YES
Question image save: yes
Solution image save: yes
Binary file save: yes
Question frames save:
Solution frames save:
Question video save: yes
Solution video save:
3D model: yes
For below question, enter an integer
Pixels per tile: 10
Border width: 1
Border color: 48 210 197
Background color: 0 0 0
Solution color: 255 255 255
For below question, enter an integer or float
Frames per second: 5
NOTE: Codec, extension and its compatibility with the codec is not checked by the program, do your research on your own. Video made using cv2 module
Codec: H264
Extension: mp4
```

## Connect with Me

* **GitHub:** [its-meAsh](https://github.com/its-meAsh)
* **Instagram:** [@itsmeash0405](https://www.instagram.com/itsmeash0405)
* **Gmail:** itsmeash0405@gmail.com
