 function convcsv(file,foldername)
    load (file)
    mkdir(foldername);
    for [val, key] = Data
        for i=1:size(fieldnames(val))(1)
          
            if ismatrix((getmyfield(val,fieldnames(val)(i)))) %if the returned value is an matrix
              
                if isnumeric((getmyfield(val,fieldnames(val)(i))))%if the returned value is an number
                  file = cell2mat(fieldnames(val)(i)); % name of the file is the name of the column
                  filename = sprintf('%s/%s.csv',foldername,file)
                  csvwrite(filename,getmyfield(val,fieldnames(val)(i)))
                endif
                
            endif
            
        endfor
    endfor
    
    for [val, key] = Data.Info.frame %for frame case
        filename = sprintf('%s/%s.csv',foldername,key)
        csvwrite(filename,getmyfield(Data.Info ,key))
    endfor


    for [val, key] = Data.Traitement.Brute %for Data.Traitement.Brute case
      filename = sprintf('%s/%s.csv',foldername,key)
      csvwrite(filename,getmyfield(Data.Traitement ,key))
    endfor
    
    for [val, key] = Data.Markers.Brute %for Data.Markers.Brute case
      filename = sprintf('%s/%s.csv',foldername,key)
      csvwrite(filename,getmyfield(Data.Markers ,key))
    endfor
    
    for [val, key] = Data.Markers.RButte %for Data.Markers.RButte case
      filename = sprintf('%s/%s.csv',foldername,key)
      csvwrite(filename,getmyfield(Data.Markers ,key))
    endfor
    
    for [val, key] = Data.Markers.RButteORamp %for Data.Markers.RButteORamp case
      filename = sprintf('%s/%s.csv',foldername,key)
      csvwrite(filename,getmyfield(Data.Markers ,key))
    endfor
    
      for [val, key] = Data.InfoRider %for string values case in InfoRider
             if iscell(val)
                string = sprintf('key : %s type :%s',key,cell2mat(val));
                disp(string)
                filename = sprintf('%s/%s.csv',foldername,key)
                cell2csv(filename,getmyfield(Data ,key),',')
                
             endif
       endfor
end

    