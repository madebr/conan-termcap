#include <termcap.h>

#include <stdio.h>
#include <stdlib.h>

static char term_buffer[2048];

int main() {
    char *termtype = getenv ("TERM");
    int success;
    if (termtype == 0) {
        puts("Specify a terminal type with `setenv TERM <yourtype>'.");
        return EXIT_SUCCESS;
    }
    success = tgetent(term_buffer, termtype);
    if (success < 0) {
        puts("Could not access the termcap data base.");
        return EXIT_SUCCESS;
    } else if (success == 0) {
        printf("Terminal type `%s' is not defined.", termtype);
        return EXIT_SUCCESS;
    }
    return EXIT_SUCCESS;
}
