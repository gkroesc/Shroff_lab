Path = getDir("Path to AceTree tif and tifr parent folder");
File.makeDirectory(Path + "\\For_MIPAV\\");
File.makeDirectory(Path + "\\For_MIPAV\\RegA\\");
File.makeDirectory(Path + "\\For_MIPAV\\RegB\\");

start = 1;
redstart = 200;
end = 471;
slice_num = 201;

Dialog.create("Enter Image Info");
Dialog.addNumber("Start timepoint", start);
Dialog.addNumber("Red channel start timepoint", redstart);
Dialog.addNumber("End timepoint", end);
Dialog.addNumber("Number of slices per timepoint", slice_num);
Dialog.show();
start = Dialog.getNumber();
redstart = Dialog.getNumber();
end = Dialog.getNumber();
slice_num = Dialog.getNumber();

File.openSequence(Path + "\\tif", "virtual");
setBatchMode(true);
for (i = start; i <=end; i++) {
run("Make Substack...", "slices=1-"+slice_num+" delete");
saveAs("Tiff", Path + "\\For_MIPAV\\RegB\\Decon_reg_"+i+".tif");
close();
}

close('*')

File.openSequence(Path + "\\tifr", "virtual");
setBatchMode(true);
for (i = redstart; i <=end; i++) {
run("Make Substack...", "slices=1-"+slice_num+" delete");
saveAs("Tiff", Path + "\\For_MIPAV\\RegA\\Decon_reg_"+i+".tif");
close();
}