//Use this max projection macro second, on a single SPIM on all positions 

//Add first and last position number to the two values for v
for (v = 1; v <= 5; v++)
{
//Add the path to the image files up to Pos#, adjust SPIMA/B to whichever is better base off of Max_proj_1
Path = "H:\\012622_DCR6485\\Pos"+v+"";
File.makeDirectory(Path + "\\MAX_SPIMB_"+v+"\\");

//Add first and last time point here, adjust SPIMA/B as needed below
for (i = 0; i <= 118; i++)
{
open(Path + "\\SPIMB\\SPIMB-"+i+".tif");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", Path + "\\MAX_SPIMB_"+v+"\\MAX_SPIMB-"+i+".tif");
close('*');
}}
