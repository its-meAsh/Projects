![Banner](https://raw.githubusercontent.com/its-meAsh/python/main/Banner.png)
# N-Body Gravity Simulator

This Python script simulates the complex gravitational interactions of multiple celestial bodies (the **N-Body Problem**) using numerical methods. It takes an input image to define the initial positions and colors of the bodies and generates an animated video of their resulting orbits and paths.

---

## The N-Body System & Problem Explained

### What is the N-Body System?
An **N-Body system** is a dynamic collection of $N$ objects, such as stars or planets, that interact with each other primarily through a central force, which in this case is **gravity**. Each object's movement is continuously influenced by the gravitational pull of *every other* object in the system.

### The N-Body Problem
The **N-Body Problem** is the classical challenge of predicting the individual motions (position and velocity) of a group of celestial objects interacting under Newton's Law of Universal Gravitation.

* **Solvable Cases:** For $N=2$ (the two-body problem), there is an exact, closed-form mathematical solution.
* **The Challenge:** For $N \geq 3$ (three or more bodies), **no general analytical solution exists**. The system is chaotic and highly sensitive to initial conditions. Therefore, the problem must be solved using **numerical methods** (like the time-step integration used in this script) to approximate the positions of the bodies over small increments of time ($\Delta t$).

---

## Features

* **Unbounded Space:** The simulation space is **larger than the visualization window**. Bodies that leave the screen continue to be calculated in real space and reappear if they return to the visible boundary.
* **Vectorized Simulation:** Uses **NumPy** for efficient vector math to calculate the gravitational forces between *all* body pairs in every time step.
* **Custom Initial State:** Defines the number, initial position, and color of bodies using a simple input PNG image (`space.png`).
* **Configurable Physics:** Allows the user to set the **Mass** and **Time Ratio** to control the simulation's parameters.
* **Visual Trails:** Features a configurable **Trail Factor** to visualize the paths and orbits traced by each body.
* **Video Output:** Generates a final video (`spaceVideo.mp4`) and optionally saves individual frames for detailed analysis.

---

## Installation

The script requires the following Python libraries:

```bash
pip install Pillow opencv-python numpy
```

## Usage

1.  **Prepare your input image:** Create an image named **`space.png`** in your project folder. Any non-black pixel will be treated as a celestial body, and its color will be used for the body and its trail.
2.  **Run the script:**
    ```bash
    python n_body.py
    ```
3.  **Enter the parameters:** The script will prompt you for seven numerical or boolean inputs:

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| **Folder path** | `str` | Path to the directory containing `space.png` and where output will be saved. |
| **Save frames** | `bool` | `True` to save every frame as a PNG in a `frames/` subfolder. |
| **Time** | `int` | The number of frames/steps to run the simulation. Enter **`0` to run indefinitely** until minimal change occurs. |
| **FPS** | `int` | Frames Per Second for the output video. |
| **Mass (10**9**)** | `float` | The mass of all bodies (assumed equal), entered as a factor of $10^9$ Kg. |
| **Trail factor** | `int` | The number of past positions to draw as the body's trail. **If set to `0`, no trail is drawn**. |
| **Time Ratio** | `float` | The amount of **simulated time that passes between two frames** ($\Delta t$ in the physics calculation). |

### Example Console Input
```text
Folder path: ./space1
Save frames:
Time: 1000
FPS: 10
Mass (10**9): 0.1
Trail factor: 15
Time Ratio: 1
```
## Connect with Me

* **GitHub:** [its-meAsh](https://github.com/its-meAsh)
* **Instagram:** [@itsmeash0405](https://www.instagram.com/itsmeash0405)
* **Gmail:** itsmeash0405@gmail.com
