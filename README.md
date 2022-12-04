# pose-detection AI Game

This project include a series of games that use mediapipe for human body detection.

[MediaPipe](https://google.github.io/mediapipe/) is a  cross-platform, customizable machine learning library for live and streaming media. It provides various solution API to efficiently  integrate AI into real-world applications. It’s free, open-source, and easy to use. By combining [opencv](https://github.com/opencv/opencv) library, we can apply it to detect players’ poses and joints positions during real-time games. 

To install mediapipe:

```bash
pip install mediapipe
```

### **Instructions:**

In each part of the project, there are some python files. Download these file and check the required libraries in the first few lines (most of them are common widely-use libraries, usually you only need to install the mediapipe). I recommend to build a virtual environment first before installing the libraries. To learn how to build and activate a virtual environment, click [here](https://docs.python.org/3/tutorial/venv.html).

After that, you can easily run the main python file. Depending on your computer’s processing power, the program may take a long time to show camera video, and the frame rate may also be influenced. Delays might happen if your computer is of an old version.

## Part1 - [AI painter](https://github.com/SUcy6/mediapipe-game/tree/main/painter)

You can draw on the screen with your fingers. On the top header, choose the paints’ colors or switch the tool to eraser. 

To draw on the screen, use your index finger 👆 to move around.

To choose tool/color, put your index finger and middle finger up 🤞, then move to touch the tool

To clean the canvas, put all of your 5 fingers up 🖐️

**Reminder**: Please only show one of your hands. You can choose either left or right hand. Showing both of your hands to the camera may cause some errors. 

**Video demo:**

[![https://youtu.be/nb24payxQLY](https://img.youtube.com/vi/nb24payxQLY/0.jpg)](https://www.youtube.com/watch?v=nb24payxQLY)

View on YouTube: [https://youtu.be/nb24payxQLY](https://youtu.be/nb24payxQLY)

## Part2 - [Motions to animation](https://github.com/SUcy6/mediapipe-game/tree/main/motion-animation)

Turn your motions into animation. In this part, you can input your video and get an animation text file. Put the file into the Unity project, then you can get an skeleton animation simulating your behaviors.

**Instructions:** 

First, choose a suitable video - only one person and no camera movement.

Second, set the input video path to your video path and run the program. An animation text file will be generated.

Third, download the Unity project and set it up in Unity. Drop the new animation text file into the asset folder in Unity. 

Forth, click the play ▶️ button in Unity. The animation is produced.

**Reminder:** due to the processing power limits, the video frame may delay and cause the animation not fit in the music. Choose a better computer may solve this issue.

**Video demo:**

[![https://youtu.be/iA3sBU9Q7FI](https://img.youtube.com/vi/iA3sBU9Q7FI/0.jpg)](https://www.youtube.com/watch?v=iA3sBU9Q7FI)

[https://youtu.be/iA3sBU9Q7FI](https://youtu.be/iA3sBU9Q7FI)
