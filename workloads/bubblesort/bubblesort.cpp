#include <iostream>
#include <gem5/m5ops.h>
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
    // this is where we start recording statistics
    m5_work_begin(0, 0);
    int array[] = {95, 45, 48, 98, 485, 65, 54, 478, 1, 2325, 1238, 12, 4328, 1028, 2, 13};
    int n = sizeof(array)/sizeof(array[0]);


    bubbleSort(array, n);
    // and this is where we end
    m5_work_end(0, 0);
    std::cout << "Bubblesort done" << std::endl;
    return 0;
}
