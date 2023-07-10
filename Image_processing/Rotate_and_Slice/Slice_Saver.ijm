Path = getDirectory("Path to Input Images")
setBatchMode(true);
for (i = 200; i <=201; i++) {
open(Path + "/Decon_reg_"+i+".tif");
run("Stack to Images");
	for (s=1;s<=211; s++){
		m=IJ.pad(s,2);
		k=IJ.pad(s, 4);
		
		

		selectWindow("Decon_reg_"+i+"-"+k);
		setOption("ScaleConversions", true);
		run("8-bit");
		t=IJ.pad(i, 3);
		saveAs("Tiff", Path +"/tifr/Decon_reg-t"+t+"-p"+m+".tif");
		
	}
close("*");
}