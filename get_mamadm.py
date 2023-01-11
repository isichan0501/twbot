
import subprocess


def get_mamadm(new_word='興味あれば@usernameに連絡してみてください！'):
    cmd = "C:\\Users\\sibuy\\go\\bin\\mamadm.exe -t 1"
    returncode = subprocess.check_output(cmd)

    word = returncode.decode().replace('mama','mαmα').replace('MAMA', 'mαmα').replace('まま', 'mαmα').replace('ママ','mαmα')
    result = ""
    for w in word.split():
        if 'ブログ' in w or '固定ツイート' in w:
            w = new_word
            
        result += w + "\n"
    return result
    
    return 


if __name__ == "__main__":

    for pp in range(10):
        msg = get_mamadm()
        print(msg)
    import pdb;pdb.set_trace()

    msg = get_mamadm()
    msg.split()
    print(msg)




