// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 17576;

// Hash table
node *table[N];

// Words in the dictionary
unsigned int total_words = 0;

// Hash node from the word
unsigned int hashNode = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    hashNode = hash(word);
    node *n = table[hashNode];

    while (n != NULL)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 17576;
    int m;

    while ((m = tolower(*word++)))
    {
        hash = ((hash << 5) + hash) + m;
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    FILE *dic = fopen(dictionary, "r");

    if (dic != NULL)
    {
        while (fscanf(dic, "%s", word) != EOF)
        {
            node *n = malloc(sizeof(node));

            if (n != NULL)
            {
                hashNode = hash(word);

                strcpy(n->word, word);

                n->next = table[hashNode];

                table[hashNode] = n;

                total_words ++;
            }

        }
        fclose(dic);
    }
    else
    {
        return false;
    }
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return total_words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        while (n)
        {
            node *tmp = n;

            n = n->next;

            free(tmp);
        }

        if (i == N - 1 && n == NULL)
        {
            return true;
        }
    }
    return false;
}