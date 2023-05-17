import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests as r
import json

def red(filename):
    with open(filename, 'r') as f:return f.read()
def get(url):
    return r.get(url).content.decode('utf-8')
url='https://api.hypixel.net/skyblock/bazaar'
item_data = json.loads(red('db.json'))['items']

def get_stock():
    data = json.loads(get(url))
    item_db = {}; item_to_buy = []
    for item in item_data:
        if not 'npc_sell_price' in item:continue
        item_db[item['id']] = item['npc_sell_price']

    for item in data['products'].values():
        item_id = item['product_id']
        if not item['buy_summary'][:5] : continue
        if not item_id in item_db: continue

        # delta = item_db[item_id]-buy_summary[0]['pricePerUnit']

        delta = item_db[item_id]-item['buy_summary'][0]['pricePerUnit']

        if delta < 5 :continue
        a = item_plus_value = delta
        b = npc_price = item_db[item_id]
        c = item_name = item_id.capitalize()
        d = item_summary = item['buy_summary'][0]['pricePerUnit']
        qty = sum([x['amount'] for x in item['buy_summary'][:5]])#show summary

        item_to_buy.append({'delta':a,'npc_price':b,'name':c,'price':d,'qty':qty})

    filter_data = sorted(item_to_buy,key=lambda i:i['delta'],reverse=True)

    return filter_data[:5]

def press(event):
    if event.keysym == 'q':
        root.destroy()

def manage_lines():
    global lines
    for i in range(5):
        item = ttk.Labelframe(root,text=" this is item text name ",bootstyle="light",padding=10)
        item.pack(fill=X,padx=10,pady=(10,0))

        npc_price = ttk.Label(item, text="npc prix: 310022",bootstyle="light")
        npc_price.pack(side=LEFT)

        sell_price = ttk.Label(item, text="prix: 150041",bootstyle="light")
        sell_price.pack(side=LEFT,padx=10)

        delta = ttk.Label(item, text="delta: +2554",bootstyle="light")
        delta.pack(side=LEFT,padx=(0,10))

        qty = ttk.Label(item, text="qty: 25",bootstyle="light")
        qty.pack(side=LEFT)

        save = ttk.Button(item, text="save", bootstyle="success")
        save.pack(side=RIGHT)
        lines.append({'name':item,'npc':npc_price,
                      'sell_price':sell_price,'delta':delta,'qty':qty})    

def update(bypass=False):
    if not bypass:
        global count,lines;count-=1
        refresh.configure(text = f'refresh in {count:02d}s')
        refresh.after(1000, update)
    if not count or bypass: 
        count = 10+1
        print('destroy item')
        for i,element in enumerate(get_stock()):
            lines[i]['name'].configure(text=element['name'])
            lines[i]['npc'].configure(text=f"Prix npc: {element['npc_price']:,.2f}")
            lines[i]['sell_price'].configure(text=f"Prix d'achat: {element['price']:,.2f}")
            lines[i]['delta'].configure(text=f"Delta: {element['delta']:,.2f}")
            lines[i]['qty'].configure(text=f"Qty: {element['qty']}")
        # item_to_buy.append({'delta':a,'npc_price':b,'name':c,'summary':d})

# notebook.add(windows_tab, text='windows')
root = ttk.Window(themename="superhero")
root.geometry('600x500')
root.title('Minecraft stock market tracker')
root.bind('<Key>',press)
lines = [];count=2

frame = ttk.Frame(root,padding=10)
frame.pack(fill=X,pady=(5,10))
title = ttk.Label(frame, text="Minecraft stock market",font="Arial 20")
title.pack(side=LEFT)

refresh = ttk.Button(frame, text="refresh in 10s", bootstyle="info", command=lambda:update(1))
refresh.pack(side=RIGHT)

update()
manage_lines()

# titre.configure(text="qty: 265")

root.mainloop()