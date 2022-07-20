#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long cc_num;  // Decleration of Credit Card Number Variable

    do
    {
        cc_num = get_long("Enter Credit Card Number: ")
    }

    while (cc_num < 0);

    // Count length of card number

    int length_num = 0;
    long cc = cc_num;

    while (cc > 0)
    {
        cc = cc / 10;
        length_num++;
    }

    // Checking for length validity

    if (length_num != 13 && length_num != 15 && length_num != 16)
    {
        printf("Invalid\n");
        return 0;
    }
    
    // Calculate checksum
    
    long x = cc_num;
    int digit1;
    int digit2;
    int sum_double_odd = 0;
    int sum_even = 0;
    int total = 0;
    int mod1;
    int mod2;
    
    
}
