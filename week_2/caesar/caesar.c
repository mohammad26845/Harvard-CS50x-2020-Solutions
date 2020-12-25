#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>


int main(int argc, string argv[])
{
    
    string input_s = argv[1];
    

    if (argc == 2 && isdigit(*argv[1]))

    {
        for (int i = 0; i < strlen(input_s); i++)
        {
            if (!isdigit(input_s[i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }

        int k = atoi(argv[1]);

        string s = get_string("plaintext: "); // get text
        printf("ciphertext: ");


        for (int i = 0, n = strlen(s) ; i < n; i++)
        {

            if (s[i] >= 'a' && s[i] <= 'z')
            {
                printf("%c", (((s[i] - 'a') + k) % 26) + 'a');
            }
            else if (s[i] >= 'A' && s[i] <= 'Z')
            {
                printf("%c", (((s[i] - 'A') + k) % 26) + 'A');
            }

            else

            {
                printf("%c", s[i]);
            }
        }

        printf("\n");
        return 0;
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}