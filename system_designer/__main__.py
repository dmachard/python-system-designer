from system_designer import designer
# 
import argparse

def setup_cli():
    """setup command-line arguments"""
    options = argparse.ArgumentParser()          
    options.add_argument("-y", help="architecture yaml file", required=True) 
    options.add_argument("-o", help="output file path", required=True) 
    options.add_argument("-f", help="output file format (default: %(default)r)", default="png") 
    options.add_argument('-d', action='store_true', help="debug mode")

    return options

def start_up():
    """called on start"""
    options = setup_cli()
    args = options.parse_args()

    designer.generate(archi_file=args.y, output_file=args.o, output_format=args.f, debug=args.d)

if __name__ == '__main__':
    start_up()