from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QListWidgetItem, QFileDialog
from PySide2.QtUiTools import QUiLoader
from lib.public import shared_module
from ui.chatroom_ui import Ui_chatroom
from chating_item import Chating_item
from chat_bubble import Message_bubble
from datetime import datetime
import os,sys
class Main_win(QWidget):

    def __init__(self):
        super().__init__()
        self.ui= Ui_chatroom()
        self.ui.setupUi(self)
        
#以下是正式的的信號槽和函數
        self.ui.send_butt.clicked.connect(self.send)
        self.ui.add_friend_butt.clicked.connect(self.add_friend)
        self.ui.get_new_friend.clicked.connect(self.check_add_friend)
        self.ui.send_file_butt.clicked.connect(self.show_file_dialog)
        #維護一個當前顯示的對象id
        self.cur_id =None

        # 用于动态维护的好友列表和消息列表
        self.friend_item = []
        self.chat_item = []
        

#以上是最終實現的信號槽
#以下是測試用的信號槽和函數
        self.ui.add_new_chat.clicked.connect(self.add_test)
    
    def add_test(self):
            #以下測試
            self.ui.chat_list_view.clear()
#以上是測試用的函數和槽


#以下是添加好友相關功能
    def add_friend(self):
        shared_module.add_friend.show()

        #测试成功
        

    def check_add_friend(self):
        
        shared_module.new_friends.show()
        shared_module.new_friends.add_message()
        #opp_id。
        #shared_module.client.ans_addfriend(yes_or_no, opp_id,defult)
        pass


    def rcv_addfriend(self, back_data, content):
        # 收到对方的添加好友请求
        # 返回发送者的用户ID和时间戳
        sender = content["sender"]
        time = content["time"]
        name = content["name"]
        shared_module.client.add_friend_list.append((sender, time, name))
        print(("收到了好友申请", sender, time, name))

    def rcv_ans_addfriend(self, back_data, content):
        # 对方接收到同意或拒绝添加好友请求的回复
        # 返回发送者的用户ID、时间戳和回复内容

        # 对方收到好友请求并确定是否同意
        if back_data == "0000":
            
            sender = content["sender"]
            time = content["time"]
            ans = content["ans"]
            name = content["name"]
            print( [sender, time, ans,name])

            if ans == "yes":
                #TODO：添加到好友列表 defult
                #TODO：添加到聊天列表

                pass
            else : 
                #别知道了 ，，或者是在信号由申请列表显示谁谁谁拒绝
                pass
        elif back_data == "0001":
            print("查无此人")
            QMessageBox.information(self,"查无此人","请检查id是否正确")

#以上是添加好友相關函數

#以下是发送文件功能
    def show_file_dialog(self):
        """这个函数负责让用户选择要发送的文件并将文件地址提取出来"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        full_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)', options=options)

        if full_path:
            # 这个里面有full_path, base_name是文件名称的“example.txt",file_extension是文件类型字符串
            print('Selected File:', full_path)
            base_name = os.path.basename(full_path)
            file_extension = os.path.splitext(base_name)[1]
            display_text = f'<a href="file:{full_path}">文件名：{base_name}</a><br>文件类型：{file_extension}'

    def update_label(self, text):
        self.text_browser.setHtml(text)

    def open_file(self, link):
        if sys.platform.startswith('win'):
            os.startfile(link)  # 适用于Windows系统
        elif sys.platform.startswith('darwin'):
            os.system(f'open "{link}"')  # 适用于macOS系统
        elif sys.platform.startswith('linux'):
            os.system(f'xdg-open "{link}"')  # 适用于Linux系统
#以上是发送文件功能
#以下是收發消息相關函數
    def send(self):
        # 获取发送框中的文本
        message = self.ui.text_in.toPlainText()
        #维护一个当下的聊天对象的id
        # 在这里添加发送的功能
        #请在这里给我发消息的对象id
        chat_id=self.cur_id #私聊是10位，群聊是五位，2開頭
        
        #TODO： lihao寫這裡的邏輯
        #如果chat_id是群聊，調用group_chat(self, msg, group_id)
        #如果是私聊，調用friend_chat(self, msg, chat_id)

        self.ui.text_in.clear()
        
    def print_online_message(self,chat_id, sender_id, time:str="" , msg:str=""):
        """把在線的消息打印出來,如果不是當前窗口，存在文件里
        要找name,avatar_path
        """

        #在這裡面找到sender_name和sender_avatar_path
        sender_name="sender_name"
        sender_avatar_path="sender_avatar_path"
        #在這裡面找到sender_name和sender_avatar_path
        if self.cur_id==chat_id:
            self.add_one_message(sender_id,sender_name,sender_avatar_path, time, msg)
            pass
        else :
            #在這裡寫直接存消息的東西
            pass

#以上是收發消息相關函數

#以下是聊天列表的功能函數
    def init_chat_list(self):
        """這個函數用來從登陸界面打開時初始化聊天列表"""
        for chat_id, sender_id, time, msg in shared_module.client.msg_list :
            #TODO：
            #這裡寫找到頭像路徑的函數
            self.img_path = "lib/login_back.png"
            self.image_path=os.path.join(os.path.dirname(__file__), self.img_path)
            #上面寫找到頭像路徑的函數
            #找到對方名字的函數
            name = shared_module.client.find_name(chat_id)
            #下面調用之增加一個list的函數
            self.add_one_list(chat_id, sender_id, name,self.image_path, time, msg)

        pass

    def add_one_list(self,chat_id, sender_id,name,avatar_path, time:str="" , msg:str=""):

        """實例化一個消息列表框"""
        new_chat_bar=Chating_item(chat_id,sender_id,name,avatar_path,time,msg)
        self.chat_item.insert(0,new_chat_bar)
        #將消息列表框放進item里
        list_item=QListWidgetItem()
        list_item.setSizeHint(new_chat_bar.sizeHint())
        self.ui.chat_list_view.insertItem(0,list_item)
        self.ui.chat_list_view.setItemWidget(list_item,new_chat_bar)
        #如果框體被點擊，連接到的函數
        new_chat_bar.itemClicked.connect(self.chating_item_clicked)

    def del_one_list(self,chat_id):
        """在動態List里找到該item的位置"""
        ind = 0
        for i in self.chat_item:
            if i.chat_id == chat_id:
                break
            ind += 1
        #刪掉ui里的東西
        self.chat_item.remove(i)
        item_to_remove=self.ui.chat_list_view.takeItem(ind)
        item_to_remove=None
        pass

    def renew_list(self,chat_id, sender_id,name,avatar_path, time:str="" , msg:str=""):
        """更新消息的時候要用"""
        self.del_one_list(chat_id)
        self.add_one_list(self,chat_id, sender_id,name,avatar_path, time , msg)
#以上是聊天列表的功能函數
    

#以下是聊天窗口的功能函數
    def chating_item_clicked(self,chat_id):
        """
        这是跳转函数，点击聊天列表跳转到对应的聊天，具体实现如下：

        #收到点击的value（也即用户id)，
        #获取对应用户的历史聊天记录（从本地）
        #循环加载add_message
        """
        print("Item clicked with value:", chat_id)

        #如果點擊到的列表本身就是窗口里的，pass
        if self.cur_id==chat_id:
            pass
        #如果列表本身是新的，清空列表模擬重新加載
        else :  
            self.ui.view_box.clear()
            self.cur_id=chat_id
            if len(shared_module.client.msg_list) == 0:
                print("聊天消息列表为空")
            while len(shared_module.client.msg_list) > 0:
                #这里要pop吗？
                (chat_id, sender_id, chat_time, chat_content) = shared_module.client.msg_list.pop(0)
                #TODO lihao将上述元组的數據來源改一下
                #同時我只需要sender_id,sender_name,chat_time,chat_content。
                #chat_id是整数，sender_id是整数，chat_time是datetime格式，chat_content是字符串
                sender_name=str(sender_id)
                avatar_path="test"
                self.add_one_message(sender_id,sender_name,avatar_path,chat_time, chat_content)
                print(chat_id,"的消息列表打印完毕")

    def add_one_message(self,sender_id,sender_name,sender_avatar_path, time:str="", msg:str=""):
        """
        調用這個函數來打印消息

        :sender_id根據是不是自己可以將消息顯示成兩種不同的氣泡

        :avatar_path,time为收到该条消息的时间，msg为消息内容
        """
        show_message=Message_bubble(sender_id,sender_name,sender_avatar_path,time,msg)
        message_item=QListWidgetItem(self.ui.view_box)
        message_item.setSizeHint(show_message.sizeHint())
        self.ui.view_box.setItemWidget(message_item,show_message)



if __name__ == "__main__":
    app = QApplication([])
    login = Main_win()
    login.show()
    app.exec_()