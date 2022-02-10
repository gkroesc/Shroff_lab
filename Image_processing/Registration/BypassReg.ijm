//This Macro can be used to crop and and rescale images so that they are ready for deep learning
//Should be used instead of Min's SplitDualViewReg macro if bypass mode was used on the DiSPIM

Path = getDirectory("Select folder containing positions");

start_pos = 1;
end_pos =5;
spim = "B";
start_tp = 0;
end_tp = 118;
bgValue = 100

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

for (v = start_pos; v <= end_pos; v++)
{
//Add the path to the image files up to Pos#, adjust SPIMA/B to whichever is better base off of Max_proj_1
current_path = Path + "\\Pos"+v+"\\SPIM" + spim ;

fileSPIM = current_path + "\\SPIM" + spim + "_0.tif";
open(fileSPIM);
IDA = getImageID();
run("Z Project...", "projection=[Max Intensity]");
run("Subtract...", "value=" + bgValue + " stack");
IDAP = getImageID();
selectImage(IDA);
close();

waitForUser("ROI Selection","Select Region of Interest, then press OK");
ROIA1 = newArray(4);
selectImage(IDAP);
getSelectionBounds(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
close();


//Enter path to the better SPIm images
File.makeDirectory(current_path + "\\RegA\\");

//Add The first and last time point to the loop here 
for (i = start_tp; i <= end_tp; i++) {
open(current_path + "\\SPIM" + spim + "-"+i+".tif");
makeRectangle(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]); //Might need to adjust locaton of this rectangle, use max projection for reference
run("Crop");

//Adjust scaling in z so each image has 308 slices
run("Scale...", "x=1.0 y=1.0 z=6.16 width=325 height=425 depth=308 interpolation=Bilinear average process create");
saveAs("Tiff", current_path + "\\RegA\\C1_reg_"+i+".tif");
close('*');
}
}