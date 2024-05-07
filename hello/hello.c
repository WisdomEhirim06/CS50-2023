#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //To obtain the user's name as prompt
    string user = get_string("Please, what's your name: ");

    //To print out the user's name as output
    printf("Hello, %s\n", user);
}
