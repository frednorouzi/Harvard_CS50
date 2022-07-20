#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int main(void)
{
    int num_l = 0, num_w = 1, num_s = 0;  // declaration variables

    string text = get_string("Text: ");  // asking user input



    for (int i = 0; i < strlen(text); i++)
    {
        char ch = text[i];

        if (isalpha(ch))  //count number of letters
        {
            num_l++;
        }
        else if (isspace(ch))  //count number of words
        {
            num_w++;
        }
        else if (ch == '.' || ch == '!' || ch == '?')  //count number of sentnces
        {
            num_s++;
        }
    }

    float L = (num_l * 100.0f) / num_w;
    float S = (num_s * 100.0f) / num_w;

    float grade = (0.0588 * L - 0.296 * S - 15.8);

    if (grade < 16 && grade >= 1)
    {
        printf("Grade %i\n", (int) round(grade));
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }

}