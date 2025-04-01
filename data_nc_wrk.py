# encoding: windows-1251
import json
import sys

from plugins.core.mod import decrypt, encrypt, generate_salt

base_conf = json.load(open('./data/base_data.json', 'r'))
data = open('./data/DATA.NC', 'r', encoding='windows-1251').read()
try:
    print(decrypt(data, eval(base_conf['CC'])))
except Exception as e:
    print(f'malf {e}')
d = ''
while d != 'exit':
    try:
        d = input('c: ')
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
        sys.exit()
    if d == 'y':
        datas = r"""#$#$SER[SETTINGS]
{'ADV_DATA': {'RefreshBTAEML': 'autoload_objects(_plugin_objects)', 'ReloadBTAEML': 'autoload_objects(_get_plugs())'}, 'USER_SETTINGS': {'TELEMETRY_ENABLED': 'True', 'SERVER': '127.0.0.1:8175', 'SEL_LOCALE': 'ru', 'FIRST_BOOT': 'False', 'THEME': 'hh', 'USERNAME': 'hdytjujds6w54sqarfhtssg', 'BTAEML': 'True', 'BT_SERV': '127.0.0.1:5252', 'PASSWORD': 'gyuhrdsbvdxrbsdxnb'}}
#$#$SER[LOADER_CONFIG]
CC_VERSIONS:msgr.py$%data/outdated_versions/ver_updates/1/1.py

"""
        open('./data/DATA.NC', 'w', encoding='windows-1251').write(encrypt(datas, eval(base_conf['CC'])))
    elif d == 'cc':
        base_conf['CC'] = str(generate_salt())
        json.dump(base_conf, open('./data/base_data.json', 'w'))
    elif d == 'pcc':
        print(base_conf['CC'])
    elif d == 'yc':
        open('./data/DATA.NC', 'w').write(encrypt(base_conf['DATA_NC_CLEARED'], eval(base_conf['CC'])))