//This Macro can be used to crop and and rescale images so that they are ready for deep learning
//Should be used instead of Min's SplitDualViewReg macro if bypass mode was used on the DiSPIM

//Enter path to the better SPIm images
Path = "H:\\011922_DCR6485xGG23\\DCR6485xGG23_2\\Pos2\\SPIMB"
File.makeDirectory(Path + "\\RegA\\")

//Add The first and last time point to the loop here 
for (i = 81; i <= 119; i++) {
open(Path + "\\SPIMB-"+i+".tif");
makeRectangle(899, 69, 325, 425); //Might need to adjust locaton of this rectangle, use max projection for reference
run("Crop");

//Adjust scaling in z so each image has 308 slices
run("Scale...", "x=1.0 y=1.0 z=6.16 width=325 height=425 depth=308 interpolation=Bilinear average process create");
saveAs("Tiff", Path + "\\RegA\\C1_reg-"+i+".tif");
close('*');
}
