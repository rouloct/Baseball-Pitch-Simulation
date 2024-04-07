# Baseball Pitch Simulation

## Demo Video
[https://drive.google.com/file/d/1g4Q1w-Hscnm_1vdxBMamzHkXE4lcrJT7/view?usp=sharing](https://drive.google.com/file/d/1p3gHEdqSiDcEyyVjxZ1xqZR7pxce1wnu/view?usp=sharing)

## Overview
This programs makes API calls to [https://statsapi.mlb.com](https://statsapi.mlb.com) to allow a user to select a specific pitch thrown in a specific game within the last 8 years. It calls a [Unity](https://unity.com) application to simulate the specific pitch-- The velocity, location, curvature, etc. of the simulated ball are the same as of the real-life pitch.

## Challenges
The first major challenge was navigating the API as little public documentation was available on the query parameters and meaning of the data. 
I explored public GitHub repos, Reddit comments, and blog posts until I had enough of an understanding of how to query and interpret the data. From there, I made calculated guesses of query parameters until I was able to get the desired data.

The second challenge was simulating the pitch itself. The API had on the position, velocity, and acceleration at 50 ft from home plate (pitcher's mound is 60.5 ft) and the position of the ball when it crossed home plate. When I simulated the pitch using constant-acceleration physics equations, the ball's ending location was wildly inaccurate. 

After reseraching on StackOverflow posts, I found the culprit: The Magnus effect. This is a phenomena in physics where the spinning baseball moving through the air results in differing pressure across the different locations of surface of the ball, which in turn creates a pressure-gradient force on the ball. The acceleration the API has does not take this into account, since the Magnus effect results in a constantly-changing acceleration.

I did not have the sufficient spin data to simulate this in Unity, so I ended up stumbling on a solution using a method I learned from Intro to Numerical Analysis, known as iterative approximation. Since I knew where the ball's true ending location, I first calculated the ball's ending location using the data provided. I took the vector difference between these two locations, then added that vector to the ball's initial acceleration. When I calculated the ball's ending location using this modified acceleration, the ball's new ending location was slightly closer to its true ending location. 

I repeatedly added the vector difference to the ball's initial acceleration and re-calcuating its ending location, around a total of 500 times, until the ball's ending location was within millimeters of its true ending location. This new calculation of acceleration results in a pretty close approximation of the ball's actual trajectory.


## Running the program
Step 1. Install the necessary python packages:
* `pip3 install tabulate`
* `pip3 install requests`

Step 2. Navigate to [main.py](main.py) and change line 6:
* If on Windows, change to `IS_WINDOWS = True` 
* If on Mac, change to `IS_WINDOWS = False` 

Step 3. Run [main.py](main.py), using an IDE or the command line:
* If on Windows, `py main.py`
* If on Mac, `python3 main.py`

Step 4. Perform the necessary terminal tasks:
* The program will prompt you in the terminal up to 7 times. 
* The simulation will open. 
* Press `Start` to see the pitch after a 3s delay. 
* Press `Restart` to see the pitch again.

Step 5. Exit the simulation:
* If on Windows, press `ALT + F4`
* If on Mac, press `COMMAND + Q` or `COMMAND + OPTION + SHIFT + ESC`

Step 6. The terminal will prompt you to rerun the program or not. If you choose yes, repeat Steps 4 and 5.

