
from InstaUserInfo import username,password  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait



class Instagram:
    def __init__(self,username,password):
        self.browser=webdriver.Chrome()
        self.username=username
        self.password=password
        self.followers=[]
        
        
        
    
    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/?hl=tr")
        self.browser.maximize_window()
        time.sleep(2) 
        
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(self.username)
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(self.password)
        
        
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[3]").click() 
        time.sleep(3)
        
        
        
    def getFollowers(self):
        self.browser.get("https://www.instagram.com/"+self.username+"/following/?hl=tr") ##kendi kullanıcı adınızı buraya direkt olarak da yazabilirsiniz.
        
        time.sleep(2)
        
        jscommand="""
        followers=document.querySelector("._aano");
        followers.scrollTo(0,followers.scrollHeight);
        followers.scrollTo(0,followers.scrollHeight);
        var lenOfPage=followers.scrollHeight;
        return lenOfPage;
        
        """
        lenOfPage=self.browser.execute_script(jscommand)
        match=False
        while(match==False):
            lastCount=lenOfPage
            time.sleep(3)
            lenOfPage=self.browser.execute_script(jscommand)
            if lastCount==lenOfPage:
                match=True
        time.sleep(5)        
        

        followers=self.browser.find_elements_by_css_selector("._ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm")
        for follower in followers:
             follower=follower.text.replace("Doğrulanmış","") 
             follower=follower.replace("\n","")
             self.followers.append(follower) ##Normalde parantez içinne follower.text yazmalıydık ama zaten üstte textini aldık.

                 
    
    def addFile(self):
        counter=1
        with open("C:\F.txt","w") as file:
            for a in self.followers:
                file.write(str(counter)+")"+a+"\n")
                counter+=1
        
        
            
        
    def autoFollow(self):
        followList=["","",""]
        counter2=0
        while counter2<len(followList):
            self.browser.get("https://www.instagram.com/"+followList[counter2]+"/?hl=tr") #profilime gidiş(takipci panelini kapatabilmek için)
            time.sleep(3)       
            searchBt=self.browser.find_element_by_css_selector("._aacl._aaco._aacw._adda._aad6._aade")
            if searchBt.text=="Takip Et":
                searchBt.click()
                time.sleep(1)
        
            else:
                print(followList[counter2]+" adlı hesap zaten takip ediliyor...")
                time.sleep(1)
            
            counter2+=1
            
    def autoUnfollow(self):
        unfollowList=["","",""]
        counter2=0
        while counter2<len(unfollowList):
            self.browser.get("https://www.instagram.com/"+unfollowList[counter2]+"/?hl=tr") #profilime gidiş(takipci panelini kapatabilmek için)
            time.sleep(3)       
            searchBt=self.browser.find_element_by_css_selector("._aacl._aaco._aacw._adda._aad6._aade") 
            if searchBt.text!="Takip Et":
                searchBt.click()
                time.sleep(2)
                unfBtn=self.browser.find_element_by_css_selector("._a9--._a9-_")
                unfBtn.click()
                print("UNFOLLOW EDİLDİ.")
        
            else:
                print(unfollowList[counter2]+" adlı hesap zaten takip edilmiyor...")
            
            counter2+=1
        
        
    def autoPhotoLike(self):
        autoPhotoLikeList=[""]
        self.browser.get("https://www.instagram.com/"+autoPhotoLikeList[0]+"/?hl=tr")
        time.sleep(1)
        numberOfPhotos=self.browser.find_element_by_xpath('.//span[@class = "_ac2a"]')  ##SPAN CLASS İÇİNDEKİ TEXTİ GETİRME !!     
        numberOfPhotosText=numberOfPhotos.text.replace(",","") ##foto sayısını çekerken 1,356 olarak çekiyordu o yüzden virgülü kaldırdım.
        numberOfPhotosText=int(numberOfPhotosText)
        
        numberOfPhotosCounter=0
        openPhotoButton=self.browser.find_element_by_css_selector("._aagu") ##bunu döngünün içine koymadım çünkü ilk fotoya tıkladıktan sonra gerisine tıklamasına gerek yok. Sürekli sagdaki geçiş butonuna basarak devam edebilir.
        openPhotoButton.click()
        time.sleep(1)
        
        while numberOfPhotosCounter<numberOfPhotosText:
            time.sleep(2)
            likeButton=self.browser.find_element_by_css_selector("._abm0._abl_") 
            likeButton.click()
            time.sleep(2)
        
            rightSideButton=self.browser.find_element_by_css_selector("._aaqg._aaqh")
            rightSideButton.click()
            numberOfPhotosCounter+=1
            
        
    
    
    
        
    def autoMessageSend(self,nameOfThePersonSendMessage,messageText):
        self.browser.get("https://www.instagram.com/"+nameOfThePersonSendMessage+"/?hl=tr")
        time.sleep(1)
        sendMessageButton=self.browser.find_element_by_css_selector("._ab8w._ab94._ab99._ab9f._ab9m._ab9o._abb0._ab9s._abcm")
        sendMessageButton.click()
        time.sleep(2)
        simdiDegilButton=self.browser.find_element_by_css_selector("._a9--._a9_1")
        simdiDegilButton.click()
        time.sleep(2)
        
        messageArea=self.browser.find_element_by_css_selector(".focus-visible") ##focus-visible textarea'nın class name'i
        #messageArea.click()
        messageArea.send_keys(messageText) #Hangi mesajı göndermek istiyorsak
        messageArea.send_keys(Keys.ENTER)
    
    
insta=Instagram(username, password)
insta.signIn()
insta.getFollowers()
insta.addFile()
insta.autoFollow()
insta.autoUnfollow()
insta.autoPhotoLike()
insta.autoMessageSend()
insta.followers
