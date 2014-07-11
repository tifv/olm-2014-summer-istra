size(3cm);

pair[] A, B;

real alpha = 9;

for (int i = 0; i < 5; ++i) {
    A[i] = dir(72 * i + alpha);
    dot(A[i]);
    B[i] = 2 dir(72 * i + alpha);
    dot(B[i]);
}

draw(A[0]--A[2]--A[4]--A[1]--A[3]--cycle);
draw(B[0]--B[1]--B[2]--B[3]--B[4]--cycle);
draw(A[0]--B[0] ^^ A[1]--B[1] ^^ A[2]--B[2] ^^ A[3]--B[3] ^^ A[4]--B[4]);

