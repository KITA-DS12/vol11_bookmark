
import time
import itertools


class BookMark_Json():
    """Bookmark形式のJsonを扱うClass"""
    
    def __init__(self, bookmark: dict) -> None:
        """Atribute
                bookmark: dict #bookmarkのdict"""
        self.bookmark = [bookmark]
        self.bookmark_list = []

    def _folder_parse_url(self, bookmark_folder : list, target_folder : set, children : bool, folder_name : str):
        bookmark_list = []
        if folder_name in target_folder:
            children = True

        for url in bookmark_folder:
            if(url["type"] == "url" and children == True):
                bookmark_list.append(url)
            elif(url["type"] == "folder"):
                bookmark_list +=  self._folder_parse_url(url["children"], target_folder, children, url["title"])

        return bookmark_list
    
    def folder_to_list(self, folder_name : set):
        """特定のフォルダーの中のtypeがurlのdictをリストにして返す
        attr
            folder_name : str = None #検索対象のフォルダーを決定する。Noneなら全部
        """
        bookmark_list = []
        for i in self.bookmark:
            if(i["type"] == "folder"):
                folder_append = self._folder_parse_url(i["children"], folder_name, False, i["title"])
                bookmark_list += folder_append
            else:
                bookmark_list.append(i)


        #重複削除
        duplication = set()
        self.bookmark_list = []
        for bookmark in bookmark_list:
            if(bookmark["url"] in duplication):
                continue
            else:
                self.bookmark_list.append(bookmark)
                duplication.add(bookmark["url"])
        
        return self.bookmark_list
    
    def _delete_folder(self, bookmark_folder : list, target_folder : set):
        bookmark_folder = list(itertools.filterfalse(
            lambda x: (x["title"] in target_folder) and (x["type"] == "folder"), bookmark_folder
        ))
        for bookmark in bookmark_folder:
            if(bookmark["type"] == "folder"):
                bookmark["children"] = self._delete_folder(bookmark["children"], target_folder)

        return bookmark_folder

        
    def list_to_folder(self, categorise: list, target_folder: set):
        """Categoriseされたものをもとの形式に戻す

        Args:
            categorise (list): CategoriseされたList
            target_folder (str): 格納先フォルダー
            folder_name (set):消すフォルダー
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


        append_dict = {
            "type" : "folder",
            "id" : 0,
            "index" : 0,
            "title" : "unpacker",
            "date_added" : int(time.time()),
            "children" : bookmark_list
        }




        self.bookmark[0]["children"] =  self._delete_folder(self.bookmark[0]["children"], target_folder)
        self.bookmark[0]["children"].append(append_dict)
        return self.bookmark[0]

    def _reset_id(self, folder : dict, current = 0):
        folder["id"] = current
        current += 1
        
        for child in folder["children"]:
            if(child["type"] == "folder"):
                current = self._reset_id(child, current)

            else:
                child["id"] = current
                current += 1


            
        return current + 1
            

        

    def sort_id(self):
        """idをSortする"""
        try:
            self._reset_id(folder=self.bookmark[0],current = 0)
            return self.bookmark[0]
        except KeyError:
            self._reset_id(folder=self.bookmark[0]["item"],current = 0)
            return self.bookmark[0]["item"]
        
                
            

        

        
        
            
            
            

    


