//Enter the filepath where the deep learning RegA and RegB folders are 
Path = getDirectory("Select folder containing deep learning output");
File.makeDirectory(Path + "\\For_Tracking\\")
File.makeDirectory(Path + "\\For_Tracking\\RegB\\");

start = 0;
end = 118;
in_channel = "RCAN_2Step_DL_RegA"
prefix = "DL_C1"


Dialog.create("Enter Imaging Run Info");
Dialog.addNumber("Start timepoint", start);
Dialog.addNumber("End timepoint", end);
Dialog.addString("Input Channel", in_channel);
Dialog.addString("Image prefix", prefix);





og_image = Path + "\\" + in_channel + "\\" +prefix+ "_reg-0.tif";
open(og_image);
IDA = getImageID();
run("Z Project...", "projection=[Max Intensity]");
IDAP = getImageID();

waitForUser("Background Selection","Select Region with no signal, then press OK");
ROIA1 = newArray(4);
selectImage(IDAP);
getSelectionBounds(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
close('*');



//Enter first and last timepoint here 
setBatchMode(true);
for(i=start;i<=end;i++)
{

image = Path + "\\" + in_channel + "\\" +prefix+"_reg-"+i+".tif";
open(image);
ID1 = getImageID();


//Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]); //Make sure that there is no signal in the square in a max projection for this dataset, might need to adjust size or bounds
a = getValue("Mean");

selectImage(ID1);
run("Subtract...", "value=a stack");

//Switch to RegB and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Tracking\\RegB\\Decon_reg_"+i+".tif");
close('*');
}