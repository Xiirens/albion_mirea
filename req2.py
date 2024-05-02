import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import re
import cv2
import math

from concurrent.futures import ThreadPoolExecutor




async def load_json(url):
    """
    Загружает JSON данные по указанному URL.

    :param url: URL для загрузки JSON.
    :return: Загруженные данные в формате словаря.
    """
    async with aiohttp.ClientSession() as session:
        
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                return data
            else:
                print(response.status)
                print('перевес')
                

async def main(urls):
    """
    Генерирует асинхронные JSON запросы по списку URL.

    :param urls: Список URL для выполнения запросов.
    """
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(load_json(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
    

url = 'https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json' # заменить на нужную ссылку


async def main_1():
    """
    Создает словарь и ссылки для запросов к Git и AlbionDataProject.
    """
    start_time = datetime.now()
    response_text = await load_json(url)
    data = response_text
    city_2 = 'BlackMarket'
    city_l = 'Lymhurst'
    city_b = 'Bridgewatch'
    city_f = 'Fort Sterling'
    city_m = 'Martlock'
    city_t = 'Thetford'
    city_c = 'Caerleon'

    
    step = 175
    trans = {} # транскрипция на рф
    urls = [] # все ссылки
    item_to = [] # вещи через запятую
    item_ready = [] # разбитые по 300 элементов
    
    for item in data:
        if item.get('LocalizedNames') and 'RU-RU' in item['LocalizedNames']:
            word = item['LocalizedNames']['RU-RU']
            unique_name = item['UniqueName']
            name = word.replace(word[word.find("("):word.find(")")+1], "")
            trans[unique_name] = name
            
            if ('T4_ARMOR' in unique_name) or ('T4_HEAD' in unique_name) or ('T4_SHOES' in unique_name) or ('T4_MAIN' in unique_name) or ('T4_OFF' in unique_name) or ('T4_2H' in unique_name):
                item_to.append(unique_name)
            if ('T5_ARMOR' in unique_name) or ('T5_HEAD' in unique_name) or ('T5_SHOES' in unique_name) or ('T5_MAIN' in unique_name) or ('T5_OFF' in unique_name) or ('T5_2H' in unique_name):
                item_to.append(unique_name)
            if ('T6_ARMOR' in unique_name) or ('T6_HEAD' in unique_name) or ('T6_SHOES' in unique_name) or ('T6_MAIN' in unique_name) or ('T6_OFF' in unique_name) or ('T6_2H' in unique_name):
                item_to.append(unique_name)
            if ('T7_ARMOR' in unique_name) or ('T7_HEAD' in unique_name) or ('T7_SHOES' in unique_name) or ('T7_MAIN' in unique_name) or ('T7_OFF' in unique_name) or ('T7_2H' in unique_name):
                item_to.append(unique_name)
            if ('T8_ARMOR' in unique_name) or ('T8_HEAD' in unique_name) or ('T8_SHOES' in unique_name) or ('T8_MAIN' in unique_name) or ('T8_OFF' in unique_name) or ('T8_2H' in unique_name):
                item_to.append(unique_name)

    for i in range(0, len(item_to), step):
        item_ready.append(item_to[i:i+step])
    
    for i in item_ready:
        s = ','.join(str(x) for x in i)
        ur =  'https://west.albion-online-data.com/api/v2/stats/prices/' + s + "?locations=" + city_l +  "," + city_b +  "," + city_f +  "," + city_m +  "," + city_t +  "," + city_c + "," + city_2 + "&qualities=0"
        urls.append(ur)
    print('колическо завпросов верх', len(urls)) 
    
    
    r = await main(urls)
    
    data = [] # словарь для всего json
    
    
    
    
    for d in r:
        data.extend(d)

     
        

    
    data_sorted = sorted(data, key=lambda x: (x["item_id"], x["quality"]))

    await asyncio.gather(
        #start_table(data_sorted, trans),
        start(data_sorted, trans)
    )
    print("--- %s seconds ---" % (datetime.now() - start_time))

async def start_table(data_sorted, trans):
    """
    Генерирует таблицы предметов на основе отсортированных данных.

    :param data_sorted: Отсортированные данные.
    :param trans: Параметры транзакций.
    """
    T4_Armor = []
    T4_Piy = []
    T5_Armor = []
    T5_Piy = []
    T6_Armor = []
    T6_Piy = []
    T7_Armor = []
    T7_Piy = []
    T8_Armor = []
    T8_Piy = []
    
    T4_Armor_s = []
    T4_Piy_s = []
    T5_Armor_s = []
    T5_Piy_s = []
    T6_Armor_s = []
    T6_Piy_s = []
    T7_Armor_s = []
    T7_Piy_s = []
    T8_Armor_s = []
    T8_Piy_s = []
    
    for i in range(len(data_sorted)):
        string = data_sorted[i]['item_id']
        armor = '_'.join(string.split('_')[:2])
        
        if armor == 'T7_ARMOR' or armor == 'T7_HEAD' or armor == 'T7_SHOES':
            T7_Armor.append(data_sorted[i])
            T7_Armor_s.append(data_sorted[i]['item_id'])
        elif armor == 'T7_2H' or armor == 'T7_MAIN' or armor == 'T7_OFF':
            T7_Piy.append(data_sorted[i])
            T7_Piy_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T8_ARMOR' or armor == 'T8_HEAD' or armor == 'T8_SHOES':
            T8_Armor.append(data_sorted[i])
            T8_Armor_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T8_2H' or armor == 'T8_MAIN' or armor == 'T8_OFF':
            T8_Piy.append(data_sorted[i])
            T8_Piy_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T6_ARMOR' or armor == 'T6_HEAD' or armor == 'T6_SHOES':
            T6_Armor.append(data_sorted[i])
            T6_Armor_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T6_2H' or armor == 'T6_MAIN' or armor == 'T6_OFF':
            T6_Piy.append(data_sorted[i])
            T6_Piy_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T5_ARMOR' or armor == 'T5_HEAD' or armor == 'T5_SHOES':
            T5_Armor.append(data_sorted[i])
            T5_Armor_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T5_2H' or armor == 'T5_MAIN' or armor == 'T5_OFF':
            T5_Piy.append(data_sorted[i])
            T5_Piy_s.append(data_sorted[i]['item_id'])
            
        elif armor == 'T4_ARMOR' or armor == 'T4_HEAD' or armor == 'T4_SHOES':
            T4_Armor_s.append(data_sorted[i]['item_id'])
            T4_Armor.append(data_sorted[i])
            
        elif armor == 'T4_2H' or armor == 'T4_MAIN' or armor == 'T4_OFF':
            T4_Piy.append(data_sorted[i])
            T4_Piy_s.append(data_sorted[i]['item_id'])
    go = [4,5,6,7,8]        
    for i in go:
        if i == 4:
            name_img = 'T4'
            await logic_table(T4_Armor_s, T4_Armor, trans, name_img)
        if i == 5:
            name_img = 'T5'
            await logic_table(T5_Armor_s, T5_Armor, trans, name_img)
        if i == 6:
            name_img = 'T6'
            await logic_table(T6_Armor_s, T6_Armor, trans, name_img)
        if i == 7:
            name_img = 'T7'
            await logic_table(T7_Armor_s, T7_Armor, trans, name_img)
        if i == 8:
            name_img = 'T8'
            await logic_table(T8_Armor_s, T8_Armor, trans, name_img)
            
            
    
    


    
async def start(data_sorted, trans):
    """
    Запускает сортировку и выбор необходимых параметров.

    :param data_sorted: Отсортированные данные.
    :param trans: Параметры транзакций.
    """
    Black = 'Black Market'
    time_update = 1440
    min_profit = 10
    money_profit = 20000
    
    Sity = ['Lymhurst', 'Bridgewatch', 'Fort Sterling', 'Martlock', 'Thetford', 'Caerleon']
    Sity = ['Bridgewatch']

    for i in Sity:
        await topografia(data_sorted, i, Black, time_update, min_profit, money_profit, trans)


async def topografia(data, city_11, city_22, time_update, min_profit, money_profit, trans):
    """
    Сортирует полученные предметы и генерирует таблицы.

    :param data: Данные для сортировки.
    :param city_11: Город 1.
    :param city_22: Город 2.
    :param time_update: Время обновления.
    :param min_profit: Минимальная прибыль.
    :param money_profit: Прибыль в валюте.
    :param trans: Параметры транзакций.
    """
    for_data = []
    l = 0
    b = 0
    mess = ''
    message = ''
    buy_price_item = 0
    sell_price_item = 0
    all_profit_item = 0
    # Ищем нужные пары строк
    
    data_dict = {}
    for elem in data:
        key = (elem["city"], elem["item_id"])
        if key not in data_dict:
            data_dict[key] = []
        data_dict[key].append(elem)

    # Сравниваем элементы списка, соответствующие данным ключам и значениям групп
    for key in trans:
        item_id = str(key)
        for elem1 in data_dict.get((city_11, item_id), []):
            for elem2 in data_dict.get((city_22, item_id), []):
                if elem1 != elem2:
                    if elem1['quality'] >= elem2['quality']:
                        price_1 = elem1['sell_price_min']
                        price_2 = elem2["buy_price_max"]
                        price_22 = elem2["sell_price_min"]
                        if (price_1 > 0) and (price_2 > 0):
                            max_profit = price_2 - price_1
                            profit = int(((price_2-price_1)/price_1)*100)
                        else:
                            profit = 0
                        
                        date_1_in_str = elem1["sell_price_min_date"]
                        date_1_in_date = datetime.strptime(date_1_in_str, '%Y-%m-%dT%H:%M:%S')
                        date_2_in_str = elem2["buy_price_max_date"]
                        date_2_in_date = datetime.strptime(date_2_in_str, '%Y-%m-%dT%H:%M:%S')

                        now = datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')
                        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
                        raz = timedelta(hours=3) # то на сколько изменится время
                        max_time = timedelta(minutes=time_update) # максимальная разница (не больше N минут)


                        msk_1 = date_1_in_date + raz #время с изменением UTC
                        msk_2 = date_2_in_date + raz


                        duration_1 = now - msk_1  #продолжительность 
                        duration_2 = now - msk_2

                        if (duration_1 < max_time) and (duration_2 < max_time) and (profit > min_profit) and (money_profit < max_profit):

                            if duration_1 < duration_2:
                                time = duration_2
                            else:
                                time = duration_1
                            
                            dict_for = {'item_id': str(elem2["item_id"]), 'city_1': str(elem1["city"]), 'city_2': str(elem2["city"]), 'profit': profit, 'max_profit': max_profit, "time": time, 'quality_1': int(elem1["quality"]), 'quality_2': int(elem2["quality"]), 'price_1': price_1, 'price_2': price_2}   
                            for_data.append(dict_for)
                                
                            quality = elem1["quality"]
                            if quality == 1:
                                mex = 'Обычное'
                            if quality == 2:
                                mex = 'Хорошее'
                            if quality == 3:
                                mex = 'Выдающееся'
                            if quality == 4:
                                mex = 'Отличное'
                            if quality == 5:
                                mex = 'Шедевр'
                                
                                
                            item_id = str(elem1["item_id"])
                            
                            level = re.search(r"T(\d+)_", item_id).group(1)
                            
                            match = re.search(r"@\d+", item_id)
                            if match:
                                number_string = match.group(0)[1:]
                                number_match = re.search(r"\d+", number_string)
                                if number_match:
                                    number = number_match.group(0)
                                else:
                                    number = "0"
                            else:
                                number = "0"
                            
                            result = f"{level}.{number}"
                            
                            ct = str(elem1["city"])
                            ct_1 = str(elem2["city"])
                            
                            key = str(elem1["item_id"])
                            ru = trans[key]
                            
                            make = elem1["item_id"]
                            mak = ru
                            message = message + str(mak) + result + '\n' + 'Качество: ' + mex +'\n' + 'Цена в: ' + ct + ' ' + str(price_1) + '\n' + 'Цена в: ' + str(ct_1) + ' ' + str(price_2) + ' ' + str(price_22) + '\n' + 'Профит: ' + str(profit) + '%' + '\n' + 'Деньгами: ' + str(max_profit) + '\n' + 'Было обновлено: ' + str(time) + ' назад' + "\n\n"
                            buy_price_item = buy_price_item + price_1
                            sell_price_item = sell_price_item + price_2
                
    all_profit_item =  sell_price_item - buy_price_item
    message_retun = mess + message + '\n\n' + 'Покупка всего ' + str(buy_price_item) + '\n' + 'Продажа всего ' + str(sell_price_item) + '\n' + 'Весь профит ' + str(all_profit_item)     
    
    await logic(for_data, trans, city_11)    
            
    print(l)
    print(b)

async def request_to_albion(items):
    """
    Выполняет дополнительные запросы JSON только по полученным предметам.

    :param items: Список предметов для запросов.
    """
    now = datetime.now()
    days_ago = now - timedelta(days=30)
    formatted_now = now.strftime("%m-%d-%Y")
    formatted_days_ago = days_ago.strftime("%m-%d-%Y")
    items_r = [] # по 180
    step = 180
    url_diagram = []
    city_market = 'BlackMarket'

    for i in range(0, len(items), step):
        items_r.append(items[i:i+step])
    for i in items_r:
        s = ','.join(str(x) for x in i)
        ur =  'https://west.albion-online-data.com/api/v2/stats/charts/' + s + '?date=' + str(formatted_days_ago) + '&end_date=' + str(formatted_now) + "&locations=" + city_market + "&qualities=0&time-scale=24"
        url_diagram.append(ur)
    print('колическо завпросов низ', len(url_diagram))  

    r = await main(url_diagram)
    data = []
    for d in r:
        data.extend(d)
    print(len(items))
    print(len(data))
    return data





async def sort_data(data):
    """
    Сортирует данные.

    :param data: Данные для сортировки.
    """
    sorted_data = sorted(data)
    no_at_data = [item for item in sorted_data if '@' not in item]
    at_data = [item for item in sorted_data if '@' in item]
    sorted_at_data = sorted(at_data, key=lambda x: (x.split('@')[1], x.split('@')[0]))
    return no_at_data + sorted_at_data

async def logic_table(name, data, trans, name_img):
    """
    Создает таблицу данных.

    :param name: Имя таблицы.
    :param data: Данные для таблицы.
    :param trans: Параметры транзакций.
    :param name_img: Название изображения.
    """
    unique_items = list(set(name))
    exclude_words = {'GATHERER_FIBER', 'GATHERER_FISH', 'GATHERER_HIDE', 'GATHERER_ORE', 'GATHERER_ROCK', 'GATHERER_WOOD'}
    filtered_words = [word for word in unique_items if not any(exclude_word in word for exclude_word in exclude_words)]
    sort =  await sort_data(filtered_words)
    
    
    # загрузка изображения
    img = cv2.imread('table3.png')
    quality = 1
    # настройки шрифта и цвета
    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 1
    fontScale_city = 2
    color = (255, 255, 255) # white
    color_ru =(255, 255, 255)
    color_orange = (0, 155, 255) 
    color_lum = (0, 213, 255)
    color_profit= (255, 255, 255)
    color_profit_avg= (255, 255, 255)
    thickness = 2
    thickness_name = 2
    font_name = cv2.FONT_HERSHEY_COMPLEX
    
    x_item, y_item = 200, 800
    x_city, y_city = 1100, 640

    
    x_name_price_1, y_name_price_1 = 980, 720
    x_profit, y_profit = 1200, 800
    x_price_avg, y_price_avg = 1250, 800
    x_sell_avg, y_sell_avg = 1500, 800
    x_item_price_1, y_item_price_1 = 1000, 800

    
    x_line, y_line = 200, 750
    x_line_end, y_line_end = 5900, 750
    
    x_line_vertical, y_line_vertical = 950, 700
    x_line_vertical_end, y_line_vertical_end = 950, 70000
    
    
    
    
    
    
    
    data_avg = await request_to_albion(sort)
    

    
    
    
    
    
    

    
    
    t_time = datetime.now()
    
    for item in sort:
        Found = False
        color_ru =(255, 255, 255)
        if 'LEATHER' in item:
            color_ru =(245, 230, 66)
        elif 'CLOTH' in item:
            color_ru =(167, 255, 135)
        elif 'PLATE' in item:
            color_ru =(135, 155, 255)
        for item_avg in data_avg:
            if item_avg['item_id'] == item and item_avg['quality'] == quality:
                x_item_price_1 = 1000
                x_profit = 1200
                ru = trans[item]
                
                item_id = str(item)                
                level = re.search(r"T(\d+)_", item_id).group(1)
                match = re.search(r"@\d+", item_id)
                if match:
                    number_string = match.group(0)[1:]
                    number_match = re.search(r"\d+", number_string)
                    if number_match:
                        number = number_match.group(0)
                    else:
                        number = "0"
                else:
                    number = "0"
                result = f"{level}.{number}"
                
                org_item = (x_item, y_item)
                cv2.putText(img, str(ru + '' + result), org_item, font, fontScale, color_ru, thickness)
                
                
                
                item_count = item_avg['data']['item_count']
                l = 0
                for b in item_count:
                    l = l + b
                l = l / len(item_count)
                l = math.ceil(l)

                avg = item_avg['data']['prices_avg']
                price_avg = 0
                for u in avg:
                    price_avg = price_avg + u
                price_avg = price_avg / len(avg)
                price_avg = math.ceil(price_avg)
                
                
                Found = True
                # находим все записи с заданным item_id
                records = [record for record in data if record['item_id'] == item and record['quality'] == quality]
                # проходим по каждому городу и выводим цену
                for city in ['Black Market', 'Lymhurst', 'Bridgewatch', 'Fort Sterling', 'Martlock', 'Thetford', 'Caerleon']:
                    # находим запись с заданным городом
                    record = next((r for r in records if r['city'] == city and r['quality'] == quality), None)

                        
                    price_1 = record["sell_price_min"]
                    
                    
                    if city == 'Black Market':
                        price_black = record['buy_price_max']
                    
                    if (price_1 > 0) and (price_black > 0):
                        max_profit = price_black - price_1
                        profit = int(((price_black-price_1)/price_1)*100)
                        if profit >= 30:
                            color_profit = (0, 155, 0)
                        elif profit < 0:
                            color_profit = (25, 0, 255)
                        elif profit > 0 and profit < 30:
                            color_profit = (255, 153, 0)
                    else:
                        profit = 0
                        color_profit = (255, 255, 255)
                        
                    if (price_1 > 0) and (price_avg > 0):
                        max_profit = price_avg - price_1
                        profit_avg = int(((price_avg-price_1)/price_1)*100)
                        if profit_avg >= 30:
                            color_profit_avg = (0, 155, 0)
                        elif profit_avg < 0:
                            color_profit_avg = (25, 0, 255)
                        elif profit_avg > 0 and profit_avg < 30:
                            color_profit_avg = (255, 153, 0)
                        profit_avg = str(profit_avg) + '%'
                    else:
                        profit_avg = ''
                        color_profit_avg = (255, 255, 255)    
                        
                    
                    
                    org_item_price_1 = (x_item_price_1, y_item_price_1)
                    org_line_start = (x_line, y_line)
                    org_line_end = (x_line_end, y_line_end)
                    org_profit = (x_profit, y_profit)
                    
                    org_price_avg = (x_price_avg, y_price_avg)
                     
                    org_sell_avg = (x_sell_avg, y_sell_avg) 
                    if (price_1) > (price_avg*7):
                        price_1 = 'incorrect'
                    
                    if city == 'Black Market':
                        cv2.putText(img, str(price_black), org_item_price_1, font, fontScale, color_lum, thickness)
                        cv2.putText(img, str(price_avg), org_price_avg, font, fontScale, (135, 255, 217), thickness)
                        cv2.putText(img, str(l), org_sell_avg, font, fontScale, (255, 255, 255), thickness)
                        cv2.line(img, org_line_start, org_line_end, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
                        x_profit += 700
                        x_item_price_1 += 700
                    else:
                        cv2.putText(img, str(price_1), org_item_price_1, font, fontScale, color_orange, thickness)
                        cv2.putText(img, str(str(profit) + '%'), org_profit, font, fontScale, color_profit, thickness)
                        x_profit_avg = x_profit
                        y_profit_avg = y_profit
                        x_profit_avg = x_profit_avg + 100
                        org_profit_avg = (x_profit_avg, y_profit_avg) 
                        cv2.putText(img, str(profit_avg), org_profit_avg, font, fontScale, color_profit_avg, thickness)
                        cv2.line(img, org_line_start, org_line_end, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
                        x_profit += 500
                        x_item_price_1 += 500
                y_price_avg += 80
                y_sell_avg += 80
                y_profit += 80
                y_line += 80
                y_line_end += 80
                y_item_price_1 += 80
                y_item += 80
                
                break
        if not Found:
            x_item_price_1 = 1000
            x_profit = 1200
            ru = trans[item]
            
            item_id = str(item)                
            level = re.search(r"T(\d+)_", item_id).group(1)
            match = re.search(r"@\d+", item_id)
            if match:
                number_string = match.group(0)[1:]
                number_match = re.search(r"\d+", number_string)
                if number_match:
                    number = number_match.group(0)
                else:
                    number = "0"
            else:
                number = "0"
            result = f"{level}.{number}"
            
            org_item = (x_item, y_item)
            cv2.putText(img, str(ru + '' + result), org_item, font, fontScale, color_ru, thickness)
            
            
            
            l = '-'
            price_avg = '-'
            
            # находим все записи с заданным item_id
            records = [record for record in data if record['item_id'] == item and record['quality'] == quality]
            # проходим по каждому городу и выводим цену
            for city in ['Black Market', 'Lymhurst', 'Bridgewatch', 'Fort Sterling', 'Martlock', 'Thetford', 'Caerleon']:
                # находим запись с заданным городом
                record = next((r for r in records if r['city'] == city and r['quality'] == quality), None)

                    
                price_1 = record["sell_price_min"]
                
                
                if city == 'Black Market':
                    price_black = record['buy_price_max']
                
                if (price_1 > 0) and (price_black > 0):
                    max_profit = price_black - price_1
                    profit = int(((price_black-price_1)/price_1)*100)
                    if profit >= 30:
                        color_profit = (0, 155, 0)
                    elif profit < 0:
                        color_profit = (25, 0, 255)
                    elif profit > 0 and profit < 30:
                        color_profit = (255, 153, 0)
                else:
                    profit = 0
                    color_profit = (255, 255, 255)
                
                org_item_price_1 = (x_item_price_1, y_item_price_1)
                org_line_start = (x_line, y_line)
                org_line_end = (x_line_end, y_line_end)
                org_profit = (x_profit, y_profit)
                
                org_price_avg = (x_price_avg, y_price_avg)
                    
                org_sell_avg = (x_sell_avg, y_sell_avg) 
                
                
                if city == 'Black Market':
                    cv2.putText(img, str(price_black), org_item_price_1, font, fontScale, color_lum, thickness)
                    cv2.putText(img, str(price_avg), org_price_avg, font, fontScale, (135, 255, 217), thickness)
                    cv2.putText(img, str(l), org_sell_avg, font, fontScale, (255, 255, 255), thickness)
                    cv2.line(img, org_line_start, org_line_end, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
                    x_profit += 700
                    x_item_price_1 += 700
                else:
                    cv2.putText(img, str(price_1), org_item_price_1, font, fontScale, color_orange, thickness)
                    cv2.putText(img, str(str(profit) + '%'), org_profit, font, fontScale, color_profit, thickness)
                    cv2.line(img, org_line_start, org_line_end, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
                    x_profit += 500
                    x_item_price_1 += 500
            y_price_avg += 80
            y_sell_avg += 80
            y_profit += 80
            y_line += 80
            y_line_end += 80
            y_item_price_1 += 80
            y_item += 80
            
            
    
    

    
    org_name_price_1 = (x_name_price_1, y_name_price_1)
    for i in range(0, 7):
        if i == 0:

            cv2.line(img, (x_line_vertical + i * 0, y_line_vertical), (x_line_vertical_end + i * 0, y_line_vertical_end), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str('Продажа'), (x_name_price_1 + i * 0, y_name_price_1), font, fontScale, color, thickness)
            cv2.putText(img, str('ЦенаAVG'), (x_name_price_1 + 230, y_name_price_1), font, fontScale, (135, 255, 217), thickness)
            cv2.putText(img, str('За месяц'), (x_name_price_1 + 450, y_name_price_1), font, fontScale, color, thickness)
        elif i == 1:

            cv2.line(img, (x_line_vertical + i * 700, y_line_vertical), (x_line_vertical_end + i * 700, y_line_vertical_end), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str('Покупка'), (x_name_price_1 + i * 700, y_name_price_1), font, fontScale, (255, 255, 255), thickness)

            # Раскраска слова "Prof" зеленым цветом
            cv2.putText(img, str('Profit'), (x_name_price_1 + i * 700 + len('Покупка') * 20 + 55, y_name_price_1), font, fontScale, (0, 213, 255), thickness)

            # Раскраска слова "ProfAVG" синим цветом
            cv2.putText(img, str('ProfitAVG'), (x_name_price_1 + i * 700 + len('ПокупкаProfit') * 20 + 40, y_name_price_1), font, fontScale, (135, 255, 217), thickness)
            
        else:
            cv2.line(img, (x_line_vertical + i * 500 + 200, y_line_vertical), (x_line_vertical_end + i * 500 + 200, y_line_vertical_end), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
           
            
            cv2.putText(img, str('Покупка'), (x_name_price_1 + i * 500 + 200, y_name_price_1), font, fontScale, (255, 255, 255), thickness)

            # Раскраска слова "Prof" зеленым цветом
            cv2.putText(img, str('Profit'), (x_name_price_1 + i * 500 + 200 + len('Покупка') * 20 + 55, y_name_price_1), font, fontScale, (0, 213, 255), thickness)

            # Раскраска слова "ProfAVG" синим цветом
            cv2.putText(img, str('ProfitAVG'), (x_name_price_1 + i * 500 + 200 + len('ПокупкаProfit') * 20 + 40, y_name_price_1), font, fontScale, (135, 255, 217), thickness)

        
            
    city_s = ['Black Market', 'Lymhurst', 'Bridgewatch', 'Fort Sterling', 'Martlock', 'Thetford', 'Caerleon']
    for i in range(len(city_s)):
        if i == 0: #black
            cv2.putText(img, str(city_s[0]), (x_city + i * 0, y_city), font, fontScale_city, color, thickness)
        elif i == 1: # lum
            cv2.putText(img, str(city_s[i]), (x_city + i * 650, y_city), font, fontScale_city, color, thickness)
            
        elif i == 2: # brig
            cv2.putText(img, str(city_s[i]), (x_city + i * 500 + 100, y_city), font, fontScale_city, color, thickness)
        elif i == 3: # fort
            cv2.putText(img, str(city_s[i]), (x_city + i * 500 + 80, y_city), font, fontScale_city, color, thickness)
        elif i == 4: # mart
            cv2.putText(img, str(city_s[i]), (x_city + i * 500 + 150, y_city), font, fontScale_city, color, thickness)
        elif i == 5: # tet
            cv2.putText(img, str(city_s[i]), (x_city + i * 500 + 150, y_city), font, fontScale_city, color, thickness)
        elif i == 6: # carl
            cv2.putText(img, str(city_s[i]), (x_city + i * 500 + 150, y_city), font, fontScale_city, color, thickness)

    
    

    
    
    
    
    new_height = y_item + 200
    img_cropped = img[:new_height, :]
    cv2.imwrite(str(name_img) + '.jpg', img_cropped)
    print('comlite_table' + str(name_img))
    print("--- %s seconds ---" % (datetime.now() - t_time))
            
            
            
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
       
async def logic(for_data, trans, city_1):
    """
    Создает вторую таблицу данных.

    :param for_data: Данные для таблицы.
    :param trans: Параметры транзакций.
    :param city_1: Город 1.
    """
    sorted_list = sorted(for_data, key=lambda x: (-x['time'], -x['max_profit']), reverse=True) # по времени
    #sorted_list = sorted(for_data, key=lambda x: x['max_profit'], reverse=True) # по количеству мани

    # for i in range(len(sorted_list)):
    #     print(sorted_list[i]['item_id'])
    #     print(sorted_list[i]['city_1'])
    #     print(sorted_list[i]['city_2'])
    #     print(sorted_list[i]['max_profit'])
    #     print(sorted_list[i]['profit'])
    #     print('')
    #     print('')

    # загрузка изображения
    img = cv2.imread('table3.png')

    # настройки шрифта и цвета
    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2
    thickness_name = 2
    font_name = cv2.FONT_HERSHEY_COMPLEX

    color_money_profit = (255, 255, 255) 
    color_profit_avg = (255, 255, 255)
    color_profit = (255, 255, 255)
    
    color_city = (69, 246, 255)
    color_city_avg = (190, 255, 176)
    color_black = (3, 154, 255)
    # начальные координаты для первой строки
    city_img_x, city_img_y = 1100, 700
    
    x, y = 200, 800
    x_text, y_text = 900, 700
    
    # добавление каждой строки текста из массива на изображение
    
    x_line_vertical, y_line_vertical = 850, 700
    x_line_vertical_end, y_line_vertical_end = 850, 70000
    
    x_n, y_n = x + 2900, 800
    x_text_n, y_text_n = x + 2900 + 700, 700

    x_line_vertical_n, y_line_vertical_n = x + 2900 + 650, 700
    x_line_vertical_end_n, y_line_vertical_end_n = x + 2900 + 650, 70000
    
    x_line, y_line = x, 750
    x_line_end, y_line_end = x + 2400 + 150, 750
    
    x_line_n, y_line_n = x_n, 750
    x_line_end_n, y_line_end_n = x_n + 1900 + 150, 750
    
    
    items = []
    for item in sorted_list:
        name = item['item_id']
        items.append(name)

    data = await request_to_albion(items)
    
    
    for i in range(len(sorted_list)):
        Found = False
        for item in data:
            if item['item_id'] == sorted_list[i]['item_id'] and item['quality'] == sorted_list[i]['quality_2']:
                item_count = item['data']['item_count']
                l = 0
                for b in item_count:
                    l = l + b
                l = l / len(item_count)
                l = math.ceil(l)

                avg = item['data']['prices_avg']
                price_avg = 0
                for u in avg:
                    price_avg = price_avg + u
                price_avg = price_avg / len(avg)
                price_avg = math.ceil(price_avg)
                Found = True
                org = (x, y)
                
                price_1 = sorted_list[i]['price_1'] # прайс в 1-м
                price_2 = sorted_list[i]['price_2'] # прайс в black
                text_max_profit = sorted_list[i]['max_profit'] # в серебре
                text_profit = sorted_list[i]['profit'] # в %
                text_time = sorted_list[i]['time'] # время
                quality_1 = sorted_list[i]['quality_1'] # качество 
                
                if quality_1 == 1:
                    quality_1 = 'Обычное'
                elif quality_1 == 2:
                    quality_1 = 'Хорошее'
                elif quality_1 == 3:
                    quality_1 = 'Выдающ'
                elif quality_1 == 4:
                    quality_1 = 'Отлично'
                elif quality_1 == 5:
                    quality_1 = 'Шедевр'
                quality_2 = sorted_list[i]['quality_2'] # качество Black
                if quality_2 == 1:
                    quality_2 = 'Обычное'
                elif quality_2 == 2:
                    quality_2 = 'Хорошее'
                elif quality_2 == 3:
                    quality_2 = 'Выдающ'
                elif quality_2 == 4:
                    quality_2 = 'Отлично'
                elif quality_2 == 5:
                    quality_2 = 'Шедевр'
                
                
                if (price_1 > 0) and (price_avg > 0):
                        max_profit = price_avg - price_1
                        profit_avg = int(((price_avg-price_1)/price_1)*100)
                        if profit_avg >= 30:
                            color_profit_avg = (0, 155, 0)
                        elif profit_avg < 0:
                            color_profit_avg = (25, 0, 255)
                        elif profit_avg > 0 and profit_avg < 30:
                            color_profit_avg = (255, 153, 0)
                        profit_avg = str(profit_avg) + '%'
                else:
                    profit_avg = ''
                    color_profit_avg = (255, 255, 255)  
                
                if text_profit >= 30:
                    color_profit = (0, 155, 0)
                elif text_profit > 0 and text_profit < 30:
                    color_profit = (255, 153, 0)
                else:
                    text_profit = ''
                    color_profit = (255, 255, 255)  
                
                
                org_line_start = (x_line, y_line)
                org_line_end = (x_line_end, y_line_end)
                
                text = sorted_list[i]['item_id']
                ru = trans[text]
                
                item_id = sorted_list[i]['item_id']             
                level = re.search(r"T(\d+)_", item_id).group(1)
                match = re.search(r"@\d+", item_id)
                if match:
                    number_string = match.group(0)[1:]
                    number_match = re.search(r"\d+", number_string)
                    if number_match:
                        number = number_match.group(0)
                    else:
                        number = "0"
                else:
                    number = "0"
                
                result = f"{level}.{number}"
                if text_max_profit >= 60000:
                    color_money_profit = (119, 245, 10) 
                elif text_max_profit >= 20000 and text_max_profit <= 60000:
                    color_money_profit = (217, 245, 10)
                else:
                    color_money_profit = (255, 255, 255) 
                    
                if (price_1) > (price_avg*7):
                        price_1 = 'incorrect'
                cv2.line(img, org_line_start, org_line_end, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
                cv2.putText(img, ru + '' + result, (x, y), font_name, fontScale, color, thickness_name)
                cv2.putText(img, str(price_1), (x + 700, y), font, fontScale, color_city, thickness)
                cv2.putText(img, str(price_2), (x + 900, y), font, fontScale, color_black, thickness)
                cv2.putText(img, str(price_avg), (x + 1100, y), font, fontScale, color_city_avg, thickness)
                cv2.putText(img, str(quality_1), (x + 1300, y), font, fontScale, color, thickness)
                cv2.putText(img, str(quality_2), (x + 1500, y), font, fontScale, color, thickness)
                
                cv2.putText(img, str(text_max_profit), (x + 1700, y), font, fontScale, color_money_profit, thickness) # сера
                cv2.putText(img, str(str(text_profit) + '%'), (x + 1900, y), font, fontScale, color_profit, thickness) # в %
                cv2.putText(img, str(str(profit_avg) + '%'), (x + 2000, y), font, fontScale, color_profit_avg, thickness) # В % на avg
                cv2.putText(img, str(str(l) + '/day'), (x + 2200, y), font, fontScale, color, thickness) # за день
                
                cv2.putText(img, str(text_time), (x + 2400, y), font, fontScale, color, thickness)
                y += 80  # увеличение координаты y для следующей строки
                y_line += 80
                y_line_end += 80
                break
        if not Found:

            org = (x_n, y_n)


            item_id = sorted_list[i]['item_id']          
            level = re.search(r"T(\d+)_", item_id).group(1)
            match = re.search(r"@\d+", item_id)
            if match:
                number_string = match.group(0)[1:]
                number_match = re.search(r"\d+", number_string)
                if number_match:
                    number = number_match.group(0)
                else:
                    number = "0"
            else:
                number = "0"
            
            result_n = f"{level}.{number}"
            
            quality_1_n = sorted_list[i]['quality_1'] # качество 
            if quality_1_n == 1:
                quality_1_n = 'Обычное'
            elif quality_1_n == 2:
                quality_1_n = 'Хорошее'
            elif quality_1_n == 3:
                quality_1_n = 'Выдающ'
            elif quality_1_n == 4:
                quality_1_n = 'Отлично'
            elif quality_1_n == 5:
                quality_1_n = 'Шедевр'
            quality_2_n = sorted_list[i]['quality_2'] # качество Black
            if quality_2_n == 1:
                quality_2_n = 'Обычное'
            elif quality_2_n == 2:
                quality_2_n = 'Хорошее'
            elif quality_2_n == 3:
                quality_2_n = 'Выдающ'
            elif quality_2_n == 4:
                quality_2_n = 'Отлично'
            elif quality_2_n == 5:
                quality_2_n = 'Шедевр'
            
            text_1 = sorted_list[i]['price_1']
            text_2 = sorted_list[i]['price_2']
            text_max_profit_n = sorted_list[i]['max_profit']
            text_profit_n = sorted_list[i]['profit']
            text_time_n = sorted_list[i]['time']
            text_none = 'Для этого столбца нету данных о средней цене'
            text_n = sorted_list[i]['item_id']
            ru_n = trans[text_n]
            
            if text_profit_n >= 30:
                color_profit_n = (0, 155, 0)
            elif text_profit_n > 0 and text_profit_n < 30:
                color_profit_n = (255, 153, 0)
            else:
                text_profit_n = ''
                color_profit_n = (255, 255, 255)  
            
            
            if text_max_profit_n >= 60000:
                color_money_profit_n = (119, 245, 10) 
            elif text_max_profit_n >= 20000 and text_max_profit_n <= 60000:
                color_money_profit_n = (217, 245, 10)
            else:
                color_money_profit_n = (255, 255, 255) 
            
            org_line_start_n = (x_line_n, y_line_n)
            org_line_end_n = (x_line_end_n, y_line_end_n)
            
            cv2.line(img, org_line_start_n, org_line_end_n, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            cv2.putText(img, ru_n + '' + result_n, (x_n, y_n), font_name, fontScale, color, thickness_name)
            cv2.putText(img, str(text_1), (x_n + 700, y_n), font, fontScale, color_city, thickness)
            cv2.putText(img, str(text_2), (x_n + 900, y_n), font, fontScale, color_black, thickness)
            cv2.putText(img, str(quality_1_n), (x_n + 1100, y_n), font, fontScale, color, thickness)
            cv2.putText(img, str(quality_2_n), (x_n + 1300, y_n), font, fontScale, color, thickness)
            cv2.putText(img, str(text_max_profit_n), (x_n + 1500, y_n), font, fontScale, color_money_profit_n, thickness) # сера
            cv2.putText(img, str(str(text_profit_n) + '%'), (x_n + 1700, y_n), font, fontScale, color_profit_n, thickness) # в %
            cv2.putText(img, str(text_time_n), (x_n + 1900, y_n), font, fontScale, color, thickness)
            
            y_line_n += 80
            y_line_end_n += 80
            y_n += 80  # увеличение координаты y для следующей строки
        
    
    for i in range(0, 2):
        if i == 0:

            cv2.line(img, (x_line_vertical + i * 0, y_line_vertical), (x_line_vertical_end + i * 0, y-40), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str(city_1), (x_text + i * 0 - 20, y_text), font, fontScale, color, thickness)
            cv2.putText(img, str('Black'), (x_text + 210, y_text), font, fontScale, (135, 255, 217), thickness)
            cv2.putText(img, str('BlackAVG'), (x_text + 400, y_text), font, fontScale, color, thickness)
            
            cv2.line(img, (x_line_vertical + 630, y_line_vertical), (x_line_vertical_end + 630, y-40), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str('Покупка'), (x_text + 600, y_text), font, fontScale, color, thickness)
            cv2.putText(img, str('Продажа'), (x_text + 800, y_text), font, fontScale, color, thickness)
            
            cv2.line(img, (x_line_vertical + 1020, y_line_vertical), (x_line_vertical_end + 1020, y-40), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str('Деньги'), (x_text + 1000, y_text), font, fontScale, color, thickness)
            cv2.putText(img, str('Prof'), (x_text + 1200, y_text), font, fontScale, color, thickness)
            cv2.putText(img, str('ProfAVG'), (x_text + 1300, y_text), font, fontScale, color, thickness)
            cv2.putText(img, str('PerDAY'), (x_text + 1500, y_text), font, fontScale, color, thickness)
            cv2.putText(img, str('UPDATE'), (x_text + 1700, y_text), font, fontScale, color, thickness)
        if i == 1:
            
            cv2.line(img, (x_line_vertical_n + i * 0, y_line_vertical_n), (x_line_vertical_end_n + i * 0, y_n-40), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str(city_1), (x_text_n + i * 0 - 20, y_text_n), font, fontScale, color, thickness)
            cv2.putText(img, str('Black'), (x_text_n + 210, y_text_n), font, fontScale, (135, 255, 217), thickness)
            
            cv2.line(img, (x_line_vertical_n + 430, y_line_vertical_n), (x_line_vertical_end_n + 430, y_n-40), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str('Покупка'), (x_text_n + 400, y_text_n), font, fontScale, color, thickness)
            cv2.putText(img, str('Продажа'), (x_text_n + 600, y_text_n), font, fontScale, color, thickness)
            
            cv2.line(img, (x_line_vertical_n + 820, y_line_vertical_n), (x_line_vertical_end_n + 820, y_n-40), (255, 255, 255), thickness=1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.putText(img, str('Деньги'), (x_text_n + 800, y_text_n), font, fontScale, color, thickness)
            cv2.putText(img, str('Prof'), (x_text_n + 1000, y_text_n), font, fontScale, color, thickness)
            cv2.putText(img, str('UPDATE'), (x_text_n + 1200, y_text_n), font, fontScale, color, thickness)


               
    if y_n < y:
        new_height = y + 300
    else:
        new_height = y_n +300
        
    new_weight = x_n + 1900 + 400
    org_city_img = (city_img_x, city_img_y)
    #cv2.putText(img, str(city_1), org_city_img, font, fontScale, color, thickness)
            # сохранение изображения с текстом
            

    img_cropped = img[:new_height, :new_weight]
    cv2.imwrite(str(city_1) + '.jpg', img_cropped)
    print('comlite')
 


        







    
    
starte = datetime.now()


asyncio.run(main_1())

end = datetime.now() - starte
print(end)
