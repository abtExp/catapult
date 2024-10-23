#include <stdlib.h>
#include <terminalProps.hpp>

TerminalProps::TerminalProps(){
    tcgetattr(STDIN_FILENO, &original_state);
}

TerminalProps::~TerminalProps(){
    if (raw_enabled){
        disableRaw();
    }
}


void TerminalProps::enableRaw(){
    if (raw_enabled) return;

    struct termios raw;

    tcgetattr(STDIN_FILENO, &raw);

    raw.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
    raw.c_oflag &= ~(OPOST);
    raw.c_cflag |= (CS8);
    raw.c_lflag &= ~(ECHO | ICANON | IEXTEN | ISIG);

    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);

    this->raw_enabled = true;
}

void TerminalProps::disableRaw(){
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &original_state);
}

