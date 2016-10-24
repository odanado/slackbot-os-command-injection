Command = {}

Command['bash'] = {}
Command['bash']['filename'] = "Main.sh"
Command['bash']['compile'] = "cat Main.sh | tr -d '\\r' >a.out"
Command['bash']['run'] = "bash a.out"

DockerImage = 'odanado/os-command-injection'

StartArgs = {}
StartArgs['--net'] = 'none'
StartArgs['--cpuset-cpus'] = '0'
StartArgs['--memory'] = '512m'
StartArgs['--memory-swap'] = '512m'
StartArgs['-w'] = '/workspace'
StartArgs['--ulimit'] = ['nproc=10:10', 'fsize=1000000']

if __name__ == '__main__':
    print(Command)
