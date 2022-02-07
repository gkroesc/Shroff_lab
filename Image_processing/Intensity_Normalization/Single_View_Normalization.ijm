//Enter the filepath where the deep learning RegA and RegB folders are 
Path ="Z:\\Cell_Tracking_Project\\DCR6485_rpm1\\012522\\Pos2"
File.makeDirectory(Path + "\\For_Tracking\\")
File.makeDirectory(Path + "\\For_Tracking\\RegB\\")

//Enter first and last timepoint here 
for(i=0;i<=118;i++)
{

//Add directory of untwisting channel here 
open(Path + "\\DenseDecon_DL_RegA\\DL_C1_reg-"+i+".tif");


//Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(0, 0, 68, 91); //Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");

selectWindow("DL_C1_reg-"+i+".tif");
run("Subtract...", "value=a stack");

//Switch to RegB and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Tracking\\RegB\\Decon_reg_"+i+".tif");
close('*');
}