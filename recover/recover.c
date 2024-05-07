#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[1])
{
    //If less than one command argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    //Opens file on command line
    FILE *file = fopen(argv[1], "r");

    //If file is null, return 1
    if (file == NULL)
    {
        fprintf(stderr, "Could not open file %s.\n", argv[1]);
        return 2;

    }

    //amount of blocks to loop over
    const int BLOCK_SIZE = 512;

    //char that consumes all 8bytes
    unsigned char buffer[BLOCK_SIZE];

    //create ouput file and set as null to prevent errors
    FILE *output = NULL;

    //image count that will help in the jpeg file naming
    int no_of_img = 0;

    char image[8];


    //Loop until the end of the card, will return 0 which will end loop
    while (fread(buffer, BLOCK_SIZE, 1, file) == 1)
    {
        //The block that matches these conditions is likely a jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] >= 0xe0 && buffer[3] <= 0xef)
        {
            //If jpeg discovered close output file
            if (no_of_img > 0)
            {
                fclose(output);
            }

            //to display jpeg format ###.000
            sprintf(image, "%03i.jpg", no_of_img);

            //to create new file
            output = fopen(image, "w");

            //if file is null then return 1
            if (output == NULL)
            {
                fprintf(stderr, "Could not open file %s.\n", image);
                return 3;
            }

            //Increase number of images
            no_of_img++;
        }

        //if ouput file is not empty then create image file
        if (output != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, output);
        }

    }

    fclose(output);
    fclose(file);
    return 0;
}