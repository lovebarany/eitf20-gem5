#include <iostream>
#include <stdlib.h>
#include <time.h>


int binary_search(int list[], int length, int to_be_found);

int main()
{
    int list_length = 300;
    int item_to_find = 2497;
    int list[list_length];
    int temp_int = 0;
    unsigned seed = 123526732;
    srand(seed);
    /* Generates a pseudo-random non decreasing sequence (list) of size list_length */
    for (int i = 0; i < list_length; i++)
    {
        temp_int = rand() % 30 + temp_int;
        list[i] = temp_int;
    }
    std::cout << "Result from iterative procedure: " << binary_search(list, list_length, item_to_find) << std::endl;
    
    return 0;
}

/* Iterative solution */
int binary_search(int list[], int length, int to_be_found){
    
    int p = 0;
    int r = length - 1;
    int q = (r + p) / 2;
    int counter = 0;

    while (p <= r)
    {
        counter++;
        if (list[q] == to_be_found)
            return q;
        else
        {
            if (list[q] < to_be_found) 
            {
                p = q + 1;
                q = (r + p) / 2;
            }
            else
            {
                r = q - 1;
                q = (r + p) / 2;    
            }
        }
    }
    return -1;
}

