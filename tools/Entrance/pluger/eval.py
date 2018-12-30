def main(text:str):
    try:
        exec(text[1:])
        return "Done"
    except Exception as e:
        return "Syntex error."
