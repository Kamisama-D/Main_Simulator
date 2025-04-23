% Define the B' matrix
B = [-46.7244, 32.1379;
      32.1379, -32.0915];

% Define the P vector (in p.u.)
P = [0.0;
    -1.1];

% Compute the inverse of B
B_inv = inv(B);

% Compute the theta vector
theta = -B_inv * P;

% Display results
disp('B inverse:');
disp(B_inv);

disp('Theta (radians):');
disp(theta);

% Convert to degrees
theta_deg = theta * (180/pi);
disp('Theta (degrees):');
disp(theta_deg);
