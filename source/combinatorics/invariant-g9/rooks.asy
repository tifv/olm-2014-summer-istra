size(5cm);

int n = 8;

for (int i = 0; i <= n; ++i) {
    draw((0,i)--(n,i));
    draw((i,0)--(i,n));
}

label("$1$", (0+0.5, 1+0.5));
label("$2$", (0+0.5, 0+0.5));
label("$3$", (1+0.5, 0+0.5));

label("$1$", (n-2+0.5, n-1+0.5));
label("$2$", (n-1+0.5, n-1+0.5));
label("$3$", (n-1+0.5, n-2+0.5));

label("{\tt a8}", (0+0.5, n-1+0.5));
label("{\tt h1}", (n-1+0.5, 0+0.5));

