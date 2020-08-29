from re import split as resplit
from typing import Union

from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8bytes

verdict = u"\u2717\u2713"


def check(
    process_output: bytes, judge_output: bytes, point_value: float, feedback: bool = True, **kwargs
) -> Union[CheckerResult, bool]:

    judge_input = list(filter(None, resplit(b'[\r\n]', utf8bytes(kwargs["judge_input"]))))
    process_lines = list(filter(None, resplit(b'[\r\n]', utf8bytes(process_output))))
    judge_lines = list(filter(None, resplit(b'[\r\n]', utf8bytes(judge_output))))
    wronganswers = ""
    

    enjin = [x.decode('utf-8') for x in judge_input]
    strinput = '\n'.join(map(str, enjin))
    print(strinput)


    if len(process_lines) > len(judge_lines):
        return CheckerResult(False,0,"S'han tornat més linies de les esperades")

    if not judge_lines:
        return True

    cases = [verdict[0]] * len(judge_lines)
    count = 0

    for i, (process_line, judge_line) in enumerate(zip(process_lines, judge_lines)):
        if process_line.strip() == judge_line.strip():
            cases[i] = verdict[1]
            count += 1
        else:
            tmpl = str(i)+"\u2720"+str(judge_line.strip().decode('utf-8'))+"\u2720"+str(process_line.strip().decode('utf-8'))+"\u2721"
            wronganswers+=(tmpl)

    return CheckerResult(
        count == len(judge_lines), point_value * (1.0 * count / len(judge_lines)), str(count)+"/"+str(len(judge_lines)) if feedback else "", strinput+"\u2719"+str(wronganswers)+ "\u2719"+str(len(judge_input))+ "\u2719"+str(len(judge_lines))   )


check.run_on_error = False  # type: ignore
