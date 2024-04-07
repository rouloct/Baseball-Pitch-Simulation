# Baseball Pitch Simulation

## Overview
This program begins in Python and uses API calls to [https://statsapi.mlb.com](https://statsapi.mlb.com) to allow a user to select a specific pitch thrown in a specific game within the last 8 years. It then calls an application that was built using [Unity](https://unity.com) to simulate the specific baseball pitch.


## Cloning the repository
The directory [/Pitch](/Pitch) contains the Unity files for opening the program in Unity with Editor Version 2022.3.21f1. However, this is not necessary to run the program and may take a lot of time to fetch. 

To clone WITH this directory, clone the main branch as normal: 

`git clone https://github.com/uvmcs2300s2024/M3OEP-rulmer.git`

To clone WITHOUT this directory, clone the branch 'nounity':
`git clone -b nounity https://github.com/uvmcs2300s2024/M3OEP-rulmer.git`


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

Step 6. The terminal will prompt you to rerun the program or not. If you choose yes, repeat Steps 4 and 5. Otherwise, you are done.

## Code
### Language 1: Python

#### Files and Code
The file [main.py](main.py) is the program's entry point. It displays game information and prompts the user.  

The file [api_methods.py](api_methods.py) is responsible for providing the methods which makes GET requests to the API.

The file [api_classes.py](api_classes.py) provides classes that are used to store the information from the GET requests. 

The file [helper_methods.py](helper_methods.py) provides helper methods for displaying class data and converting strings to dates.

Once the user has selected a pitch, [main.py](main.py) calls the simulation, which is a `.exe` (Windows) or `.app` (Mac) file that was built using Unity. This is called using the command line and passes arguments relating to the pitch data, such as position, veloicty, and acceleration.


#### Language Justification
Python was chosen for two reasons: 
* The 'requests' package provides a very simple way to requests using HTTP GET. Unlike other languages, you do not have to wrap this in a try-catch block.  
* The 'tabulate' package provides an easy way to print formatted tables of data. This was especially important for printing pitch data. In another language, formatting would been incredibly tedious to do. 

JavaScript was considered due to the optional chaining operator to find nested JSON properties without performing a null check at each step: `object.property?.property?.property?...` 

C++ was not used since GET requests and string formatting are much more difficult than in Python. Since API requests do not require a fast language, developer time is the most important factor in consdiering a language.


### Language 2: C# + (Unity)

#### Files and Code
The game engine [Unity](https://unity.com) is used to simulate the baseball. A demonstration is included in the submitted video so you can see what this looks like. 

There are four scripts (C# code) that are used in the simulation and are found at [/Pitch/Assets/Scripts](/Pitch/Assets/Scripts).

The file [GameManager.cs](/Pitch/Assets/Scripts/GameManager.cs) manages the rest of the components. When the simulation is run, it fetches the command line arguments and passes them to [PitchData.cs](/Pitch/Assets/Scripts/PitchData.cs), which converts them to appropriate values or uses defualt ones if the conversion is invalid and stores them.

When the user presses `Start`, GameManager passes information to [Ball.cs](/Pitch/Assets/Scripts/Ball.cs). Since PitchData only contains the position, veclocity, acceleration at 50 ft from the plate, GameManager determines the vectors from the ball's release point the ball was actually thrown before passing it to Ball. 

GameManager's Update() method is a Unity event method that is called every frame. This is responsible for setting components, such as the ball, timer, duplicate ball, etc, to active or inactive based on the time. Once the ball has crossed the strike zone, GameManager sets a duplicate ball to active, which is a non-moving ball that shows the user where the pitch ended.

The file [Ball.cs](/Pitch/Assets/Scripts/Ball.cs) is attached to the  ball game object. The Ball is passed information from GameManager on its starting position, velocity, acceleration, and ending position. 

However, the acceleration provided by the API does not take into account the Magnus effect, which is how an object's angular velocity (spin) influence its movement. This effect is significant for the baseball.

Since the actual ending position is known, the script uses an iterative method to calculate the actual acceleration to simulate the proper ball path. This is done by taking the difference between the calculated ending position and actual ending position then adding that difference vector to the acceleration. The difference is then calculated again, using the new acceleration, until our approximation is within an acceptable range of the actual ending position, around 0.0001 meters.

The Ball's Update() method updates the position of the ball every frame based on the initial position, veloicty, and calculated acceleration.

I generated executables using Unity's built in Build option so the user can run the simulation without needing to have Unity installed. These are found at [/WindowsBuild/Pitch.exe](/WindowsBuild/) and [/MacBuild/Pitch.app/Contents/MacOS/Pitch](/MacBuild/Pitch.app/Contents/MacOS/).

#### Language Justification
Unity was chosen because it is able to integrate graphics and code easily and provides the tools for simulating a real-life event. I do not have experience with any other tools capable of showing a baseball pitch, so Unity was the natural choice and one I am happy with. Unity only supports C#, so naturally it was the language I used. Unity's `Vector3` C# class, allows for easy math calculations and made the actual coding less complicated.

## Challenges
One challenge I ran into was with the API. There is little documentation available and it was difficult to figure out what requests to make and what the data meant. 

I used the public respository found at https://github.com/toddrob99/MLB-StatsAPI to determine the API paths and parameters, but even with this, it was quite challenging to do.

I used Baseball Savant's CSV documentation at https://baseballsavant.mlb.com/csv-docs to help understand the data, although this documentation does not perfectly match the data I was getting, so some guess work and trial-and-error needed to be done.

The other challenge I ran into was simulating the pitch itself. I was not aware of the Magnus effect at first, so the Ball was not traveling in the desired path and I could not figure out why. Once I learned about the Magnus effect, I spent some time trying to actually calculate it, which was a mistake. Once I stumbled upon the solution of approximating, writing the code was easy.

The main challenges for this project were not in writing code itself, but instead figuring out what I actually needed to write. 

## Known Bugs
Not as many games are shown as expected. Baseball teams play 162 games in the regular season but it only finds 40-50 per team. I do not know if this is due to a lack of information in the API or imperfect GET requests. 

## Future Work
With more time, I would try to add a model of the pitcher to provide a more realistic scene. I would also make it so instead of searching for a specific game the user could search for a specific pitcher. That said, the program is functional and I'm incredibly happy with the end result.

## Grade Deserved
#### Main - 40 pts
The main function has a significant amount of user interaction, all of which is validate and done smoothly. If the user hits `Enter` or enters incorrect information, it simply defualts to an appropriate value, making it very easy to get to the actual simulation if you don't care about specific game data.

#### Use of multiple languages - 20 pts
The two languages used both contained an impressive amount of work. Python contains ~700 lines of code and C# has ~400 lines of code plus all the work done in the Unity editor.

#### Choice of languages - 20 pts
The program uses GET requests and table formatting which is a strength of Python and Unity is a good choice for simulating action and movement.

#### Command line arugments - 20 pts
Python's [main.py](main.py) executes the Unity scene through the command line and passes 15 arguments relating to the pitch, such as position, veloicty, accleration, and strike zone size. These arguments are read by [GameManager.cs](/Pitch/Assets/Scripts/GameManager.cs) by  `Environment.GetCommandLineArgs()` and parsed by [PitchData.cs](/Pitch/Assets/Scripts/PitchData.cs).


#### Bonus - a lot (I hope)
I used Python's 'requests' library in Python to make API calls to http://statsapi.mlb.com.

I used the game engine Unity to simulate the baseball.


#### Ending Comments
I spent a lot of time on this project and hope you are impressed! There were many times during development where I wasn't sure if I was going to make it work, but I figured it all out and am very proud of the end result. 
