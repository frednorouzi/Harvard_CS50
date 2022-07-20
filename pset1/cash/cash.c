#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // Declaration variables
    int cents;
    float dollars;

    do
    {
        dollars = get_float("Enter change amount($): ");  // Ask user for an amount of change
        cents = round(dollars * 100);  // Round the change to nearest penny
    }
    while (cents < 0);  // If user input was less than zero, prompt again

    // Calculate number of largest coins possible
    int quarter_num = cents / 25;
    int dime_num = (cents % 25) / 10;
    int nikle_num = ((cents % 25) % 10) / 5;
    int penny_num = ((cents % 25) % 10) % 5;

    int coins = quarter_num + dime_num + nikle_num + penny_num;

    printf("%i\n", coins);
}

