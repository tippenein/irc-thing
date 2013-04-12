import socket
import re
from module.geef import random_definition, geef_happiness

from tornado import iostream
from tornado import ioloop

HOST = "irc.freenode.net"
PORT = 6667
IDENT = "sloth_bot"
REALNAME = "sloth_bot"
CHAN = ""  # ADD THE CHANNEL NAME HERE
NICK = ""

# regex for getting source of pings
# :username!~host@199.199.252.252 PRIVMSG #channel :message blah vlah
RE_ORIGIN = re.compile(r'([^!]*)!?([^@]*)@?(.*)')


def parse_sender(src):
    match = RE_ORIGIN.match(src or '')
    return match.groups()  # Nickname, username, hostname


class IRCBot(object):

    def __init__(self, chan, nick):
        self.chan = chan
        self.nick = nick
        s = socket.socket()  # default is fine
        self._stream = iostream.IOStream(s)
        self._stream.connect((HOST, PORT), self.join)

    def join(self):
        self._write(('NICK', self.nick))
        self._write(('USER', IDENT, '+iw', HOST), self.nick)
        self._write(('JOIN', self.chan))
        print "joined {}".format(self.chan)
        self._stream.read_until('\r\n', self._read)

    def _read(self, data):
        print "raw data: {}".format(data)
        if data.startswith(':'):
            source, data = data[1:].split(' ', 1)
        else:
            source = None

        if ' :' in data:
            args, data = data.split(' :', 1)
        else:
            args, data = data, ''
            args = args.split()
        # Parse the source (where the data came from)
        nickname, username, hostname = parse_sender(source)

        if 'PING' in args:
            # PING :asimov.freenode.net
            self._write(('PONG', data))
        if '!' in data:
            self.handle_bang(nickname, data)
        self._stream.read_until('\r\n', self._read)

    def handle_bang(self, nickname, data):
        ''' handle any bang command
        '''
        if '!scat' in data:
            self._write(('PRIVMSG', self.chan), text="{}: {}".format(
                                    nickname, geef_happiness()))

        if '!random' in data:
            self._write(('PRIVMSG', self.chan), text="{}: {}".format(
                                   nickname, random_definition()))
        pass

    def _write(self, args, text=None):
        if text:
            self._stream.write('{} :{}\r\n'.format(' '.join(args), text))
        else:
            self._stream.write('{}\r\n'.format(' '.join(args)))

    def shutdown_bot(self):
        ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    if CHAN and NICK:
        IRCBot(CHAN, NICK)
    else:
        chan = raw_input("channel? ")
        nick = raw_input("nickname? ")
        if chan[0] != '#':
            chan = '#' + chan
        IRCBot(chan, nick)
    ioloop.IOLoop.instance().start()
