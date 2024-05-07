#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //To prompt for block height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    //To print the value of the stored height
    //printf("Stored: %i\n", height);

    //To print new line and hashes
    for (int i = 0; i < height; i++)
    {
    //To print the dots initially
      for (int dots = height - i - 1; dots > 0; dots--)
        {
            printf(" ");
        }
    //To print the hashes by incrementing the value
      for (int j = 0; j < i + 1; j++)
      {
           printf("#");
      }
      printf("\n");
  }

}