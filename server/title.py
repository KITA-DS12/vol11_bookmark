
#################################### ライブラリ ####################################
import asyncio 
import aiohttp
import category
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


#################################### 入力 ####################################
test_bookmark = [
  {
    "type": "url", 
    "id": 4, 
    "index": 0, 
    "title": "現役警察官“大胆な撮影”が大反響　「旅の恥はかき捨て…ではない！」(2023年2月16日) - YouTube", 
    "date_added": 1677140484, 
    "url": "https://www.youtube.com/watch?v=PK2oNiWdII8", 
    "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=", 
    "iconuri": None, 
    "tags": None},
   {
     "type": "url", 
     "id": 5, 
     "index": 1, 
     "title": "【しらべてみたら】ゴミ袋に名前＆バス停には並ばない ローカルルール - YouTube", 
     "date_added": 1677140505, 
     "url": "https://www.youtube.com/watch?v=VNoISTch4OM", 
     "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=", 
     "iconuri": None, 
     "tags": None},
   {
     "type": "url", 
     "id": 6, 
     "index": 2, 
     "title": "「勝手踏切」って何? 線路の目の前に玄関! 危険な実態を調査【しらべてみたら】 - YouTube", 
     "date_added": 1677140511, 
     "url": "https://www.youtube.com/watch?v=3AIcY_X6jzI", "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=", 
     "iconuri": None, 
     "tags": None
     },
   {
     "type": "url", 
     "id": 7, 
     "index": 3, 
     "title": "除雪後の「雪」　深刻な「その後」　北海道ならでは“処理方法”…“マンゴー栽培”も【Jの追跡】(2023年2月19日) - YouTube", 
     "date_added": 1677140526, 
     "url": "https://www.youtube.com/watch?v=gyPy6nH1RyE", "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=", 
     "iconuri": None, 
     "tags": None}, 
   {
     "type": "url", 
     "id": 8, 
     "index": 4, 
     "title": "ニコニコ", 
     "date_added": 1677140553, 
     "url": "https://www.nicovideo.jp/", 
     "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABiElEQVQ4jaVSMW4UQRCs6h4sJExw0n2AnduNiBw4d05AZt0T+IHhAcYPsETqyHyAT0BAYocn+QOWLgEJAdNFsDPc3iLZASWNpqenuma6ZoAZ+r6/6rpuXZdeB7quW+ecr+Z8A8BpQtJ9Suk653wKoAAoOefTlNI1yftZPVsxATyp8c/VavXezM5KKWsAcPePEXGx2WzeAjiovF8AxJzza3d/FxGHAETSAPwA8BJAquTfAG4BPJUUAGhm30op5+z7/rOZHUcEyF03da3aFs1s2ibMDBHxJUlSRBSN2LEASvpbExGa7EVEUJLS6ARdUhlD7pk6Faynq/JcEmxS8FDxTmXksMX2CP9R/L+Adk7pQeY+2uso1bnpiCQnontoe5KamUoYf5ZIRrtVPWEu0gyOyiWAg0TyxsyO2h+IiCBpZoZ2EZKICEgKM3MAXnM3XC6XzxeLxStJzwAcufubUsqdpAuSpfbqJM/c/UUp5QOAryS/b7fbT//0OQzDZc75ZJ7POZ8Mw3A5z/8BfBrE1Q4ZtvMAAAAASUVORK5CYII=", 
     "iconuri": None, 
     "tags": None}, 
   {
     "type": "url", 
     "id": 9, 
     "index": 5, 
     "title": "とける魔法 - ニコニコ動画", 
     "date_added": 1677140658, 
     "url": "https://www.nicovideo.jp/watch/sm41821294", "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC6UlEQVQ4jW2STWicVRSG33vPvffLmMwk08w4/SZNm8xMZvyJjSGIC0uTnQRBaHWwu4IgoutScVH5wFUXLkoFd5ZSRLIQVwE3BV0UgiASEgyI2E7rNrGE0O/n/hwXMy0YeuFwuZf3vPA+5wDHTrtR/6BarU6OnnJUmK3VmvMn6+8f10sAot/v09ramkqSRApFJ6ZfMD+ebbdfBBAAhO6pUzPGyA0SqtTv92llZUX3AQIgjhsCACLgnbg88QOAGECrOVW+Ow68/TytOF0tn5udn7vYiGdUkWUloQjtVvfv3Z3tyxyC0kZTmqaHjZPxhiuKOLcF1Wr17K8/98SDB4MNsdRuXf/q65tXn6QZmAPGxkowxuDo6AjeexARmBlKKTAzOAQ472G0wudXr1xTjWb8eP/gwHa6Pb/Q7ZH3XpAidtYRMw9BSQki8hOVinBFwb9ubfm9P3ZperpuVWCm4IPuLHRRrlT0c6GMgN+59S3Ora5y7+WXxN7ujpJEhXRFQXmRwzknQgicpilCCPDe/++21uK727ews70NKUlIKYHgImmiqNBaY3xiAt/fuY0L60PYQggE74FRDKUUNu/+jHcvXBRZmrLSCoGZlPXWSyGRZxneOr+K6Vr9mYHSw0TMDGYGxHDsDB75Sij2LIkIeZZhbr4l5uZbKIoCAPDNzRvQSuOjTz4FD50gtGZXWDhnQUSsWEphreWoNPaMljEGWZbx4b+PoY0ChIDR+unWCRNFyLKchZSpipREPNMUP21uymYzDkNAxKRIvnfpEmxhsf37b8izPARmYbQJjx4O5OkzZ4Tw3qhHDweHW/fuucmpSffPYDBWrlSCc05mWcqKlJdEwjsnGCynqtVwsL9PgMidLeT9wX0LACUArwHonjDqi2ufXeH1tfM7AN4wwOI48DqA5TfPLv5y/cuE23HjBoBFAK+MeoGEWYJZAMByr/XhUqfzapKwBIZ/zCyWe7PNpYX2x+ud9ShJWPJI/x+H0UR4w6KxHwAAAABJRU5ErkJggg==", 
     "iconuri": None, 
     "tags": None}, 
   {"type": "url", "id": 10, "index": 6, "title": "【本編34分版】3DSで4年を費やし本気で作画してアニメ作ってみた【うごメモ戦士】 - ニコニコ動画", "date_added": 1677140778, "url": "https://www.nicovideo.jp/watch/sm37882117", "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC6UlEQVQ4jW2STWicVRSG33vPvffLmMwk08w4/SZNm8xMZvyJjSGIC0uTnQRBaHWwu4IgoutScVH5wFUXLkoFd5ZSRLIQVwE3BV0UgiASEgyI2E7rNrGE0O/n/hwXMy0YeuFwuZf3vPA+5wDHTrtR/6BarU6OnnJUmK3VmvMn6+8f10sAot/v09ramkqSRApFJ6ZfMD+ebbdfBBAAhO6pUzPGyA0SqtTv92llZUX3AQIgjhsCACLgnbg88QOAGECrOVW+Ow68/TytOF0tn5udn7vYiGdUkWUloQjtVvfv3Z3tyxyC0kZTmqaHjZPxhiuKOLcF1Wr17K8/98SDB4MNsdRuXf/q65tXn6QZmAPGxkowxuDo6AjeexARmBlKKTAzOAQ472G0wudXr1xTjWb8eP/gwHa6Pb/Q7ZH3XpAidtYRMw9BSQki8hOVinBFwb9ubfm9P3ZperpuVWCm4IPuLHRRrlT0c6GMgN+59S3Ora5y7+WXxN7ujpJEhXRFQXmRwzknQgicpilCCPDe/++21uK727ews70NKUlIKYHgImmiqNBaY3xiAt/fuY0L60PYQggE74FRDKUUNu/+jHcvXBRZmrLSCoGZlPXWSyGRZxneOr+K6Vr9mYHSw0TMDGYGxHDsDB75Sij2LIkIeZZhbr4l5uZbKIoCAPDNzRvQSuOjTz4FD50gtGZXWDhnQUSsWEphreWoNPaMljEGWZbx4b+PoY0ChIDR+unWCRNFyLKchZSpipREPNMUP21uymYzDkNAxKRIvnfpEmxhsf37b8izPARmYbQJjx4O5OkzZ4Tw3qhHDweHW/fuucmpSffPYDBWrlSCc05mWcqKlJdEwjsnGCynqtVwsL9PgMidLeT9wX0LACUArwHonjDqi2ufXeH1tfM7AN4wwOI48DqA5TfPLv5y/cuE23HjBoBFAK+MeoGEWYJZAMByr/XhUqfzapKwBIZ/zCyWe7PNpYX2x+ud9ShJWPJI/x+H0UR4w6KxHwAAAABJRU5ErkJggg==", "iconuri": None, "tags": None},
   {"type": "url", "id": 11, "index": 1, "title": "ホモと見る2021年放送されたアニメop集 - ニコニコ動画", "date_added": 1677140792, "url": "https://www.nicovideo.jp/watch/sm41736732", "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC6UlEQVQ4jW2STWicVRSG33vPvffLmMwk08w4/SZNm8xMZvyJjSGIC0uTnQRBaHWwu4IgoutScVH5wFUXLkoFd5ZSRLIQVwE3BV0UgiASEgyI2E7rNrGE0O/n/hwXMy0YeuFwuZf3vPA+5wDHTrtR/6BarU6OnnJUmK3VmvMn6+8f10sAot/v09ramkqSRApFJ6ZfMD+ebbdfBBAAhO6pUzPGyA0SqtTv92llZUX3AQIgjhsCACLgnbg88QOAGECrOVW+Ow68/TytOF0tn5udn7vYiGdUkWUloQjtVvfv3Z3tyxyC0kZTmqaHjZPxhiuKOLcF1Wr17K8/98SDB4MNsdRuXf/q65tXn6QZmAPGxkowxuDo6AjeexARmBlKKTAzOAQ472G0wudXr1xTjWb8eP/gwHa6Pb/Q7ZH3XpAidtYRMw9BSQki8hOVinBFwb9ubfm9P3ZperpuVWCm4IPuLHRRrlT0c6GMgN+59S3Ora5y7+WXxN7ujpJEhXRFQXmRwzknQgicpilCCPDe/++21uK727ews70NKUlIKYHgImmiqNBaY3xiAt/fuY0L60PYQggE74FRDKUUNu/+jHcvXBRZmrLSCoGZlPXWSyGRZxneOr+K6Vr9mYHSw0TMDGYGxHDsDB75Sij2LIkIeZZhbr4l5uZbKIoCAPDNzRvQSuOjTz4FD50gtGZXWDhnQUSsWEphreWoNPaMljEGWZbx4b+PoY0ChIDR+unWCRNFyLKchZSpipREPNMUP21uymYzDkNAxKRIvnfpEmxhsf37b8izPARmYbQJjx4O5OkzZ4Tw3qhHDweHW/fuucmpSffPYDBWrlSCc05mWcqKlJdEwjsnGCynqtVwsL9PgMidLeT9wX0LACUArwHonjDqi2ufXeH1tfM7AN4wwOI48DqA5TfPLv5y/cuE23HjBoBFAK+MeoGEWYJZAMByr/XhUqfzapKwBIZ/zCyWe7PNpYX2x+ud9ShJWPJI/x+H0UR4w6KxHwAAAABJRU5ErkJggg==", "iconuri": None, "tags": None},
   {"type": "url", "id": 12, "index": 2, "title": "かき集めた仲間のスクラップでヘリを購入したハラッコの運命は… - ニコニコ動画", "date_added": 1677140842, "url": "https://www.nicovideo.jp/watch/sm41832974", "icon": None, "iconuri": None, "tags": None}, 
   {"type": "url", "id": 13, "index": 3, "title": "【cover】 チョコレイトと秘密のレシピ / 小宮かふぃー 【まふまふ非公式トリビュート】 - ニコニコ動画", "date_added": 1677140849, "url": "https://www.nicovideo.jp/watch/sm41754723", "icon": None, "iconuri": None, "tags": None}
]

#################################### 出力 ####################################
WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

async def make_title(test_bookmark_dct, session,tag = "description_and_keyword" ,max_num = 36):
  """_summary_

    Args:
        test_bookmark_dct (dict):htmlから抽出したブックマークの情報を入れたdictのlistです
        tag(string):スクレイピングの時に指定するtagです
       max_num(int):生成するタイトルの最大文字数です
    """
  id_txt_category_list = [test_bookmark_dct['id'],test_bookmark_dct['url'], '']
  if len(id_txt_category_list) == 0:
    return []
  else:
    url_to_txt = await category.scraping_meta(id_txt_category_list[1], tag, session)
    input_ids = tokenizer(
      [WHITESPACE_HANDLER(url_to_txt)],
      return_tensors="pt",
      padding="max_length",
      truncation=True,
      max_length=512)["input_ids"]
    output_ids = model.generate(
      input_ids=input_ids,
      max_length=max_num,
      no_repeat_ngram_size=2,
      num_beams=4
      )[0]
    summary = tokenizer.decode(
      output_ids,
      skip_special_tokens=True,
      clean_up_tokenization_spaces=False
      )
  return [id_txt_category_list[0], url_to_txt, summary]

#一度にやる関数を作ったのですがエラーがでるので放置しています
#async def make_title_lst(bookmark_dct_lst,tag = "description_and_keyword" ,max_num = 36 ):
#  """_summary_
#
#    Args:
#        test_bookmark_dct (dict_lst):idやurlなどの情報が入ったdictです。
#        tag(string):スクレイピングの時に指定するtagです
#       max_num(int):生成するタイトルの最大文字数です
#    """
#  async with aiohttp.ClientSession() as session:
#    result_list = await asyncio.gather(*[make_title(x, session, tag, max_num) for x in bookmark_dct_lst])
#  return result_list

  

async def main(): 
  #test_scraping_list = make_title_lst(test_bookmark)
  async with aiohttp.ClientSession() as session:
   test_scraping_list = await asyncio.gather(*[make_title(x, session, tag = "description_and_keyword", max_num = 36) for x in test_bookmark])
  print('test \n')
  print(test_scraping_list)
    

if __name__ == "__main__":
  asyncio.run(main())
