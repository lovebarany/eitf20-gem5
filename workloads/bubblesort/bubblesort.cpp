#include <iostream>

void bubbleSort(int *array, int n)
{
    bool swapped = true;
    int j = 0;
    int temp;

    while (swapped)
    {
        swapped = false;
        j++;
        for (int i = 0; i < n - j; ++i)
        {
            if (array[i] > array[i + 1])
            {
                temp = array[i];
                array[i] = array[i + 1];
                array[i + 1] = temp;
                swapped = true;
            }
        }
    }
}

int main()
{
    int array[] = {95, 45, 48, 98, 485, 65, 54, 478, 1, 2325, 1238, 12, 4328, 1028, 2, 13};
    int n = sizeof(array)/sizeof(array[0]);


    bubbleSort(array, n);
    std::cout << "Bubblesort done" << std::endl;
    return 0;
}
