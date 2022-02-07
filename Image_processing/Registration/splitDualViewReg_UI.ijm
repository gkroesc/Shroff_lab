macro "splitDualViewReg"{
// This macro is to create a simple User Interface within ImageJ and 
// launch the reg_3d_affine.exe console and pass arguments to the console
// for split dual-view dual-color imaging
// Min Guo, May 28, 2019


// close all windows
while (nImages>0) {
          selectImage(nImages); 
          close(); 
      }

//*** Default setup****
// Default folders/files for CUDA app
appPath = "C://Users//kroeschellga//Desktop//splitDualViewReg//CudaApp//";


bgValue = 100;  //background value for bio-sample images

bgValueBeads = 100; //background value for beads images


// Default parameters
nameA = "SPIMB-";

pixelSizeAx = 0.1625;
pixelSizeAy = 0.1625;
pixelSizeAz = 1;

//initial matrix for beads image
tmxChoice= "2D registration"; //"Default", "Customized" or "2D registration"

dQuery = false; // show GPU information or not
deviceNum = 0; // GPU device #

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

// registration parameters for beads
Dialog.addMessage("\n");
Dialog.addMessage("Set Beads Registration Options");
items = newArray("Default", "Customized",  "2D registration");
Dialog.setInsets(0, 40, 0);
Dialog.addRadioButtonGroup("Initial matrix", items, 1, 3, tmxChoice);

//GPU device settings
Dialog.addMessage("\n");
Dialog.addMessage("Set GPU Options");
Dialog.addCheckbox("Show GUP Device Information", dQuery);
Dialog.addNumber("GPU Device #", deviceNum);

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

// registration
tmxChoice = Dialog.getRadioButton();// 0, 1, 2;
if(tmxChoice=="Default"){
	flagInitialTmx = 0;
	fileTmx = "Balabalabala";
}
else if(tmxChoice=="Customized"){
	flagInitialTmx = 1; // 
	fileTmx =  File.openDialog("Select transform matrix file");
}
else if(tmxChoice=="2D registration"){
	flagInitialTmx = 2;
	fileTmx = "Balabalabala";
}

//Set GPU Options
dQuery = Dialog.getCheckbox();
deviceNum = Dialog.getNumber();

//CUDA app

//*****ROI cropping***** ///
//files and folders for cropping
folderCropped = "Cropped//";
folderCroppedSPIMA1 = "C1//";
folderCroppedSPIMA2 = "C2//";

fileNameCroppedSPIMA1 = "C1_";
fileNameCroppedSPIMA2 = "C2_";

folderCroppedBeads = "Beads//";
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
makeRectangle(0, 0, 1152, 576);
run("Duplicate...", " ");
IDAP1 = getImageID();
selectImage(IDAP);
makeRectangle(1152, 0, 1152, 576);
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
ROIA2[0] = ROIA2[0] + 1152;
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

// *****registration and deconvultion ****** //
// choose CUDA app
cudaExe = appPath + "reg_3d_affine.exe";


// **** Beads **** //
folderRegBeads = "Reg_Beads\\";
pathRegBeads = pathOutput + folderRegBeads;
File.makeDirectory(pathRegBeads);

// registration for beads
//interpolation
pathSPIMA0 = pathOutput + folderCropped + folderCroppedBeads;
pathSPIMB0 = pathOutput + folderCropped + folderCroppedBeads;
nameA0 = fileNameCroppedBeadsSPIMA1;
nameB0 = fileNameCroppedBeadsSPIMA2;
pathOutput0 = pathRegBeads;

print("Performing registration for beads ...\n...\n");
result = exec(cudaExe,pathOutput0,pathSPIMA0,pathSPIMB0,nameA0,nameB0,0,0,1,0, 
			pixelSizeAx,pixelSizeAy,pixelSizeAz,pixelSizeAx,pixelSizeAy,pixelSizeAz, 2,
			0,flagInitialTmx, fileTmx, 1, 1,dQuery,deviceNum);
print("Beads registration: \n"+result);


// **** Sample **** //
// registration for sample
pathFinal = pathOutput + "Reg_Sample\\";
pathSPIMA0 = pathOutput + folderCropped + folderCroppedSPIMA1;
pathSPIMB0 = pathOutput + folderCropped + folderCroppedSPIMA2;
nameA0 = fileNameCroppedSPIMA1;
nameB0 = fileNameCroppedSPIMA2;
pathOutput0 = pathFinal;
flagInitialTmx = 1;
fileTmx = pathRegBeads + "TMX\\Matrix_0.tmx";
dQuery= 0;

print("Performing registration for sample ...\n...\n");
result = exec(cudaExe,pathOutput0,pathSPIMA0,pathSPIMB0,nameA0,nameB0,imageNumStart,imageNumEnd,
			imageNumInterval,imageNumTest, 
			pixelSizeAx,pixelSizeAy,pixelSizeAz,pixelSizeAx,pixelSizeAy,pixelSizeAz, 0,
			0,flagInitialTmx, fileTmx, 1, 1,dQuery,deviceNum);
print("Sample registration \n"+result);

print("\n\n ***All processing completed !!! *** \n"+result);
}