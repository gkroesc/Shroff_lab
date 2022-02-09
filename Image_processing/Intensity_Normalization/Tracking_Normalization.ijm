//This Macro is run on both RegA and RegB of a tracking dataset AFTER it has gone through Deep Learning 
//Grant Kroeschell 01/13/2022

//Enter the filepath where the deep learning RegA and RegB folders are 
Path = getDirectory("Select folder containing deep learning output");
File.makeDirectory(Path + "\\For_Tracking\\")
File.makeDirectory(Path + "\\For_Tracking\\RegB\\")
File.makeDirectory(Path + "\\For_Tracking\\RegA\\")

start = 0;
end = 118;
uc = "RegA"
uc_prefix = "DL_C1"
tc = "RegB"
tc_prefix = "DL_C2"


//Add the first and last time point as the two values here
Dialog.create("Enter first and last timepoints");
Dialog.addNumber("Start", start);
Dialog.addNumber("End", end);
Dialog.addString("Untwisting channel", uc);
Dialog.addString("Untwisting channel image prefix", uc_prefix);
Dialog.addString("Tracking channel", tc);
Dialog.addString("Tracking channel image prefix", tc_prefix);
Dialog.show();
start = Dialog.getNumber();
end = Dialog.getNumber();
uc = Dialog.getString();
uc_prefix = Dialog.getString();
tc = Dialog.getString();
tc_prefix = Dialog.getString();




og_image_a = Path + "\\DenseDecon_DL_" + uc + "\\" +uc_prefix+ "_reg_0.tif";
open(og_image_a);
IDA = getImageID();
run("Z Project...", "projection=[Max Intensity]");
IDAP = getImageID();

waitForUser("Background Selection","Select Region with no signal, then press OK");
ROIA1 = newArray(4);
selectImage(IDAP);
getSelectionBounds(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
close('*');



og_image_b = Path + "\\RCAN_2Step_DL_" + tc + "\\" +tc_prefix+ "_reg_0.tif";
open(og_image_b);
IDB = getImageID();
run("Z Project...", "projection=[Max Intensity]");
IDBP = getImageID();


waitForUser("Background Selection","Select Region with no signal, then press OK");
ROIB1 = newArray(4);
selectImage(IDBP);
getSelectionBounds(ROIB1[0], ROIB1[1], ROIB1[2], ROIB1[3]);
close("*");


//Start the loop 
for(i=start;i<=end;i++)
{

//Add directory of untwisting channel here 
image_uc = Path + "\\DenseDecon_DL_" + uc + "\\"+uc_prefix+"_reg_"+i+".tif";
open(image_uc);
ID1 = getImageID();


//Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]); //Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");

selectImage(ID1);
run("Subtract...", "value=a stack");

//Switch to RegB and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Tracking\\"+tc+"\\Decon_reg_"+i+".tif");
close('*');

//Add directory of channel that you want to track (Most likely red)
image_tc = Path +"\\RCAN_2Step_DL_"+tc+"\\"+tc_prefix+"_reg_"+i+".tif";
open(image_tc);

// Rescale so that there are 308 slices in z
run("Scale...", "x=1.0 y=1.0 z=.987 width=325 height=425 depth=308 interpolation=Bilinear average process create title=Decon_reg_"+i+".tif");
ID2 = getImageID();

 //Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(ROIB1[0], ROIB1[1], ROIB1[2], ROIB1[3]);
//Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
b = getValue("Mean");
selectImage(ID2);
run("Subtract...", "value=b stack");

//Switch to RegA and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Tracking\\"+uc+"\\Decon_reg_"+i+".tif");
close('*');
}

