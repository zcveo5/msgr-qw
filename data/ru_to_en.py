main = {'й': 'y', 'ц': 'c', 'у': 'u', 'к': 'k', 'е': 'e', 'н': 'n', 'г': 'g', 'ш': 'sh', 'щ': "sh'", 'з': 'z',
        'х': 'h', 'ъ': "'", 'ф': 'f', 'ы': 'iu', 'в': 'v', 'а': 'a', 'п': 'p', 'р': 'r', 'о': 'o', 'л': 'l', 'д': 'd',
        'ж': "zh", 'э': 'e', 'я': 'ya', 'ч': 'ch', 'с': 's', 'м': 'm', 'и': 'i', 'т': 't', 'ь': '"'}

def replace_letters(text):
    ans = ''
    for i in text:
        if i.lower() in main:
            ans += main[i.lower()]
        else:
            ans += i
    return ans