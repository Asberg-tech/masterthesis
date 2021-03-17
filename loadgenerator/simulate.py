from edityml import edit_yaml
from applyyaml import apply_yaml
from checklimit import check_errors

def main():
    
    for i in range(500, 1500, 100):
        if not check_errors():
            print("\nStarting loadgenerator with ,  %s , users!\n" % (i))
            edit_yaml(i)
            apply_yaml()
        else:
            print("\n***Loadgenerator maxed out at, %s , users***" % (i-100))
            break
if __name__ == '__main__':
    main()

