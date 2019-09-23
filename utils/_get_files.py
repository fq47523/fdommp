import os




def get_scripts(path):
    files_list = []
    dirs = os.listdir(path)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(path+d):
            pass
        else:
            files_list.append(d)
    return files_list

def get_roles(args):
    roles_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(args+d):
            roles_list.append(d)
        else:
            pass
    return roles_list
