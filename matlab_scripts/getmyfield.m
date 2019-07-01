function S2=getmyfield(S1,queriedField)

if isstruct(S1)
    % Get all fieldnames of S1
    fieldArray=fieldnames(S1);

    % Find any match with the queried field. You can also use isfield().
    % If there is a match return the value of S1.(queriedField),
    % else perform a loop and recurse this function.
    matchTF=strcmp(queriedField,fieldArray);
    if any(matchTF)
        S2=S1.(fieldArray{matchTF});
        return;
    else
        S2=[];
        i=0; % an iterator count
        while isempty(S2)
            i=i+1;
            S2=getmyfield(S1.(fieldArray{i}),queriedField);
        end
    end
else
    S2=[];
end

end