# How to use:

Either of these files generates a max projection of an image sequence over time. It takes the image stack for each timepoint, projects the maximum intensity for
each slice onto a flat image in z.
 
Both are used by dragging and dropping the file into Fiji which opens the interacive macro editor

## Max Projection 1
Max_proj_1 should be used first, on a single position to compare images from the two different SPIMs. Run it to determine whether to use SPIMA or SPIMB for the 
other positions from that run. 
### To use:
  1. Adjust the filepath in line 4 up to the position that you want to generate max projections for
  2. Adjust the first and second numbers in line 9 to be the first and last timepoint that you want to create projections for
  3. Press run
  
## Max Projection 2
Max_proj_2 should be used on every other position not used in Max_proj_1. Runs on either SPIMA or SPIMB, whichever is determined to be better based on the previous 
step. 
### To use:
  1. Adjust the first and second number in line 4 to be the first and last positions that you want to generate max projections 
  for (do not include position previously run in Max_proj_1)
  2. Adjust the path in line 7 up until the directory that contains the different positions
  3. Adjust the first and second numbers in line 11 to be the first and last timepoint that you want to create projections for 
  4. Adjust SPIMB/SPIMA in lines 8, 13, and 15 as needed
  5. Press run


The output is a MAX_SPIMB/MAX_SPIMA folder that can then be dragged and dropped into Fiji to generate a virtual stack. This stack allows for quick and easy 
visualization of the embryo over the entire imaging run. Can help to figure out things like when twithcing starts, when the embryo hatches, when/if there is 
a focal shift, etc.
