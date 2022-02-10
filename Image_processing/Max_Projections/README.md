# How to use:

Either of these files generates a max projection of an image sequence over time. It takes the image stack for each timepoint, projects the maximum intensity for
each slice onto a flat image in z.
 
Both are used by dragging and dropping the file into Fiji which opens the interacive macro editor. Once open press run and a dialog box should pop up where you can specify details of the imaging run

## Max Projection 1
Max_proj_1 should be used first, on a single position to compare images from the two different SPIMs. Run it to determine whether to use SPIMA or SPIMB for the 
other positions from that run. 

## Max Projection 2
Max_proj_2 should be used on every other position not used in Max_proj_1. Runs on either SPIMA or SPIMB, whichever is determined to be better based on the previous 
step. 


The output for btoh of these is a MAX_SPIMB/MAX_SPIMA folder that can then be dragged and dropped into Fiji to generate a virtual stack. This stack allows for quick and easy 
visualization of the embryo over the entire imaging run. It can help to figure out things like when twithcing starts, when the embryo hatches, when/if there is 
a focal shift, etc.
