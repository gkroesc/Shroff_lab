//This Macro is run on both RegA and RegB of a tracking dataset AFTER it has gone through Deep Learning 
//Grant Kroeschell 01/13/2022

//Enter the filepath where the deep learning RegA and RegB folders are 
Path ="Z:\\Cell_Tracking_Project\\RW10711\\Lineaging\\Pos0\\SPIMB\\Reg_Sample\\Test"
File.makeDirectory(Path + "\\For_Tracking\\")
File.makeDirectory(Path + "\\For_Tracking\\RegB\\")
File.makeDirectory(Path + "\\For_Tracking\\RegA\\")

//Enter first and last timepoint here 
for(i=0;i<=3;i++)
{

//Add directory of untwisting channel here 
open(Path + "\\DenseDecon_DL_RegA\\DL_C1_reg_"+i+".tif");


//Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(0, 0, 81, 91); //Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");

selectWindow("DL_C1_reg_"+i+".tif");
run("Subtract...", "value=a stack");

//Switch to RegB and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Tracking\\RegB\\Decon_reg_"+i+".tif");
close('*');

//Add directory of channel that you want to track (Most likely red)
open(Path +"\\\\RCAN_2Step_DL_RegB\\DL_C2_reg_"+i+".tif");

// Rescale so that there are 308 slices in z
run("Scale...", "x=1.0 y=1.0 z=.987 width=325 height=425 depth=308 interpolation=Bilinear average process create title=Decon_reg_"+i+".tif");


 //Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(0, 0, 81, 91);
//Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");
selectWindow("DL_C2_reg_"+i+".tif");
run("Subtract...", "value=a stack");

//Switch to RegA and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Tracking\\RegA\\Decon_reg_"+i+".tif");
close('*');
}

