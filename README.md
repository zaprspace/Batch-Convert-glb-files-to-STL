This script uses Python and Blender to batch convert a folder of glb files to stls for 3d printing.

There are two files: 
  glb-stl gui.py
  convert_glbs_to_stls.py

  Wherever you put the first file, create a folder called "scripts" and place the second file there. 

Instructions:
 From a Command Line, run  
  python "glb-stl gui.py"
This opens the GUI. Just choose the input and output folders. The script will run a headless instance of blender and convert every glb file in the input
folder to an stl file and save it in the output folder.
  Note: Line 80 of the gui file points to the default blender install path in Windows. If you have the correct version of Blender installed (4.5.x+) and you get a "Blender not found"
  error, find your Blender installation location and replace the default location in line 80. 
