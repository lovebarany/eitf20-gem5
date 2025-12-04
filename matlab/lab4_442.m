ht_l1; % Hit Time for L1
ht_l2; % Hit Time for L2
mp_l2; % Miss Penalty for L2
block_size = [16, 32, 64, 128, 256];
cpi  = [];
mr_l1 = []; % Miss Rate for L1
mr_l2 = []; % Miss Rate for L2
AMAT = ht_l1 + mr_l1.*(ht_l2 + mr_l2 .* mp_l2);%Average Memory Access Time
 
figure(1);
plot(block_size, cpi,'bd-', block_size, AMAT,'ms-');
legend('CPI', 'AMAT');% 
set(gca,'xtick',block_size);
title('matrix-multiply'); % to be changed
grid on;
xlabel('Block size (Bytes)');
