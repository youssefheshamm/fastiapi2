from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"This is the root endpoint"}


# addition of a + b
@router.get("/add/{a}/{b}")
def add_numbers(a, b):
    try:
        a_num = float(a)
        b_num = float(b)
        result = a_num + b_num
        if a_num.is_integer():
            a_num = int(a_num)
        if b_num.is_integer():
            b_num = int(b_num)
        if result.is_integer():
            result = int(result)
        return {f"a = {a_num}, b = {b_num}, a + b = {result} "}
    except ValueError:
        return {"ERROR: both inputs must be numeric values"}


# checks if a word is palindrome or not
@router.get("/pal/{x}")
def palindrome(x):
    y = x
    try:
        z = float(y)
        return {"this is not a word"}
    except ValueError:
        if len(y) > 1:
            y = y.lower()
            for i in range(len(y)//2):
                if y[i] != y[-(i+1)]:
                    return {"The word is not a palindrome"}
            return {"The word is a palindrome"}
        else:
            return {"The word is too short"}
