#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
void counter(char *str);




int main(void)
{
    string s = get_string("Text: ");
    counter(s);
}


void counter(char *str)
{
    int ascii_code;
    int letters = 0;
    int sentences = 0;
    int words = 1;
    float index = 0;

    for (int i = 0; i < strlen(str); i++)
    {
        ascii_code = str[i];
        if ((ascii_code >= 65 && ascii_code <= 90) || (ascii_code >= 97 && ascii_code <= 122))
        {
            letters++;
        }
        if ((ascii_code == 46) || (ascii_code == 33) || (ascii_code == 63))
        {
            sentences++;
        }
        if (ascii_code == 32)
        {
            words++;
        }
    }

    index = 0.0588 * (100 * (float) letters / (float) words) - 0.296 * (100 * (float) sentences / (float) words) - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}

