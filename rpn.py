from random import randint
from asciimatics.screen import Screen

class Frame:

    def __init__(self, screen):
        self.left   = (screen.width - 60) / 2
        self.right  = self.left + 60
        self.bottom = 30
        
        self.screen = screen

        
    def clear_screen(self):
        for i in range(self.bottom):
            self.screen.move(self.left , i)
            self.screen.draw(self.right, i, char=' ', bg=7)


class Calculator:

    def __init__(self):
        self.input_buffer = ''
        
        self.stack = []
        
    def command(self, cmd_number):
        
        if cmd_number in (range(0x30, 0x3A) + [46]):
            self.input_buffer += chr(cmd_number)

        # Backspace
        elif cmd_number == -300:
            self.input_buffer = self.input_buffer[:-1]
            
        # del
        elif cmd_number == -102:
            self.stack.pop()
            
        # right arrow
        elif cmd_number == -205:
            temp = self.stack[-1]
            self.stack[-1] = self.stack[-2]
            self.stack[-2] = temp
         
        # Enter
        elif cmd_number == 13:
            self._append_buffer()
        
        # *
        elif cmd_number == 42:
            pass
        else:
            self.input_buffer += str(cmd_number)
            
    def get_input_buffer(self):
        return self.input_buffer
        
    def get_stack(self):
        return self.stack
        
    def _append_buffer(self):
        if not self.input_buffer and not self.stack:
            return False
        self.stack.append(float(self.input_buffer) if self.input_buffer else self.stack[-1])
        self.input_buffer = ''
        return True


def demo(screen):
    frame = Frame(screen)
    calculator = Calculator()
    string = ''
    while True:
        frame.clear_screen()
        string = calculator.get_input_buffer()
        screen.print_at(string[-60:],
                        frame.left, frame.bottom,
                        colour=0,
                        bg=7)
        
        i = 0
        for item in reversed(calculator.get_stack()[-25:]):
            # We want the colon of the stack tag to always be 3
            # in from the right edge of the frame
            stack_tag = ':{}'.format(i + 1)
            stack_tag += ' ' * (3 - len(stack_tag))
            
            printable = '{} {}'.format(item, stack_tag)
            screen.print_at(printable,
                            frame.right - len(printable), frame.bottom - 2 - i,
                            colour=0,
                            bg=7)
            i += 1
        
                        
        ev = screen.get_key()

        if ev in (ord('Q'), ord('q')):
            return

        elif ev == None:
            pass
            
        else:
            calculator.command(ev)
            

        screen.refresh()

Screen.wrapper(demo)
