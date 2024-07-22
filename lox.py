#!/usr/bin/python3

import sys

from typing import List


class Lox:    
    had_error: bool = False

    @classmethod
    def run_file(kls, file_name: str) -> None:
        with open(file_name, "r") as f:
            source_code = f.read()
            kls.run(source_code)
            if kls.had_error:
                exit(65)
    
    @classmethod
    def run_prompt(kls) -> None:
        while True:
            print("> ", end="")
            line: str = input()
            if not line:
                break
            kls.run(line)
            kls.had_error = False
    
    
    @classmethod
    def run(kls, source: str) -> None:
        from scanner import Scanner
        scanner = Scanner(source)
        tokens: List[str] = scanner.scan_tokens()

        for token in tokens:
            print(tokens)

    @classmethod
    def error(kls, line: int, message: str):
        kls.report(line, "", message)
    
    @classmethod
    def report(kls, line: int, where: str, message:str):
        print(f"[line {line}] Error {where}: {message}")
        had_error = True

if __name__ == '__main__':
    print(sys.argv)
    try:
        if len(sys.argv) > 2:
            print("Usage: pylox [script]")
            exit(64)
        elif len(sys.argv) == 2:
                Lox.run_file(sys.argv[0])
        else:
            Lox.run_prompt()
    except IOError as e:
        print("IOError: ", e)
        raise