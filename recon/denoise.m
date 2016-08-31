function [u] = denoise(init_image,lambda)
    norm2 = @(w) sum(sum(w.^2));
    grad1 = @(w) w([2:end end],:) - w;
    grad2 = @(w) w(:,[2:end end]) - w;
    
    % Parameters of the algorithm
    reg_param = 1/lambda;
    tau = 1/sqrt(8);
    sigma = 1/sqrt(8);
    theta = 1;
    itr = 200;

    % Initialise variables
    xvar = zeros(size(init_image));
    barx = zeros(size(init_image));
    y1var = zeros(size(init_image));
    y2var = zeros(size(init_image));

    % Main loop
    for iterates = 1:itr
      xold = xvar;
      xvar = ((xvar + tau * div(y1var,y2var)) + tau*lambda*init_image)/(1+tau*lambda);
      barx = xvar + theta*(xvar-xold);
      [y1var,y2var] = prox_fconj(y1var+sigma*grad1(barx),y2var+sigma*grad2(barx));
    end
    u = xvar;
end