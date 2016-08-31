function v = div(u1,u2)
    [n1,n2] = size(u1);
    v = zeros(size(u1));
    for ii = 1:n1
        for jj = 1:n2
            if ii == 1
                t = u1(ii,jj);
            elseif ii == n1
                t = -u1(n1-1,jj);
            else
                t = u1(ii,jj) - u1(ii-1,jj);
            end
            
            if jj == 1
                t = t + u2(ii,jj);
            elseif jj == n2
                t = t - u2(ii,n2-1);
            else
                t = t + u2(ii,jj) - u2(ii,jj-1);
            end
            v(ii,jj) = t;
        end
    end
end