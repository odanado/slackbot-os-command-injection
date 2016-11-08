Command = {}

Command['bash'] = {}
Command['bash']['filename'] = "Main.sh"
Command['bash']['compile'] = "cat Main.sh | tr -d '\\r' >a.out"
Command['bash']['run'] = "bash a.out"

Command['c'] = {}
Command['c']['filename'] = "Main.c"
Command['c']['compile'] = "gcc -O2 -o ./a.out ./Main.c -lm"
Command['c']['run'] = "./a.out"

DockerImage = 'odanado/os-command-injection'

StartArgs = {}
StartArgs['--net'] = 'none'
StartArgs['--cpuset-cpus'] = '0'
StartArgs['--memory'] = '128m'
StartArgs['--memory-swap'] = '128m'
StartArgs['-w'] = '/workspace'
StartArgs['--ulimit'] = ['fsize=1000000']
StartArgs['--pids-limit'] = '5'

if __name__ == '__main__':
    print(Command)
