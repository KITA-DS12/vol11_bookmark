
import time


class BookMark_Json():
    """Bookmark形式のJsonを扱うClass"""
    
    def __init__(self, bookmark: dict) -> None:
        """Atribute
                bookmark: dict #bookmarkのdict"""
        self.bookmark = [bookmark]
        self.bookmark_list = []

    def _folder_parse_url(self, bookmark_folder : list, target_folder : str, children : bool, folder_name : str):
        bookmark_list = []
        if folder_name == target_folder:
            children = True

        for url in bookmark_folder:
            if(url["type"] == "url" and children == True):
                bookmark_list.append(url)
            elif(url["type"] == "folder"):
                bookmark_list +=  self._folder_parse_url(url["children"], target_folder, children, url["title"])

        return bookmark_list
    
    def folder_to_list(self, folder_name : str = ""):
        """特定のフォルダーの中のtypeがurlのdictをリストにして返す
        attr
            folder_name : str = None #検索対象のフォルダーを決定する。Noneなら全部
        """
        bookmark_list = []
        for i in self.bookmark:
            if(folder_name != "" and i["type"] == "folder"):
                folder_append = self._folder_parse_url(i["children"], folder_name, False, i["title"])
                bookmark_list += folder_append
            elif(i["type"] == "folder" and folder_name == ""):
                folder_append = self._folder_parse_url(i["children"], folder_name, True)
                bookmark_list += folder_append
            else:
                bookmark_list.append(i)

        self.bookmark_list = bookmark_list
        return bookmark_list

        
    def list_to_folder(self, categorise: list, target_folder: str = ""):
        """Categoriseされたものをもとの形式に戻す

        Args:
            categorise (list): CategoriseされたList
            target_folder (str): 格納先フォルダー
        """
        #bookmarklistを加工してindexをidにする
        bookmark_list_dict = {}

        for i in self.bookmark_list:
            bookmark_list_dict[i["id"]] = i

        #フォルダーのリストを生成する
        folder_list : dict[list] = {}

        for i in categorise:
            folder_list[i[2]] = []
        for i in categorise:
            folder_list[i[2]].append(i[0])

        #フォルダーを生成する
        bookmark_list = []
        folder_index = 0
        for (i, j) in folder_list.items():
            bookmark_list.append({
                "type" : "folder",
                "id" : folder_index + 1,
                "index" : folder_index,
                "title" : i,
                "date_added" : int(time.time()),
                "children" : []
            })
            bookmark_id = 0
            for k in j:
                bookmark = bookmark_list_dict[k]
                bookmark["index"] =  bookmark_id
                bookmark_id += 1
                bookmark_list[folder_index]["children"].append(bookmark)

            folder_index += 1

        if(target_folder == ""):

            self.bookmark_list = {
                "type" : "folder",
                "id" : 0,
                "index" : 0,
                "title" : "root",
                "date_added" : int(time.time()),
                "children" : bookmark_list
            }

            return self.bookmark_list

        else:
            def replace_folder(target):
                for i in target:
                    if(i["type"] == "folder"):
                        if(i["title"] == target_folder):
                            i["children"] = bookmark_list
                        else:
                            replace_folder(i["children"])

            replace_folder(self.bookmark)
            return self.bookmark[0]
                
            

        

        
        
            
            
            

    


