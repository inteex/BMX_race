function extract_csv(indir)
  
  directory = dir(indir);
  
  for i=1:length(directory)
      folder = directory(i).folder;
      subfolder = directory(i).name;
      str = sprintf('%s\\%s\\*.mat',folder, subfolder)
      files = dir(str);
      N = length(files)   % total number of files 
      % loop for each file 
      for i = 1:N
         thisfile = files(i).name
         file_directory = sprintf('%s\\%s\\%s',folder, subfolder, thisfile);
         foldername = thisfile(21:length(thisfile)-4)
         folder_directory = sprintf('%s\\%s\\%s',folder, subfolder, foldername);
         convcsv(file_directory, folder_directory)
      endfor
      
   end
  
  
  %files = dir('*.mat') ;    % you are in folder of csv files
  %N = length(files) ;   % total number of files 
  % loop for each file 
      %for i = 1:N
        %thisfile = files(i).name;
        %convcsv(thisfile)
      %endfor
end