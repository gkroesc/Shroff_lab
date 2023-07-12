# Tracking

Three simple scripts used for analysis and editing of annotation and tracking data from MIPAV. 

### tracking_changes.py

This script allows you to edit the name of an annotation over a series of timepoints. To use, edit the path and start and end timepoint variables in lines 5-9. Then set exisitng annotation to the name of the annotation that you want to change, and new annotation to the name you want to change it to. To run, open an Anaconda prompt, navigate to the directory containing this script and type `python tracking_changes.py`. Annotation files should automatically be updated for all timepoints specified. 'Done' will be displayed in the command prompt when it has finished running.

### clip_check.py

This is a dual function analysis script that checks for both duplicate annotations and annotations that got clipped out during the straighteneing process. To use, specify the path and start and end timepoints in lines 5-9.  To run, open an Anaconda prompt, navigate to the directory containing this script and type `python clip_check.py`. Annotation names and the timepoint(s) in which they are clipped or duplicated are displayed on the command line as the script is run.
