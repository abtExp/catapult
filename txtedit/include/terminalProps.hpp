// Checking if a windows system or not, as unistd.h is limited to posix systems
#ifdef _WIN32
    #include <windows.h>
    #include <conio.h>
#else
    #include<termios.h>
    #include<unistd.h>
#endif

class TerminalProps{
    private:
        struct termios original_state;
        bool raw_enabled = false;
    
    public:
        TerminalProps();
        ~TerminalProps();

        // I don't know what these 2 lines do
        TerminalProps(const TerminalProps&) = delete;
        TerminalProps& operator=(const TerminalProps&) = delete;

        void enableRaw();
        void disableRaw();
};