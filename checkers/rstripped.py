from re import split as resplit
import os

from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8bytes


def check(process_output: bytes, judge_output: bytes, **kwargs) -> bool:
    process_lines = resplit(b'[\r\n]', utf8bytes(process_output))
    judge_lines = resplit(b'[\r\n]', utf8bytes(judge_output))

    #l'usuari fara una sola linea d'output, el nom del seu fitxer
    filename = process_lines[0].decode('utf-8')

    #fitxer esperat passat a caracters utf8
    enjin = [x.decode('utf-8') for x in list(filter(None,judge_lines))]
    strexpected = '\n'.join(map(str, enjin))
    print(strexpected)

    #rescato el nom del fitxer i l'obro
    myfile = open("/outputfiles/"+filename, "rb").read()
    file_lines = resplit(b'[\r\n]', utf8bytes(myfile))

    #fitxer de l'usuari passat a caracters utf8
    enjin = [x.decode('utf-8') for x in list(filter(None,file_lines))]
    data_to_read = '\n'.join(map(str, enjin))
    print(data_to_read)

    #comparacio
    print(file_lines)
    print(judge_lines)


    #pots esborrar ja el fitxer i que no ocupi memòria (no hi ha risc de fitxer de 3GB, perque donaria MLE)
    os.remove("/outputfiles/"+filename)

    if len(file_lines) != len(judge_lines):
        #print("ep")
        
        return CheckerResult(False, 0, "Els fitxers no tenen les mateixes línees", strexpected+"\u2719"+data_to_read)

    for process_line, judge_line in zip(file_lines, judge_lines):
        if process_line.rstrip() != judge_line.rstrip():
            #print("aaa",process_line.rstrip,judge_line.rstrip())
            return CheckerResult(False, 0, "Els fitxers no son iguals", strexpected+"\u2719"+data_to_read)

    return True
