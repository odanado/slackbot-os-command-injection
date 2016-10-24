Command = {}

Command['bash'] = {}
Command['bash']['filename'] = "Main.sh"
Command['bash']['compile'] = "cat Main.sh | tr -d '\\r' >a.out"
Command['bash']['run'] = "bash a.out"

DockerImage = 'odanado/os-command-injection'

if __name__ == '__main__':
    print(Command)
