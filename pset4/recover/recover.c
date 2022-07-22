#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open card.raw
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        printf("Can not find file\n");
        return 1;
    }

    // Define and initialise variables
    int count = 0;
    BYTE buffer[512];
    char filename[8];
    FILE *imgFile = NULL;

    while (fread(&buffer, 512, 1, infile) == 1)
    {
        // Checking of new jpg starting
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close prior file if it is not first
            if (count != 0)
            {
                fclose(imgFile);
            }

            sprintf(filename, "%03i.jpg", count);
            imgFile = fopen(filename, "w");
            count++;
        }
        // Write to file when found
        if (count != 0)
        {
            fwrite(&buffer, 512, 1, imgFile);
        }

    }

    fclose(infile);
    fclose(imgFile);

    return 0;

}