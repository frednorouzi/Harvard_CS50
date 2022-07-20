#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool test_valid_key(string s);

int main(int argc, string argv[])
{

    if (argc != 2 || !test_valid_key(argv[1]))   // checking for two arguments and only digit for second argument
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }


    int key = atoi(argv[1]);  // convert string to integer


    if (key < 0)  // checking non negative integer for second argument
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {

        string txt = get_string("plaintText: ");  //asking user input for plain text

        printf("ciphertext: ");

        // calculating ciphertext for both lower and upper case letters

        for (int i = 0; i < strlen(txt); i++)
            {
                char c = txt[i];

                if islower(c)
                    printf("%c", (((c + key) - 'a') % 26) + 'a');

                else if isupper(c)
                    printf("%c", (((c + key) - 'A') % 26) + 'A');


                else
                    printf("%c", c);
            }
            printf("\n");
            return 0;
    }
}

bool test_valid_key(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        char c = s[i];
        if (!isdigit(c))
        {
            return false;
        }

    }
    return true;
}