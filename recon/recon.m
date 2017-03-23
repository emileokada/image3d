classdef recon
   properties
      im_dir;
      files;
      height;
      width;
      mid;
      vertical_spacing = 50;
      vertical_resolution;
      shadow_bands;
      xy_scaling = 10;
      scaled_width;
      scaled_mid;
      teeth = 100;
      increments;
   end
   methods
       function obj = recon(im_directory)
           obj.im_dir = im_directory;
           obj.files = get_files(im_directory);
           [obj.height,obj.width] = ...
               size(imread([im_directory,obj.files{1,1}]));
           obj.mid = round(obj.width/2);
           
           obj.scaled_width = round(obj.width/obj.xy_scaling);
           obj.scaled_mid = round(obj.scaled_width/2);
           obj.vertical_resolution = ...
               floor(obj.height/obj.vertical_spacing);

           [obj.increments, ~] = size(obj.files);
           obj.shadow_bands = cell(obj.increments,obj.vertical_resolution);

           for i = 1:obj.increments
               %img = double(rgb2gray(...
               %    imread([im_directory,obj.files{i,1}])))/255;
               img = double(...
                   imread([im_directory,obj.files{i,1}]))/255;
               
               img = round(img);
               for j = 1:obj.vertical_resolution
                   obj.shadow_bands{i,j} = ...
                       read_bands(obj,img(j*obj.vertical_spacing,:));
               end
           end

       end
       function theta = increment2theta(obj,i)
           theta = 2*pi*obj.files{i,2}/obj.teeth;
       end
       function bands = read_bands(obj,row)
           d = diff(row);
           left_edges = find(~(d+1))-obj.mid;
           right_edges = find(~(d-1))+1-obj.mid;
           
           if length(left_edges)>length(right_edges)
               right_edges = [right_edges,length(row)];
           elseif length(left_edges)<length(right_edges)
               left_edges = [1, left_edges];
           end
           if length(left_edges) == length(right_edges) ...
                   && ~isempty(left_edges)
               bands = [left_edges; right_edges]';
           else
               bands = [];
           end
       end
       function is_in = in_band(obj,theta,m,n,bands)
           d = -(m-obj.scaled_mid)*sin(theta)+...
               (n-obj.scaled_mid)*cos(theta);
           [h,~] = size(bands);
           for i = 1:h
               if bands(i,1) <= obj.xy_scaling*d && ...
                       obj.xy_scaling*d <= bands(i,2)
                   is_in = true;
                   return
               end
           end
           is_in = false;
       end
       function mat = intersected_area(obj, z_coord) 
           mat = ones(obj.scaled_width,obj.scaled_width);
           for i = 1:obj.scaled_width
               for j = 1:obj.scaled_width
                   for k = 1:obj.increments
                       if ~obj.in_band(obj.increment2theta(k),...
                               i,j,obj.shadow_bands{k,z_coord})
                           mat(i,j) = 0;
                           break;
                       end
                   end
               end
           end
       end
       function vol = volume(obj)
           vol = zeros(obj.scaled_width,obj.scaled_width);
           for i = 1:obj.vertical_resolution
               vol(:,:,i) = obj.intersected_area(...
                   obj.vertical_resolution-i+1);
           end
       end
   end
end
