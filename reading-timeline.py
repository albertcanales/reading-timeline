import yaml
import drawSvg as draw
import data as dat
import calculator as calc

def read_yaml(path):
    try:
        file = open(path, 'r')
        d = yaml.load(file, Loader=yaml.FullLoader)
        return d
    except IOError:
        print("Could not load %s." % path)
        exit(1)
    except yaml.YAMLError:
        print("Invalid YAML in %s." % path)
        exit(1)

def main():
    # Read data file
    data_dict = read_yaml('data.yml')
    data = dat.Data(data_dict)

    print(data)

    # Calculate positions and sizes
    pass

    # Draw the SVG
    pass

if __name__ == "__main__":
    main()
