
#################################### ライブラリ ####################################
import asyncio 
import aiohttp
import category

#################################### 入力 ####################################
# ブックマークの情報
book_mark_info_list =[]


#################################### 出力 ####################################


async def main(): 
    async with aiohttp.ClientSession() as session:
        id_txt_category_list = await asyncio.gather(*[[x['id'],category.scraping_meta(x['url'], "description_and_keyword", session), ''] for x in book_mark_info_list])
        print('test \n')
        print(id_txt_category_list)
    

if __name__ == "__main__":
  asyncio.run(main())