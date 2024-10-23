#include <iostream>
#include <string>
#include <cctype>
#include <format>
#include <terminalProps.hpp>

int main(){
    TerminalProps terminal = TerminalProps();

    terminal.enableRaw();

    char inp_char;

    while (std::cin.get(inp_char) && inp_char != 'q'){
        if (iscntrl(inp_char)){
            std::cout << "%d\n" << inp_char;
        }else{
            std::cout << std::format("%d ({})\n", inp_char);
        }
    }
    return 0;
}