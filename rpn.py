from random import randint
from asciimatics.screen import Screen

class Frame:

    def __init__(self, screen):
        self.left   = (screen.width - 60) / 2
        self.right  = self.left + 60
        self.bottom = screen.height - 1

        self.screen = screen

    def clear_screen(self):
        for i in range(self.bottom):
            self.screen.move(self.left , i)
            self.screen.draw(self.right, i, char=' ', bg=7)

    def print_multiline_exception(self, ex):
        lines = [' ' * 30] + ex.lines + [' ' * 30, 'Press enter to continue']
        for i in range(len(lines)):
            line = lines[i]
            line += ' ' * (30 - len(line))
            self.screen.print_at(line,
                                 self.left + 15, 5 + i,
                                 colour=7,
                                 bg=1)

        self.screen.refresh()

        while self.screen.get_key() != 13:
            pass

class MultilineException(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.lines = []
        words = message.split(' ')
        buffer = ''
        for word in words:
            if len(buffer) + len(word) + 1 < 28:
                buffer += ' ' + word
                continue
            elif len(buffer) + len(word) + 1 == 28:
                buffer += ' ' + word
            self.lines.append(buffer)
            buffer = ' ' + word
        if buffer:
            self.lines.append(buffer)

class Calculator:

    def __init__(self):
        self.input_buffer = ''

        self.stack = []

    def command(self, cmd_number):

        if cmd_number in (range(0x30, 0x3A) + [46]):
            self.input_buffer += chr(cmd_number)
            return

        elif cmd_number in range(301, 400):
            self.input_buffer = str(self.stack[-(cmd_number % 300)])
            return

        func = {
            -300 : self._reduce_input_buffer,
            -102 : self._pop_stack,
            -205 : self._swap,
            13   : self._append_buffer,
            42   : self._multiply,
            43   : self._add,
            45   : self._subtract,
            47   : self._divide
        }.get(cmd_number, None)

        if func:
            func()
        else:
            self.input_buffer += str(cmd_number)

    def get_input_buffer(self):
        return self.input_buffer

    def get_stack(self):
        return self.stack

    def _append_buffer(self):
        if not self.input_buffer and not self.stack:
            return
        self.stack.append(float(self.input_buffer) if self.input_buffer else self.stack[-1])
        self.input_buffer = ''
        if len(self.stack) > 99:
            self.stack.pop(0)

    def _reduce_input_buffer(self):
        self.input_buffer = self.input_buffer[:-1]

    def _pop_stack(self):
        if self.stack:
            self.stack.pop()

    def _swap(self):
        if len(self.stack) >= 2:
            temp = self.stack[-1]
            self.stack[-1] = self.stack[-2]
            self.stack[-2] = temp

    def _multiply(self):
        if len(self.stack) + (1 if self.input_buffer else 0) < 2:
            raise MultilineException('Too few arguments for multiplication!')

        temp = float(self.input_buffer) if self.input_buffer else self.stack.pop()
        self.stack[-1] *= temp

        self.input_buffer = ''

    def _add(self):
        if len(self.stack) + (1 if self.input_buffer else 0) < 2:
            raise MultilineException('Too few arguments for addition!')

        temp = float(self.input_buffer) if self.input_buffer else self.stack.pop()
        self.stack[-1] += temp

        self.input_buffer = ''

    def _subtract(self):
        if len(self.stack) + (1 if self.input_buffer else 0) < 2:
            raise MultilineException('Too few arguments for subtraction!')

        temp = float(self.input_buffer) if self.input_buffer else self.stack.pop()
        self.stack[-1] -= temp

        self.input_buffer = ''

    def _divide(self):
        if len(self.stack) + (1 if self.input_buffer else 0) < 2:
            raise MultilineException('Too few arguments for division!')

        temp = float(self.input_buffer) if self.input_buffer else self.stack.pop()

        if temp == 0:
            raise MultilineException("You divided by zero. You know you can't do that.")

        self.stack[-1] /= temp

        self.input_buffer = ''

def demo(screen):
    frame = Frame(screen)
    calculator = Calculator()
    string = ''
    stack_selector = 0
    while True:
        frame.clear_screen()
        string = calculator.get_input_buffer()
        screen.print_at(string[-60:],
                        frame.left, frame.bottom,
                        colour=0,
                        bg=7)

        i = 0
        stack = calculator.get_stack()
        for item in reversed(stack[-25:None]):
            # We want the colon of the stack tag to always be 3
            # in from the right edge of the frame
            stack_tag = ':{}'.format(i + 1)
            stack_tag += ' ' * (3 - len(stack_tag))

            colour, bg = (7, 0) if i + 1 == stack_selector else (0, 7)

            printable = '{} {}'.format(item, stack_tag)
            screen.print_at(printable,
                            frame.right - len(printable), frame.bottom - 2 - i,
                            colour=colour,
                            bg=bg)
            i += 1

        ev = screen.get_key()

        if ev in (ord('Q'), ord('q')):
            return

        # Up arrow
        elif ev == -204:
            stack_selector = stack_selector + 1 if stack_selector < len(stack) else stack_selector

        # Down Arrow
        elif ev == -206:
            stack_selector = stack_selector - 1 if stack_selector > 0 else 0

        # If we hit enter while highlighting an item in the stack, move item into input buffer
        elif stack_selector > 0 and ev == 13:
            calculator.command(300 + stack_selector)
            stack_selector = 0

        elif ev == None:
            pass

        else:
            try:
                stack_selector = 0
                calculator.command(ev)
            except MultilineException as ex:
                frame.print_multiline_exception(ex)

        screen.refresh()

Screen.wrapper(demo)
