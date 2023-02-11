



class BookMark_Json():
    """Bookmark形式のJsonを扱うClass"""
    
    def __init__(self, bookmark: dict) -> None:
        """Atribute
                bookmark: dict #bookmarkのdict"""
        self.bookmark = bookmark

    def _folder_parse_url(self, bookmark_folder : list):
        bookmark_list = []
        for url in bookmark_folder:
            if(url["type"] == "url"):
                bookmark_list.append(url)
            elif(url["type"] == "folder"):
                bookmark_list +=  self._folder_parse_url(url["children"])

        return bookmark_list
    
    def folder_to_list(self, folder_name : str = None):
        """特定のフォルダーの中のtypeがurlのdictをリストにして返す
        attr
            folder_name : str = None #検索対象のフォルダーを決定する。Noneなら全部
        """
        bookmark_list = []
        for i in self.bookmark:
            if(folder_name != None & i["type"] == "folder" & i["title"] == folder_name):
                bookmark_list += self._folder_parse_url(i["children"])
            elif(folder_name != None):
                continue
            elif(i["type"] == "folder"):
                bookmark_list += self._folder_parse_url(i["children"])
            else:
                bookmark_list.append(i)

        return bookmark_list
            
            
            

    


