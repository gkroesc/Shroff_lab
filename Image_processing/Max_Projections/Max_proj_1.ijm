//Use this max projection macro first, on a single position to determine whether SPIMA or SPIMB is clearer

//Add the path to the first position folder
Path = getDirectory("Select folder containing SPIMA and SPIMB");
File.makeDirectory(Path + "\\MAX_SPIMB\\");
File.makeDirectory(Path + "\\MAX_SPIMA\\");

start = 0;
end = 118;

//Add the first and last time point as the two values here
Dialog.create("Enter first and last timepoints");
Dialog.addNumber("Start", start);
Dialog.addNumber("End", end);
Dialog.show();
start = Dialog.getNumber();
end = Dialog.getNumber();

setBatchMode(true);
for(i = start; i <= end; i++)
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