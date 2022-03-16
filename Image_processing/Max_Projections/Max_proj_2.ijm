//Use this max projection macro second, on a single SPIM on all positions 
Path = getDirectory("Select folder containing positions");

start_pos = 1;
end_pos =5;
spim = "B";
start_tp = 0;
end_tp = 118;

Dialog.create("Image Details")
Dialog.addNumber("First Position", start_pos);
Dialog.addNumber("Last Position", end_pos);
Dialog.addString("SPIM" , spim);
Dialog.addNumber("First Timepoint" , start_tp);
Dialog.addNumber("Final Timepoint" , end_tp);
Dialog.show();

start_pos = Dialog.getNumber();
end_pos = Dialog.getNumber();
spim = Dialog.getString();
start_tp = Dialog.getNumber();
end_tp = Dialog.getNumber();



//Add first and last position number to the two values for v
setBatchMode(true);
for (v = start_pos; v <= end_pos; v++)
{
//Add the path to the image files up to Pos#, adjust SPIMA/B to whichever is better base off of Max_proj_1
current_path = Path + "\\Pos"+v+"";
File.makeDirectory(current_path + "\\MAX_SPIM" + spim + "_"+v+"\\");

//Add first and last time point here, adjust SPIMA/B as needed below
setBatchMode(true);
for (i = start_tp; i <= end_tp; i++)
{
open(current_path + "\\SPIM" + spim + "\\SPIM" + spim + "-"+i+".tif");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", current_path + "\\MAX_SPIM" + spim + "_"+v+"\\MAX_SPIM" + spim + "-"+i+".tif");
close('*');
}}
