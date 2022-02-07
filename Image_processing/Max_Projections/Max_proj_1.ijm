//Use this max projection macro first, on a single position to determine whether SPIMA or SPIMB is clearer

//Add the path to the first position folder
Path = "H:\\012622_DCR6485\\Pos0";
File.makeDirectory(Path + "\\MAX_SPIMB\\");
File.makeDirectory(Path + "\\MAX_SPIMA\\");

//Add the first and last time point as the two values here
for(i = 0; i <= 118; i++)
{
open(Path + "\\SPIMB\\SPIMB-"+i+".tif");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", Path + "\\MAX_SPIMB\\MAX_SPIMB-"+i+".tif");
close('*');

open(Path + "\\SPIMA\\SPIMA-"+i+".tif");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", Path + "\\MAX_SPIMA\\MAX_SPIMA-"+i+".tif");
close('*');
}