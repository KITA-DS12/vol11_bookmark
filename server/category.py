#ライブラリ
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

#入力
#クラスタリングしたいフォルダの種類一覧
candidate_labels_list = ["食べ物","研究","開発"]
#ブックマークの情報
book_mark_info_list =[
        {
          "type": "url",
          "id": 4,
          "index": 0,
          "title": "Google",
          "date_added": 1676090342,
          "url": "https://www.google.com/",
          "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACIklEQVQ4jYWSS0iUURTHf/fe8RvHooE2VlT2FNqUGWmNEYUR9lhEEVJhUIsoXOQuap1Rq6KHNQt3LaPAIOxhlNTChUwLMU3NR1CklUzg6xvPd1ro2KhTHjjcA/e8/uf/hzmmqsUiEheRLhHxp/2TiDxQ1aK5+ZmFeSJSrwuYiMRVNZKuMxnFz51zu9T3GX/6iPGmRqS/F5WAUMEawuUVRI5UYjwPEWl2zlUYY8YMgIjUW2vPBkPfSV6uYbKvJ+uW3rZSojfuABAEQdw5d96oajHQqr7P8IUqpL8X43lEjp3EK4mBtfgt75l4+4po7U3cytWZPbcyjUlTidv642ipDu7foX7bh2zgs92jDhHpUlWdbNmuEw15OvqweqE7ZjboCAEFADrSjs1LkRM7NAt3+bWRebfYudFx9XguwFqbwePs9z/mT/6NLdAHMBpex28W0/C1Y1Zy05VFM75nUwiAZVGT/v5sgdcA3UurOPUrxvXOFhJD7fOmdn4LeNc5NbpkfWimv5mWZ8KXFKdfXqInOYBnc6gsPEjZ8mKssbQOtvEkMczYl0oK8z3un4lgppbYkhZS3Fp7bnD0Jxeba+lODmTFviFcxq29NeRHDUEQ1DnnqtNSjohIo3Nutx+keNz9gmf9zfQkB0ChYMkK9q2KcaLwMJFQGFV9Y4w5YIwZzyBBI2lRLcD9PVXN/SdFqlokInUi0iEiE9P+UUTuqurmufl/AKTzsFGmvUNUAAAAAElFTkSuQmCC",
          "icouri" : None,
          "tags" : None
        },
        {
          "type": "url",
          "id": 5,
          "index": 1,
          "title": "lofi hip hop radio - beats to relax/study to - YouTube",
          "date_added": 1676090372,
          "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
          "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=",
          "icouri" : None,
          "tags" : None
        },
        {
            "type": "url",
            "id": 7,
            "index": 0,
            "title": "ChatGPTが変える働き方　AIリスクは増加へ【WBS】（2023年1月27日）　Open AI イーロンマスク　チャットGPT - YouTube",
            "date_added": 1676090386,
            "url": "https://www.youtube.com/watch?v=cHikHtiVwXU",
            "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=",
          "icouri" : None,
          "tags" : None
            },
        {
            "type": "url",
            "id": 9,
            "index": 0,
            "title": "白石麻衣 × 絢香 - にじいろ / THE FIRST TAKE powered by ASAHI SUPER DRY - YouTube",
            "date_added": 1676090380,
            "url": "https://www.youtube.com/watch?v=XGmYvJB8mlc",
            "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABx0lEQVQ4jZ2TQWtTQRDHfzO7yUsNKSG0heJJ0YKnCvVSkHrV7+BBeu7Vk9+lH8CLN6EXk4Lo1V48lGClFBELGmmSmr73djy8fS8vll4c+LO7s7OzM///LhQmBmrg+uDtZrgIBQQAKyf/YQbiBexFt9t9niSP7ji3umrW7og0UfWL0ZaOzGYjmBxn2c/BdPpJxuNz+vDwFxxnqmaqZs4V8L5AuS6haqmqXcDpO3jCEN4YmEFmkMcxrSCSGqSh8GcGIY52Am91Ce5HJ5EYBRwbG45222HmUHVS+DX2DhASuKu3oAeolGSqCiDs7gqHh8L2thCCxOQSbxFAO9BToClzNQSJokwmsLUFgwHs78P6eklnlQho6c0axUKbTVhZgUYjHpeqCwE8kMWFxYNF9uVlGA5hbw8ODuqJzajqnPENPtfYDxU2N4OtrRVzkVDfC0V8/h2G/g98AR7ESkJF8tFRcYdzkOf15iRW6y/hlD48voCz+BbmELFrvhrG8OMjPBOAV3D7qXM791R73Var00qSJRoNTyifB5Dn+eVsNv19dTX+mmWj93n+4SWciM1LKkmqy7RoImFBqPqPfH39K7t/4A18f74nAH8Bjm35s3ZkOjEAAAAASUVORK5CYII=",
          "icouri" : None,
          "tags" : None
        }
        ]
#閾値
category_score = 0.5
#その他ファイルの名前
other_folder_name= 'その他'

#出力
def make_folder_category_list (book_mark_info_list,candidate_labels_list,other_folder_name = 'その他',category_score = 0.5):
  """_summary_

  Args:
      book_mark_info_list (dict_list):htmlから抽出したブックマークの情報を入れたdictのlistです。
      candidate_labels_list (string_list): ユーザーが入力したフォルダ名のリストです。
      other_folder_name (string): クラスタリングで外れたものを入れるフォルダの名前です。
      category_score (float): クラスタリングする際に使う閾値です。各フォルダに割り振られる確率の最大値がこの閾値より低ければ<other_folder_name>に割り当てます。
  """  
  def make_id_txt_category_list(book_mark_info_list):
    def make_id_txt_category (book_mark_info):
      id_txt_category =[book_mark_info['id'],book_mark_info[ 'title'] , '']
      return id_txt_category
    id_txt_category_list = [make_id_txt_category(v) for v in book_mark_info_list]
    return id_txt_category_list
  id_txt_category_list = make_id_txt_category_list(book_mark_info_list)
  #クラスタリングして候補を取り出す
  def update_foldername(id_foldername,candidate_labels_list,other_folder_name,category_score):
    output = id_foldername
    sequence_to_classify = id_foldername[1]
    candidate_labels = candidate_labels_list
    model_value = classifier(sequence_to_classify, candidate_labels, multi_label=False)
    score_list = model_value['scores']
    max_score = max(score_list)
    if category_score > max_score:
      output[2] = other_folder_name
    else:
      max_score_index = score_list.index(max_score )
      max_score_folder_name = model_value['labels'][max_score_index ]
      output[2] = max_score_folder_name
    return output
  output_id_txt_category_list = [update_foldername(v,candidate_labels_list,other_folder_name,category_score) for v in id_txt_category_list]
  return output_id_txt_category_list

if __name__ == "__main__":
    print(make_folder_category_list (book_mark_info_list,candidate_labels_list,other_folder_name,category_score))