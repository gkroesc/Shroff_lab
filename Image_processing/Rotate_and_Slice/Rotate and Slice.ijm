Path = "\\\\nibibaimdata-01\\shroff_lab\\Cell_Tracking_Project\\101521_NG8413_lineaging\\Reg_Sample\\For_Lineaging"
File.makeDirectory(Path + "\\Rotated\\")
File.makeDirectory(Path + "\\Rotated\\RegB\\")
File.makeDirectory(Path + "\\Rotated\\RegA\\")
File.makeDirectory(Path + "\\StarryNite\\")
File.makeDirectory(Path + "\\StarryNite\\tif\\")
File.makeDirectory(Path + "\\StarryNite\\tifr\\")


start = 0 //First timepoint that you want to rotate (generally 0)
startslice = 176 //Z slice where signal first appears AFTER rotating
redstart = 200 //Timepoint you want the red channel to be added to dataset	 
twitch = 369 //Timepoint twitching begins at
stop = twitch + 1
savefinal = 1


x1=70.0; y1=20.0; z1=-70.0; //Degrees in x, y, and z that embryo needs to be rotated in order to be in canonical orientation

rotation="z-angle="+z1+" y-angle="+y1+" x-angle="+x1+" interpolation=[Cubic B-Spline] background=0.0 adjust resample";

file=File.open(Path + "\\StarryNite\\matricies.txt");
	
	print(file, " Rotation    "+"z-angle   "+z1+" y-angle   "+y1+" x-angle   "+x1+ "\n ");



setBatchMode(true);
for (i=start;i<=stop;i++){
	open(Path + "\\RegB\\Decon_reg_"+i+".tif");
	rename("Decon_reg_"+i+".tif");
	
	run("TransformJ Rotate", rotation);
	
	//getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	//Timestring = "Date" + "-" + hour+":"+minute+":"+second;
	//print(Timestring);
	
	setMinAndMax(0, 721);
	run("8-bit");

	selectWindow("Decon_reg_"+i+".tif rotated");
	getDimensions(w, h, channels, slices, frames);
	run("Stack Splitter", "number="+slices+"");
	for (s=000;s<=200;s++){
		k=IJ.pad(s+1, 2);
		m=s+startslice;
		n=IJ.pad(m, 3);
	
		selectWindow("slice0"+n+"_Decon_reg_"+i+".tif rotated");
		t=IJ.pad(i+1, 3);
		saveAs("Tiff", Path + "\\StarryNite\\tif\\Decon-t"+t+"-p"+k+".tif");
		
	}
	

    if(savefinal == 1){
    	if(i==twitch-1){
	selectWindow("Decon_reg_"+i+".tif rotated");
    run("Slice Keeper", "first="+startslice+" last="+startslice+200+" increment=1");
    saveAs("Tiff", Path + "\\Rotated\\RegB\\Decon_r_reg_"+t+".tif");
    }}
	
	run("Close All");
}



setBatchMode(true);
 for (i=redstart;i<=stop;i++){   
    open(Path + "\\RegA\\Decon_reg_"+i+".tif");
    rename("Decon_reg_"+i+".tif");
    
    run("TransformJ Rotate", rotation);

	
	setMinAndMax(0, 591);
	run("8-bit");

	selectWindow("Decon_reg_"+i+".tif rotated");
	getDimensions(w, h, channels, slices, frames);
	run("Stack Splitter", "number="+slices+"");
	for (s=000;s<=200;s++){
		k=IJ.pad(s+1, 2);
		m=s+startslice;
		n=IJ.pad(m, 3);

		selectWindow("slice0"+n+"_Decon_reg_"+i+".tif rotated");
		t=IJ.pad(i+1, 3);
		saveAs("Tiff", Path +"\\StarryNite\\tifr\\Decon-t"+t+"-p"+k+".tif");
		
	}
	

	selectWindow("Decon_reg_"+i+".tif rotated");
    if(savefinal == 1){
    	if(i==twitch-1){
	selectWindow("Decon_reg_"+i+".tif rotated");
    run("Slice Keeper", "first="+startslice+" last="+startslice+200+" increment=1");
    saveAs("Tiff", Path + "\\Rotated\\RegA\\Decon_r_reg_"+t+".tif");
    	}}
	run("Close All");
}


