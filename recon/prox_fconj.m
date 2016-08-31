function[v1,v2] = prox_fconj(y1,y2)
    d = sqrt(max(ones(size(y1)),y1.^2+y2.^2));
    v1 = y1 ./ d;
    v2 = y2 ./ d;
end