#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAX 9  //Set maximum number of candidates

typedef struct {  //Each candidate has two fields; name and votes

    string name;
    int votes;
}
candidate;

candidate candidates[MAX]; //defines a global array "candidates"

int candidate_count  //defines global variable which representing the number of candidates in the election

//function prototypes
bool vote(string name);
void print_winner(void);

int main(argc, argv[])
{
    
    if (argc != 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1
    }
    
}