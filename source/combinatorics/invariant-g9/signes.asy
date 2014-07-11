size(5cm);

int n = 6;

for (int i = 0; i <= n; ++i) {
    draw((0,i)--(n,i));
    draw((i,0)--(i,n));
}

for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
        if (i == 1 && j == n-1) {
            label("$-$", (i+0.5, j+0.5));
            continue;
        }
        label("$+$", (i+0.5, j+0.5));
    }
}

