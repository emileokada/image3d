function [output] = get_files(directory)
    all_files = dir(directory);
    file_names = {all_files.name};
    files = regexp(file_names,'.*\.jpg','match');
    files = files(logical(~cellfun(@isempty,files)));
    files = [files{1,1:end}];
    output = cell(length(files),2);
    for i = 1:length(files)
        output{i,1} = files{i};
        output{i,2} = str2num(regexp(files{i},'\d+','match','once'));
    end
    output = sortrows(output,2);
end