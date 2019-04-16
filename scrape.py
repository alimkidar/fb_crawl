import pandas as pd
from scraper_new import *

def main():
    data = []
    # Getting email and password from user to login into his/her profile
    email = input('\nEnter your Facebook Email: ')
    password = getpass.getpass()
    flag = True
    while flag:
        try:
            scrl = int(input('Scroll: '))
            flag = False
        except:
            print("Wrong Number!")
    pages = get_input('input.txt')
    load_fb()
    login(email,password)

    for page in pages:
        if 'http' in page:
            print('Load', page)
            go_to(page)
            scroll(scrl)
            open_seemore()
            data += generate_data(page) 
            print('Ok.')
    df = pd.DataFrame(data)
    columns = ['name', 'username', 'bedge', 'prof_link', 'time(gmt+7)', 'timestamp', 'post_utl', 'convo', 'likes_count', 'comments_count','photos_count', 'source']
    df = df[columns]
    df.to_csv('result.csv')
    print('Done!')

def get_input(file):
    f = open(file, 'r', newline='\n')
    text = f.read()
    x = text.split('\n')
    return x
main()