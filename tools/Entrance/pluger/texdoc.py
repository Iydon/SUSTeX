import os


def main(text:str):
    try:
        os.system(text)
    except:
        return "Error."
