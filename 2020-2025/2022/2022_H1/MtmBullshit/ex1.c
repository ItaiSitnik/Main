#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* stringDuplicator(char* str, int times)
{
    assert(str);
    assert(times > 0);
    int len = strlen(str);
    char* out = malloc(len * times * sizeof(char));
    assert(out);
    char* copyIterator = out;
    for (int i = 0; i < times; i++) {
        strcpy(copyIterator, str);
        copyIterator = copyIterator + len;
    }
    return out;
}

int main()
{
    printf(stringDuplicator("123 ", 10));
    return 0;
}
