set_assoc = [1, 2,  4, 8, 16];
miss_rate_ui = [ ]; % miss rates obtained for unified caches for instructions
miss_rate_ud = [ ]; % miss rates obtained for unified caches for data
miss_rate_si=[ ]; % miss rates obtained for instruction caches
miss_rate_sd=[ ]; % miss rates obtained for data caches

figure(1);
plot(set_assoc, miss_rate_ui,'bd-', set_assoc, miss_rate_si,'cs-');
grid on;
legend('Unified instruction', 'Separate instruction');
title('matrix-multiply'); % to be changed depending on the used benchmark
xlabel('Set Associativity (blocks/set)');
ylabel('Miss Rate');
set(gca,'xtick',set_assoc);

figure(2);
plot(set_assoc, miss_rate_ud, 'ro-', set_assoc, miss_rate_sd, 'ms-');
legend('Unified data', 'Separate data');
grid on;
title('matrix-multiply'); % to be changed depending on the used benchmark
xlabel('Set Associativity (blocks/set)');
ylabel('Miss Rate');
 
