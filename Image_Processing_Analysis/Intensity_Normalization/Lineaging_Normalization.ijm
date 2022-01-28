//This Macro is run on both RegA and RegB of a lineaging dataset AFTER it has gone through 2 Step RCAN Deep Learning 
//Grant Kroeschell 01/13/2022

//Enter the filepath where the RCAN_2Step_DL RegA and RegB folders are 
Path ="Z:\\Cell_Tracking_Project\\RW10711\\Lineaging\\Pos0\\SPIMB\\Reg_Sample\\Test"
File.makeDirectory(Path + "\\For_Lineaging\\")
File.makeDirectory(Path + "\\For_Lineaging\\RegB\\")
File.makeDirectory(Path + "\\For_Lineaging\\RegA\\")

//Enter first and last timepoint here 
for(i=0;i<=3;i++)
{

//Add directory of pan nuclear channel here (most liekly green)
open(Path + "\\RCAN_2Step_DL_RegA\\DL_C1_reg_"+i+".tif");

//Lower max intensity
run("Divide...", "value=260 stack"); //might need to change value, Acetree prefers max ~250 

//Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(0, 0, 81, 91); //Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");
selectWindow("DL_C1_reg_"+i+".tif");
run("Subtract...", "value=a stack");

//Switch to RegB and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Lineaging\\RegB\\Decon_reg_"+i+".tif");
close('*');

//Add directory of channel that you want to lineage (Most likely red)
open(Path +"\\\\RCAN_2Step_DL_RegB\\DL_C2_reg_"+i+".tif");

//Lower max intensity
run("Divide...", "value=260 stack"); //Might need to change value, Acetree prefers max ~250

 //Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(0, 0, 81, 91);
//Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");
selectWindow("DL_C2_reg_"+i+".tif");
run("Subtract...", "value=a stack");

//Switch to RegA and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Lineaging\\RegA\\Decon_reg_"+i+".tif");
close('*');
}
