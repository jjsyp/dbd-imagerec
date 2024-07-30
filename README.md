# dbd-imagerec
Disclaimer: This program is meant to be a skill check bot for the game Dead By Daylight.  This program was designed purely for 
educational purposes and I firmly discourage the use of this tool during online play.  As such, I have not included steps here
on how to edit which monitor is captured, how to run the program or how to change any other values in the program.

Purpose: I created this tool to gain an understanding of opencv for the purposes of object detection.  Using the mss library and
some of my own code, I continually take screenshots of a section of the monitor. I limited the area captured in order to increase
the speed at which the program runs.  The below screen shot shows what a typical skill check from the game can look like:

![image](https://github.com/user-attachments/assets/042b1c2d-1e5b-420b-98b8-7756f81f9af7)

Using openCV, the progran looks for red lines and white boxes within certain size and color restraints.  The below image shows
what the previous image looks like from the program's perspective.  With the tool coloring red lines green and the white boxes 
surrounded in yellow.  

![image](https://github.com/user-attachments/assets/13a00446-6c2d-4f56-bc8f-6e454639fa4f)
Note: This coloring was implemented during testing so that I could visualize what was occuring and change the programs constrains 
based on what it was determining as red lines and white boxes.  The code for this can be found in branches besides the two release branches.
