//This Macro is run on both RegA and RegB of a lineaging dataset AFTER it has gone through 2 Step RCAN Deep Learning 
//Grant Kroeschell 01/13/2022

//Enter the filepath where the RCAN_2Step_DL RegA and RegB folders are 
Path = getDirectory("Select folder containing deep learning output");
File.makeDirectory(Path + "\\For_Lineaging\\");
File.makeDirectory(Path + "\\For_Lineaging\\RegB\\");
File.makeDirectory(Path + "\\For_Lineaging\\RegA\\");

//Enter first and last timepoint here 
start = 0;
end = 418;
pnc = "RegB"
pnc_prefix = "DL_C2"
tc = "RegA"
tc_prefix = "DL_C1"


//Add the first and last time point as the two values here
Dialog.create("Enter first and last timepoints");
Dialog.addNumber("Start", start);
Dialog.addNumber("End", end);
Dialog.addString("Pan-Nuclear channel", pnc);
Dialog.addString("Pan-Nuclear channel image prefix", pnc_prefix);
Dialog.addString("Tracking channel", tc);
Dialog.addString("Tracking channel image prefix", tc_prefix);
Dialog.show();
start = Dialog.getNumber();
end = Dialog.getNumber();
pnc = Dialog.getString();
pnc_prefix = Dialog.getString();
tc = Dialog.getString();
tc_prefix = Dialog.getString();





og_image_a = Path + "\\RCAN_2Step_DL_" + pnc + "\\" +pnc_prefix+ "_reg_0.tif";
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
for(i = start; i <= end; i++)
{

//Add directory of pan nuclear channel here (most liekly green)
image_pnc = Path + "\\RCAN_2Step_DL_" + pnc + "\\" +pnc_prefix+ "_reg_"+i+".tif";
open(image_pnc);

//Lower max intensity
run("Divide...", "value=260 stack"); //might need to change value, Acetree prefers max ~250 
ID1 = getImageID();

//Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
a = getValue("Mean");

selectImage(ID1);
run("Subtract...", "value=a stack");

//Switch to RegB and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Lineaging\\"+pnc+"\\Decon_reg_"+i+".tif");
close('*');

//Add directory of channel that you want to lineage (Most likely red)
image_tc =  Path +"\\RCAN_2Step_DL_" +tc+ "\\" +tc_prefix+ "_reg_"+i+".tif";
open(image_tc);


//Lower max intensity
run("Divide...", "value=260 stack"); //Might need to change value, Acetree prefers max ~250
ID2 = getImageID();

 //Normalize for background noise
run("Z Project...", "projection=[Average Intensity]");
makeRectangle(ROIB1[0], ROIB1[1], ROIB1[2], ROIB1[3]);
b = getValue("Mean");

selectImage(ID2);
run("Subtract...", "value=b stack");

//Switch to RegA and rename all images with prefix Decon_reg
saveAs("Tiff", Path + "\\For_Lineaging\\"+pnc+"\\Decon_reg_"+i+".tif");
close('*');
}
