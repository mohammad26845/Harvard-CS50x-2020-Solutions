#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int cents;
    float n;
    int total_coins = 0;
    int temp;
    int mod;

    do
    {
        n = get_float("Change owed: ");
    }
    while (n < 0);



    cents = round(n * 100);

    temp = cents / 25;
    mod = cents % 25;
    total_coins += temp;

    temp = mod / 10;
    mod = mod % 10;
    total_coins += temp;

    temp = mod / 5;
    mod = mod % 5;
    total_coins += temp;

    temp = mod / 1;
    mod = mod % 1;
    total_coins += temp;

    printf("%i \n", total_coins);
}