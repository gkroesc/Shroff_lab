Path = getDirectory("Path to Input Images")
File.makeDirectory(Path + "\\tifr\\")

start = 1;
end = 418;
start_slice = 1
end_slice = 211
image_prefix = "Decon_reg"

Dialog.create("Enter Imaging Run Info");
Dialog.addNumber("Start timepoint", start);
Dialog.addNumber("End timepoint", end);
Dialog.addNumber("Start slice", start_slice);
Dialog.addNumber("End slice", end_slice);
Dialog.addString("Image prefix", image_prefix);

Dialog.show();
start = Dialog.getNumber();
end = Dialog.getNumber();
start_slice = Dialog.getNumber();
end_slice = Dialog.getNumber();
image_prefix = Dialog.getString();

setBatchMode(true);
for (i = start; i <=end; i++) {
open(Path + "//" +image_prefix +"_"+i+".tif");
setMinAndMax(0, 255);
call("ij.ImagePlus.setDefault16bitRange", 8);
run("Stack to Images");
	for (s=start_slice;s<=end_slice; s++){
		m=IJ.pad(s,2);
		k=IJ.pad(s, 4);
		
		

		selectWindow(image_prefix +"_"+i+"-"+k);
		setOption("ScaleConversions", true);
		run("8-bit");
		t=IJ.pad(i, 3);
		saveAs("Tiff", Path +"/tifr/"+image_prefix+"-t"+t+"-p"+m+".tif");
		
	}
close("*");
}
