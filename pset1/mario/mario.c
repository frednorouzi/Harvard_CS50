# include <cs50.h>
# include <stdio.h>

int main(void)
{
    int height;  // declaration of variable height

    do
    {
        height = get_int("Enter height: ");    // Prompt user for height
    }

    while (height < 1 || height > 8);   // If height is less than 1 or greater than 8, go back one step

    for (int line = 0; line < height; line++)  // For creating lines
    {
        for (int blank = height - line - 1; blank > 0; blank--)  // for creating blank
        {
            printf(" ");
        }
        for (int hash = 0; hash < line + 1; hash++)  // for creating hashes
        {
            printf("#");
        }
        printf("\n");    // for printing new line
    }

}