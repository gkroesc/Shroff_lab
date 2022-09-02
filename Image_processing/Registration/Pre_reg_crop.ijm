
bgValue = 100;  //background value for bio-sample images

bgValueBeads = 100; //background value for beads images


// Default parameters
nameA = "SPIMB-";

pixelSizeAx = 0.1625;
pixelSizeAy = 0.1625;
pixelSizeAz = 1;


// log file name
fileLog = "cropping log.txt";

pathSPIMA = getDirectory("Select input image folder");
fileBeadsA =  File.openDialog("Select beads image");
pathOutput = getDirectory("Select output folder");

SPIMAList = getFileList(pathSPIMA);
totalImageNum = lengthOf(SPIMAList);
imageNumStart = 0;
imageNumEnd = totalImageNum - 1;
imageNumInterval = 1;

print("Set input parameters...\n...\n");

Dialog.create("split Dual Color Registration");
	//input images parameters
Dialog.addString("Input Directory",pathSPIMA,80);
Dialog.addString("Image Name",nameA,20);
Dialog.addString("Output Directory",pathOutput,80);
Dialog.addNumber("Start #", imageNumStart);
Dialog.addNumber("End #", imageNumEnd);
Dialog.addNumber("Interval", imageNumInterval);
Dialog.addNumber("Test #", imageNumStart);
Dialog.addMessage("Input Pixel Size");
Dialog.addNumber("ImageA x, y, z", pixelSizeAx,4,6,"um");
Dialog.setInsets(-28, 100, 0);
Dialog.addNumber(" ", pixelSizeAy,4,6,"um");
Dialog.setInsets(-28, 200, 0);
Dialog.addNumber(" ", pixelSizeAz,4,6,"um");



Dialog.show();

//Get parameters from dialog
pathSPIMA = Dialog.getString();
nameA = Dialog.getString();
pathOutput = Dialog.getString();

imageNumStart = Dialog.getNumber();
imageNumEnd = Dialog.getNumber();
imageNumInterval = Dialog.getNumber();
imageNumTest = Dialog.getNumber();

pixelSizeAx = Dialog.getNumber();
pixelSizeAy = Dialog.getNumber();
pixelSizeAz = Dialog.getNumber();


//*****ROI cropping***** ///
//files and folders for cropping
folderCropped = "Cropped\\";
folderCroppedSPIMA1 = "C1\\";
folderCroppedSPIMA2 = "C2\\";

fileNameCroppedSPIMA1 = "C1_";
fileNameCroppedSPIMA2 = "C2_";

folderCroppedBeads = "Bead\\";
fileNameCroppedBeadsSPIMA1 = "Beads_C1_";
fileNameCroppedBeadsSPIMA2 = "Beads_C2_";

File.makeDirectory(pathOutput);
File.makeDirectory(pathOutput + folderCropped);
File.makeDirectory(pathOutput + folderCropped + folderCroppedSPIMA1);
File.makeDirectory(pathOutput + folderCropped + folderCroppedSPIMA2);
File.makeDirectory(pathOutput + folderCropped + folderCroppedBeads);


// ROI selecting
print("ROI selecting ...\n...\n");
fileSPIMA = pathSPIMA + nameA + imageNumStart + ".tif";
open(fileSPIMA);
IDA = getImageID();
run("Z Project...", "projection=[Max Intensity]");
run("Subtract...", "value=" + bgValue + " stack");
IDAP = getImageID();
selectImage(IDA);
close();
selectImage(IDAP);
makeRectangle(0, 0, 1024, 512);
run("Duplicate...", " ");
IDAP1 = getImageID();
selectImage(IDAP);
makeRectangle(1024, 0, 1024, 512);
run("Duplicate...", " ");
IDAP2 = getImageID();
selectImage(IDAP);
close();

waitForUser("ROI Selection","Select Region of Interest for all 4 images, then press OK");
ROIA1 = newArray(4);
ROIA2 = newArray(4);
selectImage(IDAP1);
getSelectionBounds(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
close();
selectImage(IDAP2);
getSelectionBounds(ROIA2[0], ROIA2[1], ROIA2[2], ROIA2[3]);
close();

//do cropping
ROIA2[0] = ROIA2[0] + 1024;
setBatchMode(true); //

//crop beads files
print("Performing cropping for beads ...\n...\n");
fileSPIMA1 = pathOutput + folderCropped + folderCroppedBeads + fileNameCroppedBeadsSPIMA1 + 0 + ".tif";
fileSPIMA2 = pathOutput + folderCropped + folderCroppedBeads + fileNameCroppedBeadsSPIMA2 + 0 + ".tif";

open(fileBeadsA);
IDA = getImageID();
makeRectangle(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
run("Duplicate...", "duplicate");
IDA1 = getImageID();
run("Subtract...", "value=" + bgValueBeads + " stack");
saveAs("Tiff", fileSPIMA1);
close();
makeRectangle(ROIA2[0], ROIA2[1], ROIA2[2], ROIA2[3]);
run("Duplicate...", "duplicate");
IDA2 = getImageID();
run("Subtract...", "value=" + bgValueBeads + " stack");
saveAs("Tiff", fileSPIMA2);
close();
selectImage(IDA);
close();

//crop sample files
print("Performing cropping for sample ...\n...\n");
for(i = imageNumStart; i<= imageNumEnd; i = i + imageNumInterval){
	fileSPIMA = pathSPIMA + nameA + i + ".tif";
	fileSPIMA1 = pathOutput + folderCropped + folderCroppedSPIMA1 + fileNameCroppedSPIMA1 + i + ".tif";
	fileSPIMA2 = pathOutput + folderCropped + folderCroppedSPIMA2 + fileNameCroppedSPIMA2 + i + ".tif";

	open(fileSPIMA);
	IDA = getImageID();
	makeRectangle(ROIA1[0], ROIA1[1], ROIA1[2], ROIA1[3]);
	run("Duplicate...", "duplicate");
	IDA1 = getImageID();
	run("Subtract...", "value=" + bgValue + " stack");
	saveAs("Tiff", fileSPIMA1);
	close();
	makeRectangle(ROIA2[0], ROIA2[1], ROIA2[2], ROIA2[3]);
	run("Duplicate...", "duplicate");
	IDA2 = getImageID();
	run("Subtract...", "value=" + bgValue + " stack");
	saveAs("Tiff", fileSPIMA2);
	close();
	selectImage(IDA);
	close();}

//record cropping configurations to log file
flog = File.open(pathOutput + folderCropped+fileLog);
print(flog, "Cropping: single view dual color \n");
print(flog, "...image time points range:  " + imageNumStart + "-"+ imageNumInterval +"-"+ imageNumEnd +"\n");
print(flog, "...image time point for ROI selecting:  " + imageNumTest +"\n");
//print(flog, "... ... ... rotation and interpolation during ROI selecting:  no\n");
print(flog, "... ... ... SPIMA Color 1 coordinates for cropping (x, y, width, height):  " + ROIA1[0] +", " + ROIA1[1] +", " + ROIA1[2]+", " + ROIA1[3] +"\n");
print(flog, "... ... ... SPIMA Color 2 coordinates for cropping (x, y, width, height):  " + ROIA2[0] +", " + ROIA2[1] +", " + ROIA2[2]+", " + ROIA2[3] +"\n");
print(flog,"... background subtraction value:" + bgValue + "\n");

File.close(flog);
