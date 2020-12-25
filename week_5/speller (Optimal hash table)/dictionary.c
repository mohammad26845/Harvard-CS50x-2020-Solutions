// Implements a dictionary's functionality

// Added libs
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

// Defult libs
#include <stdbool.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
// N = (45 + 1) * 122
const unsigned int N = ((LENGTH + 1) * 'z');

// Hash table
node *table[N];

// Number of words
int word_count = 0;


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Get hash index
    int hash_index = hash(word);

    // Create a cursor
    node *cursor = table[hash_index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            // If find it
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}


// Hashes word to a number
unsigned int hash(const char *word)
{
    // Add the askii code of all the letters
    // cat ==> (99 + 97 + 116) == (312 mod N)
    int sum_leter = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum_leter += tolower(word[i]);
    }
    return (sum_leter % N);

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Get argvn(address) for open DICT
    // Get "dictionaries/small"  OR  "dictionaries/large" OR ...
    FILE *dict_file = fopen(dictionary, "r");

    // Check file
    if (dict_file == NULL)
    {
        // If not exist ==> exit
        return false;
    }

    // Clear hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }


    // Create temp pointer for fscanf
    char word[LENGTH + 1];

    // Check the words in the file (copy to "word")
    while (fscanf(dict_file, "%s\n", word) != EOF)
    {
        // Create a new node
        node *new_node = malloc(sizeof(node));
        // Check create the new_node
        if (new_node == NULL)
        {
            return false;
        }

        // Copy Word To new_node
        strcpy(new_node->word, word);

        // Get hash index of this word
        int hash_index = hash(word);

        // If it is the first value of the table
        if (table[hash_index] == NULL)
        {
            new_node->next = NULL;
            table[hash_index] = new_node;

        }
        // If not first, add to other nodes
        else
        {
            // ADD node
            new_node->next = table[hash_index];
            table[hash_index] = new_node;

        }

        // Calc total words
        word_count++;

    }

    // Free memory (Close_file)
    fclose(dict_file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Free memory and linked list
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *temp = cursor;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }

        // As a precaution
        table[i] = NULL;
    }

    return true;
}