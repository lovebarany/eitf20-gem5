#include <stdio.h>

int main()
{
    const int size = 30;
    int first_int[size][size], second_int[size][size], multiply_int[size][size];
    float first_float[size][size], second_float[size][size], multiply_float[size][size];

    printf("First iteration: integer matrices \n");
    printf("Populating the first and second matrix...\n");
    for(int x=0; x<size; x++)
    {
        for(int y=0; y<size; y++)
        {
            first_int[x][y] = x + y;
            second_int[x][y] = (4 * x) + (7 * y);
        }
    }
    printf("Done!\n");

    printf("Multiplying the matrixes...\n");
    for(int c=0; c<size; c++)
    {
        for(int d=0; d<size; d++)
        {
            int sum_int = 0;
            for(int k=0; k<size; k++)
            {
                sum_int += first_int[c][k] * second_int[k][d];
            }
           multiply_int[c][d] = sum_int;
        }
    }
    printf("Done!\n");

    printf("Calculating the sum of all elements in the matrix...\n");
    long int sum_int = 0;
    for(int x=0; x<size; x++)
        for(int y=0; y<size; y++)
            sum_int += multiply_int[x][y];
    printf("Done\n");

    printf("The integer sum is %ld\n", sum_int);

    printf("Second iteration: floating point matrices \n");
    printf("Populating the first and second matrix...\n");
    for(int x=0; x<size; x++)
    {
        for(int y=0; y<size; y++)
        {
            first_float[x][y] = (2.37321238f * (float)x) + (-1.37123459f * (float)y);
	    first_float[x][y] = first_float[x][y] / 1.12395f;
            second_float[x][y] = (-0.64271237f * (float)x) + (3.5786147f * (float)y);
        }
    }
    printf("Done!\n");

    printf("Multiplying the matrixes...\n");
    for(int c=0; c<size; c++)
    {
        for(int d=0; d<size; d++)
        {
            float sum_float = 0;
            for(int k=0; k<size; k++)
            {
                sum_float += first_float[c][k] * second_float[k][d];
            }
           multiply_float[c][d] = sum_float;
        }
    }
    printf("Done!\n");

    printf("Calculating the sum of all elements in the matrix...\n");
    float sum_float = 0;
    for(int x=0; x<size; x++)
        for(int y=0; y<size; y++)
            sum_float += multiply_float[x][y];
    printf("Done\n");

    printf("The floating point sum is %f\n", sum_float);
    return 0;
}
