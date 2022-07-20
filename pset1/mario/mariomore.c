#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;  // declaration of variable height

    do
    {
        height = get_int("Enter height: ");  // Prompt user for height
    }
    while (height < 1 || height > 8);  // If height is less than 1 or greater than 8, go back one step


    for (int line = 0; line < height; line++)  // For creating lines
    {

        for (int blank = height - line -1; blank > 0; blank--)  // for creating blanks
        {
            printf(" ");
        }

        for (int left_hashes = 0; left_hashes < line + 1; left_hashes++)  // for creating left align hashes
        {
            printf("#");
        }

        printf("  ");  // Creating blanks between left and right align hashes

        for (int right_hashes = 0; right_hashes < line + 1; right_hashes++)  // for creating right align hashes
        {
            printf("#");
        }

        printf("\n");
    }
}